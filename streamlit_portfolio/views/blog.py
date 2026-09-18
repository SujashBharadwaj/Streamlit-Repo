import re
import streamlit as st
from pathlib import Path
from utils.helpers import normalize_math, resolve_markdown_images, sanitize_html
from components.oee import render_oee_interactive
from components.means import render_means_interactive
from components.gradient_descent import render_gradient_descent_interactive

OEE_MARKER = "## A simple OEE calculation snippet (Python)"


def blog_view(posts):
    if not posts:
        st.markdown("## Blog")
        st.info("No posts found yet.")
        return

    # Initialise sub-view state
    if "blog_detail_open" not in st.session_state:
        st.session_state["blog_detail_open"] = False

    # ---- Route: Reader view or Index ----
    if st.session_state["blog_detail_open"] and st.session_state.get("selected_post"):
        _reader_view(posts)
    else:
        _index_view(posts)


# =====================================================================
# Index / Catalog view — card grid only
# =====================================================================
def _index_view(posts):
    st.markdown("## Blog")
    st.markdown('<div class="muted">Short learning notes and project logs.</div>', unsafe_allow_html=True)
    st.markdown("")

    q = st.text_input("Search posts", placeholder="Type to search by title or content...", key="blog_search")
    filtered = posts
    if q.strip():
        qq = q.strip().lower()
        filtered = [p for p in posts if qq in p["title"].lower() or qq in p["content"].lower()]

    if not filtered:
        st.info("No posts match your search.")
        return

    st.markdown("### Articles")
    cols = st.columns(min(len(filtered), 3), gap="small")
    for i, p in enumerate(filtered):
        post_path = str(p["path"])
        with cols[i % min(len(filtered), 3)]:
            tag_pills = "".join([f"<span class='project-chip'>{t}</span>" for t in p.get("tags", [])[:3]])
            st.markdown(
                sanitize_html(f"""
                <div class="card" style="min-height:130px; cursor:pointer;">
                  <div style="font-size:1.12rem; font-weight:700;">{p['title']}</div>
                  <div class="tiny" style="margin-top:4px;">{p.get('date', '')}</div>
                  <div class="muted" style="margin-top:6px; font-size:.95rem;">{p['excerpt'][:100]}...</div>
                  <div style="margin-top:6px;">{tag_pills}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )
            if st.button(
                "Read article →",
                key=f"blog_card_{i}",
                use_container_width=True,
            ):
                st.session_state["selected_post"] = post_path
                st.session_state["blog_detail_open"] = True
                st.rerun()


# =====================================================================
# Reader view — dedicated page for a single article
# =====================================================================
def _reader_view(posts):
    selected_path = st.session_state.get("selected_post", "")
    post = next((p for p in posts if str(p["path"]) == selected_path), None)

    if post is None:
        st.session_state["blog_detail_open"] = False
        st.rerun()
        return

    post_path_obj = Path(post["path"])

    # ---- Top nav bar ----
    st.markdown("")
    nav_left, nav_right = st.columns([1, 2], gap="small")
    with nav_left:
        if st.button("← Back to all posts", key="back_to_blog_index", use_container_width=True):
            st.session_state["blog_detail_open"] = False
            st.rerun()
    with nav_right:
        all_titles = [p["title"] for p in posts]
        path_by_title = {p["title"]: str(p["path"]) for p in posts}
        new_title = st.selectbox(
            "Jump to article",
            all_titles,
            index=all_titles.index(post["title"]),
            key="blog_reader_selectbox",
            label_visibility="collapsed",
        )
        if path_by_title[new_title] != selected_path:
            st.session_state["selected_post"] = path_by_title[new_title]
            st.rerun()

    # ---- Article header ----
    st.markdown(f"### {post['title']}")
    meta_bits = []
    if post["date"]:
        meta_bits.append(post["date"])
    if post.get("tags"):
        meta_bits.append(" | ".join([f"`{t}`" for t in post["tags"]]))
    if meta_bits:
        st.markdown(f"<div class='tiny'>{' | '.join(meta_bits)}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---- Article body ----
    is_oee_post = (
        "oee" in post["title"].lower()
        or "overall equipment effectiveness" in post["title"].lower()
        or post_path_obj.stem.lower().endswith("oee")
        or "oee" in post_path_obj.stem.lower()
    )

    content = normalize_math(post["content"])
    content = resolve_markdown_images(content, post_path_obj.parent)

    # Strip redundant leading H1 if it mirrors post['title']
    content_lines = content.lstrip().splitlines()
    if content_lines and content_lines[0].startswith("# "):
        h1_text = content_lines[0].lstrip("# ").strip().lower()
        if h1_text == post["title"].strip().lower():
            content = "\n".join(content_lines[1:]).lstrip()

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post_path_obj.stem.lower())
    is_means_post = slug == "means-guide"
    is_gd_post = slug == "gradient-descent"

    if is_oee_post and OEE_MARKER in content:
        before, after = content.split(OEE_MARKER, 1)
        st.markdown(before, unsafe_allow_html=True)
        st.markdown("---")
        render_oee_interactive()
        after_clean = re.sub(r"^\s*```python[\s\S]*?```\s*", "", after, count=1).lstrip()
        st.markdown("---")
        st.markdown(after_clean, unsafe_allow_html=True)
    elif is_means_post and "## Interactive playground" in content:
        before, after = content.split("## Interactive playground", 1)
        st.markdown(before, unsafe_allow_html=True)
        st.markdown("---")
        render_means_interactive()
        if "## Takeaways" in after:
            _, tail = after.split("## Takeaways", 1)
            st.markdown("---")
            st.markdown("## Takeaways" + tail, unsafe_allow_html=True)
    elif is_gd_post and "## Interactive playground (1-D, cubic only)" in content:
        before, after = content.split("## Interactive playground (1-D, cubic only)", 1)
        st.markdown(before, unsafe_allow_html=True)
        st.markdown("---")
        render_gradient_descent_interactive()
        if "## Usage in machine learning" in after:
            _, tail = after.split("## Usage in machine learning", 1)
            st.markdown("---")
            st.markdown("## Usage in machine learning" + tail, unsafe_allow_html=True)
    else:
        st.markdown(content, unsafe_allow_html=True)

    # ---- Bottom prev / next navigation ----
    st.markdown("---")
    all_paths = [str(p["path"]) for p in posts]
    idx = all_paths.index(selected_path)
    prev_col, _, next_col = st.columns([1, 2, 1])
    if idx > 0:
        with prev_col:
            if st.button(f"← {posts[idx - 1]['title']}", key="prev_post", use_container_width=True):
                st.session_state["selected_post"] = all_paths[idx - 1]
                st.rerun()
    if idx < len(all_paths) - 1:
        with next_col:
            if st.button(f"{posts[idx + 1]['title']} →", key="next_post", use_container_width=True):
                st.session_state["selected_post"] = all_paths[idx + 1]
                st.rerun()
