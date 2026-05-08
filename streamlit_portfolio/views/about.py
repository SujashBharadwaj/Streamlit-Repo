import streamlit as st
from utils.helpers import quick_links, ASSETS


def about_view():
    st.markdown("## About")
    st.markdown("")

    a1, a2 = st.columns([1, 2.2], gap="large")
    with a1:
        img_path = ASSETS / "img" / "profile.png"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

    with a2:
        st.markdown(
            """
            <div class="card">
              <div style="font-size: 1.5rem; font-weight: 900;">Hi, I'm Sujash.</div>
              <div class="muted" style="margin-top: 10px; font-size: 1.1rem;">
                I'm a final-year student at MIT-WPU (BSc(Hons) Applied Statistics &amp; Data Analytics) and in my diploma term
                for IITM BS in Data Science and Applications.
              </div>
              <div class="muted" style="margin-top: 10px; font-size: 1.1rem;">
                I'm 22 (born 10 Jan 2004). I like machine learning, AI, math, and statistics.
                I'm also self-studying bioinformatics and data science for biology.
              </div>
              <div class="muted" style="margin-top: 10px; font-size: 1.1rem;">
                Outside work: F1 and cricket fan, I go karting and play cricket when I can.
                I'm an avid music listener and still log hours on Age of Empires II DE.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        quick_links(
            email="sujashbharadwaj10@gmail.com",
            github_url="https://github.com/SujashBharadwaj",
            linkedin_url="https://www.linkedin.com/in/sujash-bharadwaj-14752827a/",
        )

    st.markdown("---")
    st.markdown("### Focus & Skills")
    st.markdown(
        """
        <div style="margin-top: 10px;">
          <span class="pill">Python</span><span class="pill">Pandas</span><span class="pill">FastAPI</span>
          <span class="pill">Scikit-learn</span><span class="pill">EDA &amp; Visualization</span>
          <span class="pill">ML Pipelines</span><span class="pill">Vector DB basics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
