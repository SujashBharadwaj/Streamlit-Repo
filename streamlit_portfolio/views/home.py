import streamlit as st
from utils.helpers import card, quick_links, sanitize_html, ASSETS


def home_view(posts, projects):
    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown(
            sanitize_html("""
            <div style="margin-top: 6px;">
              <div style="font-size: clamp(2.1rem, 4vw, 3.2rem); font-weight: 900; line-height: 1.1;">
                Sujash Bharadwaj's Portfolio
              </div>
              <div class="muted" style="margin-top: 10px; font-size: 1.25rem;">
                Software Engineer at sfhawk Solutions. BSc(Hons) Applied Statistics &amp; Data Analytics (MIT-WPU) + IITM BS (Data Science &amp; Applications).
                I build practical projects, write what I learn, and keep things reproducible.
              </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 1], gap="small")
        with c1:
            if st.button("Explore projects", use_container_width=True, key="home_explore_projects"):
                st.session_state["page"] = "Projects"
                st.rerun()
        with c2:
            if st.button("Read the blog", use_container_width=True, key="home_read_blog"):
                st.session_state["page"] = "Blog"
                st.rerun()

        st.markdown("")
        st.markdown("### Latest article")
        latest = posts[0] if posts else None
        if latest:
            card(latest["title"], latest["excerpt"], meta=latest["date"])
            if st.button("Open article", key="open_latest"):
                st.session_state["selected_post"] = latest["path"]
                st.session_state["page"] = "Blog"
                st.rerun()
        else:
            st.info("No blog posts found yet.")

        st.markdown("### Latest project")
        if projects:
            card(projects[0]["title"], projects[0]["desc"])
            if st.button("Open project", key="open_latest_project"):
                st.session_state["selected_project"] = projects[0]["slug"]
                st.session_state["page"] = "Projects"
                st.rerun()
        else:
            st.info("No projects found yet.")

        st.markdown("### What I'm doing now")
        st.markdown(
            sanitize_html("""
            <span class="pill">Computer Vision</span>
            <span class="pill">SLM &amp; VLM</span>
            <span class="pill">AI &amp; ML</span>
            <span class="pill">.NET &amp; Angular</span>
            <span class="pill">React</span>
            <span class="pill">Statistics</span>
            <span class="pill">Reproducible notebooks</span>
            """),
            unsafe_allow_html=True,
        )
        st.markdown(
            sanitize_html('<div class="muted" style="margin-top:10px;">Building production systems, exploring vision &amp; language models, and writing about what I learn along the way.</div>'),
            unsafe_allow_html=True,
        )

    with right:
        img_path = ASSETS / "img" / "profile.png"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

        quick_links(
            email="sujashbharadwaj10@gmail.com",
            github_url="https://github.com/SujashBharadwaj",
            linkedin_url="https://www.linkedin.com/in/sujash-bharadwaj-14752827a/",
        )
