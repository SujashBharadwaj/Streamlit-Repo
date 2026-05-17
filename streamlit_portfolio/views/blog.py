import re
import streamlit as st
from pathlib import Path
from utils.helpers import normalize_math, resolve_markdown_images, sanitize_html
from components.oee import render_oee_interactive
from components.means import render_means_interactive
from components.gradient_descent import render_gradient_descent_interactive

OEE_MARKER = "## A simple OEE calculation snippet (Python)"


def blog_view(posts):
    st.markdown("## Blog")
    st.markdown('<div class="muted">Short learning notes and project logs.</div>', unsafe_allow_html=True)
    st.markdown("")

    if not posts:
        st.info("No posts found yet.")
        return

    q = st.text_input("Search posts", placeholder="Type to search by title or content...", key="blog_search")
    filtered = posts
    if q.strip():
        qq = q.strip().lower()
        filtered = [p for p in posts if qq in p["title"].lower() or qq in p["content"].lower()]

    if not filtered:
        st.info("No posts match your search.")
        return

    # ---- Card-based post selection (replaces old selectbox) ----
    selected_path = st.session_state.get("selected_post", "")

    # If there is no selection or the selection isn't in filtered, default to first
    filtered_paths = [str(p["path"]) for p in filtered]
    if selected_path not in filtered_paths:
        selected_path = filtered_paths[0]
        st.session_state["selected_post"] = selected_path

    st.markdown("### Articles")
    cols = st.columns(min(len(filtered), 3), gap="small")
    for i, p in enumerate(filtered):
        post_path = str(p["path"])
        with cols[i % min(len(filtered), 3)]:
            is_active = post_path == selected_path
            border_color = "rgba(163,230,53,.55)" if is_active else "rgba(229,231,235,.10)"
            tag_pills = "".join([f"<span class='project-chip'>{t}</span>" for t in p.get("tags", [])[:3]])
            st.markdown(
                sanitize_html(f"""
                <div class="card" style="border-color:{border_color}; min-height:130px; cursor:pointer;">
                  <div style="font-size:1.12rem; font-weight:700;">{p['title']}</div>
                  <div class="tiny" style="margin-top:4px;">{p.get('date', '')}</div>
                  <div class="muted" style="margin-top:6px; font-size:.95rem;">{p['excerpt'][:100]}...</div>
                  <div style="margin-top:6px;">{tag_pills}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )
            if st.button(
                "Read" if not is_active else "✓ Selected",
                key=f"blog_card_{i}",
                use_container_width=True,
                disabled=is_active,
            ):
                st.session_state["selected_post"] = post_path
                st.rerun()

    # ---- Render selected post ----
    post = next(p for p in filtered if str(p["path"]) == selected_path)
    post_path_obj = Path(post["path"])

    st.markdown("---")

    is_oee_post = (
        "oee" in post["title"].lower()
        or "overall equipment effectiveness" in post["title"].lower()
        or post_path_obj.stem.lower().endswith("oee")
        or "oee" in post_path_obj.stem.lower()
    )

    st.markdown(f"### {post['title']}")
    meta_bits = []
    if post["date"]:
        meta_bits.append(post["date"])
    if post.get("tags"):
        meta_bits.append(" | ".join([f"`{t}`" for t in post["tags"]]))
    if meta_bits:
        st.markdown(f"<div class='tiny'>{' | '.join(meta_bits)}</div>", unsafe_allow_html=True)

    st.markdown("---")

    content = normalize_math(post["content"])
    content = resolve_markdown_images(content, post_path_obj.parent)

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post_path_obj.stem.lower())
    is_means_post = slug == "means-guide"
    is_gd_post = slug == "gradient-descent"

    if is_oee_post and OEE_MARKER in content:
        before, after = content.split(OEE_MARKER, 1)
        st.markdown(sanitize_html(before), unsafe_allow_html=True)
        st.markdown("---")
        render_oee_interactive()
        after_clean = re.sub(r"^\s*```python[\s\S]*?```\s*", "", after, count=1).lstrip()
        st.markdown("---")
        st.markdown(sanitize_html(after_clean), unsafe_allow_html=True)
    elif is_means_post and "## Interactive playground" in content:
        before, after = content.split("## Interactive playground", 1)
        st.markdown(sanitize_html(before), unsafe_allow_html=True)
        st.markdown("---")
        render_means_interactive()
        if "## Takeaways" in after:
            _, tail = after.split("## Takeaways", 1)
            st.markdown("---")
            st.markdown(sanitize_html("## Takeaways" + tail), unsafe_allow_html=True)
    elif is_gd_post and "## Interactive playground (1-D, cubic only)" in content:
        before, after = content.split("## Interactive playground (1-D, cubic only)", 1)
        st.markdown(sanitize_html(before), unsafe_allow_html=True)
        st.markdown("---")
        render_gradient_descent_interactive()
        if "## Usage in machine learning" in after:
            _, tail = after.split("## Usage in machine learning", 1)
            st.markdown("---")
            st.markdown(sanitize_html("## Usage in machine learning" + tail), unsafe_allow_html=True)
    else:
        st.markdown(sanitize_html(content), unsafe_allow_html=True)
