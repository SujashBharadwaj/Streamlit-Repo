import base64
import re
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st
from bs4 import BeautifulSoup
from markdownify import markdownify as mdify

# ---------------------------
# Config
# ---------------------------
st.set_page_config(
    page_title="Sujash Bharadwaj",
    layout="wide",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
POSTS_DIR = ROOT / "posts"
BLOG_HTML_DIR = ROOT / "blog_static"
PROJECTS_DIR = ROOT / "projects_static"

# ---------------------------
# Theme + fonts (Crimson Text + Oswald)
# ---------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Oswald:wght@400;600;700&display=swap');

      /* Base */
      html, body, [class*="css"]  {
        font-family: 'Crimson Text', serif !important;
      }

      /* Headings / nav */
      h1, h2, h3, h4, h5, h6,
      .stRadio label, .stButton button, .stDownloadButton button {
        font-family: 'Oswald', sans-serif !important;
        letter-spacing: 0.2px;
      }

      /* Layout */
      .block-container { padding-top: 1.8rem; max-width: 1120px; }

      /* Links */
      a { color: #A3E635 !important; text-decoration: none; }
      a:hover { text-decoration: underline; }

      /* Cards */
      .card {
        border: 1px solid rgba(229,231,235,.10);
        background: linear-gradient(180deg, rgba(14,31,24,.98), rgba(11,20,17,.98));
        padding: 18px 18px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,.45);
        margin-bottom: 14px;
      }
      .card:hover { border-color: rgba(163,230,53,.22); }

      .muted { color: rgba(229,231,235,.78); }
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

      /* Buttons */
      .stButton button, .stDownloadButton button {
        border-radius: 12px !important;
        border: 1px solid rgba(229,231,235,.14) !important;
      }

      /* Sidebar */
      [data-testid="stSidebar"] {
        background: rgba(11,20,17,.92);
        border-right: 1px solid rgba(229,231,235,.10);
      }
      [data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Helpers
# ---------------------------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def html_main_to_markdown(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    main = soup.find("main") or soup.body or soup
    for tag in main.select("header, nav, footer, script, style"):
        tag.decompose()
    md = mdify(str(main), heading_style="ATX")
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return md

def load_posts() -> List[Dict]:
    posts = []
    if POSTS_DIR.exists():
        for p in sorted(POSTS_DIR.glob("*.md"), reverse=True):
            text = read_text(p)
            title = None
            date_ = None
            tags = []
            content = text

            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = parts[1].strip()
                    content = parts[2].lstrip()
                    for line in fm.splitlines():
                        if ":" not in line:
                            continue
                        k, v = line.split(":", 1)
                        k = k.strip().lower()
                        v = v.strip()
                        if k == "title":
                            title = v
                        elif k == "date":
                            date_ = v
                        elif k == "tags":
                            tags = [t.strip() for t in v.split(",") if t.strip()]

            title = title or p.stem.replace("-", " ").title()
            excerpt = re.sub(r"\s+", " ", content.strip())
            excerpt = excerpt[:190] + ("..." if len(excerpt) > 190 else "")
            posts.append(
                {"title": title, "date": date_ or "", "tags": tags, "path": p, "content": content, "excerpt": excerpt}
            )
    return posts

def load_projects() -> List[Dict]:
    # Use the original HTML index (if available) to keep your existing project titles/descriptions
    idx = PROJECTS_DIR / "index.html"
    projects = []
    if idx.exists():
        soup = BeautifulSoup(read_text(idx), "html.parser")
        for a in soup.select("a.tile"):
            title = a.find("h3").get_text(" ", strip=True) if a.find("h3") else "Project"
            desc = a.find("p").get_text(" ", strip=True) if a.find("p") else ""
            href = (a.get("href") or "").strip().strip("/")
            slug = href.split("/")[0] if href else ""
            projects.append({"title": title, "desc": desc, "slug": slug})
    else:
        # Fallback: scan folders
        for p in sorted(PROJECTS_DIR.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                projects.append({"title": p.name, "desc": "", "slug": p.name})
    return projects

def list_project_files(slug: str) -> Tuple[List[Path], List[Path]]:
    pdir = PROJECTS_DIR / slug
    pdfs = sorted(pdir.rglob("*.pdf"))
    others = []
    for ext in ("*.xlsx", "*.csv", "*.png", "*.jpg", "*.jpeg"):
        others.extend(pdir.rglob(ext))
    others = sorted([p for p in others if p.suffix.lower() != ".pdf"])
    return pdfs, others

def embed_pdf(pdf_path: Path, height: int = 860):
    data = pdf_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    html = f"""
    <iframe
      src="data:application/pdf;base64,{b64}"
      width="100%"
      height="{height}"
      style="border:1px solid rgba(229,231,235,.10); border-radius: 14px; background: rgba(11,20,17,.60);"
      type="application/pdf"
    ></iframe>
    """
    st.markdown(html, unsafe_allow_html=True)

def card(title: str, body: str, meta: str = ""):
    st.markdown(
        f"""
        <div class="card">
          <div style="font-size: 1.35rem; font-weight: 700;">{title}</div>
          {"<div class='tiny' style='margin-top:4px;'>" + meta + "</div>" if meta else ""}
          <div class="muted" style="margin-top:10px; font-size: 1.05rem;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------
# Data
# ---------------------------
posts = load_posts()
projects = load_projects()

# ---------------------------
# Sidebar nav
# ---------------------------
st.sidebar.markdown("## Sujash Bharadwaj")
st.sidebar.markdown('<div class="muted">Portfolio and personal blog</div>', unsafe_allow_html=True)
st.sidebar.markdown("")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Projects", "Blog", "About"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Theme**: Forest + Lime")
st.sidebar.markdown('<div class="tiny">Primary font: Crimson Text<br/>Secondary font: Oswald</div>', unsafe_allow_html=True)

# ---------------------------
# Pages
# ---------------------------
if page == "Home":
    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown(
            """
            <div style="margin-top: 6px;">
              <div style="font-size: clamp(2.1rem, 4vw, 3.2rem); font-weight: 800; line-height: 1.1;">
                Learning with Sujash
              </div>
              <div class="muted" style="margin-top: 10px; font-size: 1.25rem;">
                Final-year BSc(Hons) Applied Statistics & Data Analytics (MIT-WPU) + IITM BS (Data Science & Applications).
                I build practical projects, write what I learn, and keep things reproducible.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 1], gap="small")
        with c1:
            if st.button("Explore projects", use_container_width=True):
                st.session_state["nav_override"] = "Projects"
        with c2:
            if st.button("Read the blog", use_container_width=True):
                st.session_state["nav_override"] = "Blog"

        st.markdown("")

        st.markdown("### Latest article")
        # Pick most recent by date if available
        latest = posts[0] if posts else None
        if latest:
            card(latest["title"], latest["excerpt"], meta=latest["date"])
            if st.button("Open article", key="open_latest"):
                st.session_state["selected_post"] = str(latest["path"])
                st.session_state["nav_override"] = "Blog"
        else:
            st.info("No blog posts found yet.")

        st.markdown("### Latest project")
        if projects:
            card(projects[0]["title"], projects[0]["desc"])
            if st.button("Open project", key="open_latest_project"):
                st.session_state["selected_project"] = projects[0]["slug"]
                st.session_state["nav_override"] = "Projects"
        else:
            st.info("No projects found yet.")

        st.markdown("### What I'm doing now")
        st.markdown(
            """
            <span class="pill">AI & ML</span>
            <span class="pill">Statistics</span>
            <span class="pill">Bioinformatics</span>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="muted" style="margin-top:10px;">Hands-on mini projects, clean analysis, and small write-ups as I learn.</div>',
            unsafe_allow_html=True,
        )

    with right:
        img_path = ASSETS / "img" / "profile.png"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        st.markdown("### Quick links")
        st.markdown("- Email: sujashbharadwaj10@gmail.com")
        st.markdown("- GitHub: SujashBharadwaj")
        st.markdown("- LinkedIn: sujash-bharadwaj-14752827a")
        st.markdown("")
        st.markdown('<div class="tiny">If you want this as a single landing page with sections (instead of sidebar nav), tell me and I’ll switch it.</div>', unsafe_allow_html=True)

    # Navigation override from buttons
    if st.session_state.get("nav_override"):
        st.session_state["page_override"] = st.session_state["nav_override"]
        st.session_state["nav_override"] = None
        st.rerun()

elif page == "Projects" or st.session_state.get("page_override") == "Projects":
    st.session_state["page_override"] = None
    st.markdown("## Projects")
    st.markdown('<div class="muted">Reports, dashboards, and longer experiments.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Choose project
    titles = [p["title"] for p in projects] if projects else []
    slug_by_title = {p["title"]: p["slug"] for p in projects}

    default_slug = st.session_state.get("selected_project")
    default_title = None
    if default_slug:
        for p in projects:
            if p["slug"] == default_slug:
                default_title = p["title"]
                break

    selected_title = st.selectbox("Select a project", titles, index=titles.index(default_title) if default_title in titles else 0) if titles else None

    if not selected_title:
        st.info("No projects found.")
    else:
        slug = slug_by_title[selected_title]
        st.session_state["selected_project"] = slug

        # Description from projects list
        desc = next((p["desc"] for p in projects if p["slug"] == slug), "")
        if desc:
            st.markdown(f'<div class="muted">{desc}</div>', unsafe_allow_html=True)
            st.markdown("")

        pdfs, others = list_project_files(slug)

        cols = st.columns([1.4, 1], gap="large")
        with cols[0]:
            # show embedded PDF picker if exists
            if pdfs:
                pdf_names = [p.name for p in pdfs]
                chosen = st.selectbox("View report", pdf_names, index=0)
                chosen_path = next(p for p in pdfs if p.name == chosen)
                embed_pdf(chosen_path, height=860)
            else:
                st.info("No PDF found for this project.")

        with cols[1]:
            st.markdown("### Downloads")
            if pdfs:
                for p in pdfs:
                    st.download_button(
                        label=f"Download {p.name}",
                        data=p.read_bytes(),
                        file_name=p.name,
                        mime="application/pdf",
                        use_container_width=True,
                    )
            if others:
                st.markdown("### Data / assets")
                for p in others:
                    mime = "application/octet-stream"
                    if p.suffix.lower() == ".xlsx":
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    elif p.suffix.lower() == ".csv":
                        mime = "text/csv"
                    elif p.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                        mime = f"image/{p.suffix.lower().lstrip('.')}"
                    st.download_button(
                        label=f"Download {p.name}",
                        data=p.read_bytes(),
                        file_name=p.name,
                        mime=mime,
                        use_container_width=True,
                    )

            st.markdown("### Notes")
            st.markdown(
                '<div class="tiny">If you want each project to have a full case-study page (problem → approach → results → takeaways), I can convert your existing HTML project pages into Streamlit layouts.</div>',
                unsafe_allow_html=True,
            )

elif page == "Blog" or st.session_state.get("page_override") == "Blog":
    st.session_state["page_override"] = None
    st.markdown("## Blog")
    st.markdown('<div class="muted">Short learning notes and project logs.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Filters
    q = st.text_input("Search posts", placeholder="Type to search by title or content…")
    filtered = posts
    if q.strip():
        qq = q.strip().lower()
        filtered = [p for p in posts if qq in p["title"].lower() or qq in p["content"].lower()]

    # Select post
    post_titles = [p["title"] for p in filtered]
    default_path = st.session_state.get("selected_post")
    default_idx = 0
    if default_path:
        for i, p in enumerate(filtered):
            if str(p["path"]) == default_path:
                default_idx = i
                break

    if not filtered:
        st.info("No posts match your search.")
    else:
        selected = st.selectbox("Select a post", post_titles, index=default_idx)
        post = next(p for p in filtered if p["title"] == selected)
        st.session_state["selected_post"] = str(post["path"])

        st.markdown(f"### {post['title']}")
        if post["date"]:
            st.markdown(f"<div class='tiny'>{post['date']}</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(post["content"])

elif page == "About":
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
              <div style="font-size: 1.5rem; font-weight: 800;">Hi, I'm Sujash.</div>
              <div class="muted" style="margin-top: 10px; font-size: 1.1rem;">
                I'm a final-year student at MIT-WPU (BSc(Hons) Applied Statistics & Data Analytics) and in my diploma term
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

        st.markdown("### Contact")
        st.markdown("- Email: sujashbharadwaj10@gmail.com")
        st.markdown("- GitHub: SujashBharadwaj")
        st.markdown("- LinkedIn: https://www.linkedin.com/in/sujash-bharadwaj-14752827a/")

    st.markdown("---")
    st.markdown("### Quick customization checklist (tell me what you want)")
    st.markdown(
        """
        - What roles are you targeting right now (Data Analyst / BI / Data Science / Customer Success Analytics)?
        - Do you want the homepage to be minimal (1-screen hero) or content-heavy (tiles + highlights)?
        - Should we add a proper 'Resume' section with a PDF and a one-page summary?
        """
    )
