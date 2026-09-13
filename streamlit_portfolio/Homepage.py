# Homepage.py — Entry point & router
import streamlit as st
from PIL import Image
from utils.helpers import load_posts, load_projects, sanitize_html
from views.home import home_view
from views.projects import projects_view
from views.blog import blog_view
from views.about import about_view

# ---------------------------
# Config
# ---------------------------
from pathlib import Path as _Path
_favicon = Image.open(_Path(__file__).parent / "assets" / "css" / "favicon.png")
st.set_page_config(
    page_title="Sujash Bharadwaj | Software & ML Engineer",
    page_icon=_favicon,
    layout="wide",
)

# ---------------------------
# Theme + fonts (Crimson Text + Oswald) + UI polish
# ---------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Oswald:wght@400;600;700&display=swap');

      :root{
        --bg:#071A14;
        --surface:#0B1411;
        --card:#0E1F18;
        --text:#E5E7EB;
        --muted:rgba(229,231,235,.78);
        --border:rgba(229,231,235,.10);
        --primary:#10B981;
        --primary2:#34D399;
        --accent:#A3E635;
        --shadow:0 10px 30px rgba(0,0,0,.45);
      }

      html, body, [class*="css"]  {
        font-family: 'Crimson Text', serif !important;
        color: var(--text) !important;
      }

      h1, h2, h3, h4, h5, h6,
      .stRadio label, .stButton button, .stDownloadButton button,
      [data-testid="stSidebar"] * {
        font-family: 'Copperplate Gothic', 'Copperplate', 'Oswald', sans-serif !important;
        letter-spacing: 0.2px;
      }

      .block-container { padding-top: 1.8rem; max-width: 1120px; }
      .stApp { background: var(--bg); }

      a { color: var(--accent) !important; text-decoration: none; }
      a:hover { text-decoration: underline; }

      .card {
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(14,31,24,.98), rgba(11,20,17,.98));
        padding: 18px 18px;
        border-radius: 16px;
        box-shadow: var(--shadow);
        margin-bottom: 14px;
      }
      .card:hover { border-color: rgba(163,230,53,.22); }

      .muted { color: var(--muted); }
      .tiny { color: rgba(229,231,235,.70); font-size: 0.95rem; }

      .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid rgba(229,231,235,.12);
        background: rgba(229,231,235,.06);
        margin-right: 6px;
        margin-top: 6px;
        font-size: 0.95rem;
      }

      .stButton button, .stDownloadButton button {
        border-radius: 12px !important;
        border: 1px solid rgba(229,231,235,.14) !important;
        background: rgba(229,231,235,.06) !important;
        color: rgba(229,231,235,.92) !important;
      }
      .stButton button:hover, .stDownloadButton button:hover {
        border-color: rgba(163,230,53,.28) !important;
        color: var(--accent) !important;
        transform: translateY(-1px);
      }

      [data-testid="stSidebar"] {
        background: rgba(11,20,17,.92);
        border-right: 1px solid rgba(229,231,235,.10);
      }
      [data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

      p, li { font-size: 1.08rem; line-height: 1.7; }
      code { background: rgba(229,231,235,.06) !important; }

      .oee-box{
        border:1px solid rgba(229,231,235,.10);
        background: rgba(229,231,235,.04);
        border-radius: 14px;
        padding: 14px 14px;
        margin-top: 10px;
      }

      .project-card{
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(14,31,24,.98), rgba(11,20,17,.98));
        border-radius: 16px;
        padding: 14px 16px;
        min-height: 160px;
        margin-bottom: 8px;
      }

      .project-eyebrow{
        color: rgba(163,230,53,.92);
        font-size: .88rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin-bottom: 4px;
      }

      .project-title{
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 6px;
      }

      .project-chips{ margin-top: 10px; }

      .project-chip{
        display: inline-block;
        padding: 2px 8px;
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 999px;
        border: 1px solid rgba(229,231,235,.16);
        background: rgba(229,231,235,.05);
        font-size: .82rem;
      }

      @media (max-width: 900px){
        .block-container{
          padding-top: 1.15rem !important;
          padding-left: 0.9rem !important;
          padding-right: 0.9rem !important;
        }
        h1{ font-size: 1.9rem !important; line-height: 1.15 !important; }
        h2{ font-size: 1.5rem !important; line-height: 1.2 !important; }
        h3{ font-size: 1.2rem !important; line-height: 1.25 !important; }
        p, li{ font-size: 1rem !important; line-height: 1.55 !important; }
        .card{ padding: 14px 14px; border-radius: 14px; margin-bottom: 10px; }
        .project-card{ min-height: 0; padding: 12px 12px; border-radius: 14px; }
        .project-title{ font-size: 1.12rem; line-height: 1.25; }
        .project-chip{ font-size: .76rem; padding: 2px 7px; margin-right: 5px; margin-bottom: 5px; }
        .stButton button, .stDownloadButton button{
          min-height: 2.55rem !important;
          padding: 0.45rem 0.7rem !important;
          font-size: 0.95rem !important;
        }
        [data-testid="stMetricValue"]{ font-size: 1.3rem !important; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Data
# ---------------------------
posts = load_posts()
projects = load_projects()

# ---------------------------
# Navigation state
# ---------------------------
PAGES = ["Home", "Projects", "Blog", "About"]
if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "selected_post" not in st.session_state:
    st.session_state["selected_post"] = ""
if "selected_project" not in st.session_state:
    st.session_state["selected_project"] = ""

st.sidebar.markdown("## Sujash Bharadwaj")
st.sidebar.markdown(sanitize_html('<div class="muted">Portfolio and personal blog</div>'), unsafe_allow_html=True)
st.sidebar.markdown(
    sanitize_html('<div style="margin-top:6px;"><span style="display:inline-block; padding:2px 10px; border-radius:999px; border:1px solid rgba(16,185,129,.35); background:rgba(16,185,129,.10); font-size:0.82rem; color:#34D399; letter-spacing:0.04em;">v2.2.0</span></div>'),
    unsafe_allow_html=True,
)
st.sidebar.markdown("")

current_index = PAGES.index(st.session_state["page"]) if st.session_state["page"] in PAGES else 0
page = st.sidebar.radio("Navigate", PAGES, index=current_index, label_visibility="collapsed")
st.session_state["page"] = page

# ---------------------------
# Router
# ---------------------------
if page == "Home":
    home_view(posts, projects)
elif page == "Projects":
    projects_view()
elif page == "Blog":
    blog_view(posts)
elif page == "About":
    about_view()
