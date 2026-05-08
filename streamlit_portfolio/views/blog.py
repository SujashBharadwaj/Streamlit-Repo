import re
import streamlit as st
from utils.helpers import normalize_math, resolve_markdown_images
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

    post_titles = [p["title"] for p in filtered]

    default_idx = 0
    if st.session_state["selected_post"]:
        for i, p in enumerate(filtered):
            if str(p["path"]) == st.session_state["selected_post"]:
                default_idx = i
                break

    selected = st.selectbox("Select a post", post_titles, index=default_idx, key="blog_selectbox")
    post = next(p for p in filtered if p["title"] == selected)
    st.session_state["selected_post"] = str(post["path"])

    is_oee_post = (
        "oee" in post["title"].lower()
        or "overall equipment effectiveness" in post["title"].lower()
        or post["path"].stem.lower().endswith("oee")
        or "oee" in post["path"].stem.lower()
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
    content = resolve_markdown_images(content, post["path"].parent)

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post["path"].stem.lower())
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
