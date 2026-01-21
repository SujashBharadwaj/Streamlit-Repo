# Homepage.py
import base64
import re
import random
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

# Try to use BeautifulSoup if available (for parsing your existing HTML projects index)
try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None  # type: ignore


# ---------------------------
# Config
# ---------------------------
st.set_page_config(
    page_title="Sujash Bharadwaj's Portfolio",
    layout="wide",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
POSTS_DIR = ROOT / "posts"
PROJECTS_DIR = ROOT / "projects_static"

# Marker heading that exists in your OEE MD and should be replaced by the interactive demo
OEE_MARKER = "## A simple OEE calculation snippet (Python)"


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
        font-family: 'Oswald', sans-serif !important;
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
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------
# Helpers
# ---------------------------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_posts() -> List[Dict]:
    posts: List[Dict] = []
    if POSTS_DIR.exists():
        for p in sorted(POSTS_DIR.glob("*.md"), reverse=True):
            text = read_text(p)
            title = None
            date_ = None
            tags: List[str] = []
            content = text

            # Simple frontmatter (optional)
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
    """
    Reads your existing HTML projects index if present:
    projects_static/index.html with <a class="tile"> ... </a>
    Falls back to scanning subfolders in projects_static/.
    """
    projects: List[Dict] = []
    idx = PROJECTS_DIR / "index.html"

    if idx.exists() and BeautifulSoup is not None:
        try:
            soup = BeautifulSoup(read_text(idx), "html.parser")
            for a in soup.select("a.tile"):
                title = a.find("h3").get_text(" ", strip=True) if a.find("h3") else "Project"
                desc = a.find("p").get_text(" ", strip=True) if a.find("p") else ""
                href = (a.get("href") or "").strip().strip("/")
                slug = href.split("/")[0] if href else ""
                if slug:
                    projects.append({"title": title, "desc": desc, "slug": slug})
        except Exception:
            projects = []

    if not projects and PROJECTS_DIR.exists():
        for p in sorted(PROJECTS_DIR.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                projects.append({"title": p.name, "desc": "", "slug": p.name})

    return projects


def list_project_files(slug: str) -> Tuple[List[Path], List[Path]]:
    pdir = PROJECTS_DIR / slug
    if not pdir.exists():
        return [], []
    pdfs = sorted(pdir.rglob("*.pdf"))
    others: List[Path] = []
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


def card(title: str, body: str, meta: str = "", extra_html: str = ""):
    st.markdown(
        f"""
        <div class="card">
          <div style="font-size: 1.35rem; font-weight: 800;">{title}</div>
          {"<div class='tiny' style='margin-top:4px;'>" + meta + "</div>" if meta else ""}
          <div class="muted" style="margin-top:10px; font-size: 1.05rem;">{body}</div>
          {extra_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def quick_links(email: str, github_url: str, linkedin_url: str):
    mailto = f"mailto:{email}"
    html = f"""
    <div style="display:flex; gap:12px; align-items:center; margin-top:10px;">

      <a href="{mailto}" target="_blank" rel="noopener noreferrer" title="Email"
         style="display:inline-flex; align-items:center; justify-content:center;
                width:42px; height:42px; border-radius:12px;
                border:1px solid rgba(229,231,235,.12);
                background: rgba(229,231,235,.06);
                box-shadow: 0 10px 30px rgba(0,0,0,.20);
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"
             style="fill: rgba(229,231,235,.92);">
          <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/>
        </svg>
      </a>

      <a href="{github_url}" target="_blank" rel="noopener noreferrer" title="GitHub"
         style="display:inline-flex; align-items:center; justify-content:center;
                width:42px; height:42px; border-radius:12px;
                border:1px solid rgba(229,231,235,.12);
                background: rgba(229,231,235,.06);
                box-shadow: 0 10px 30px rgba(0,0,0,.20);
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"
             style="fill: rgba(229,231,235,.92);">
          <path d="M12 .5C5.73.5.5 5.74.5 12.02c0 5.11 3.29 9.44 7.86 10.97.57.1.78-.25.78-.55v-2.05c-3.2.7-3.88-1.38-3.88-1.38-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.72-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .98-.31 3.2 1.18.93-.26 1.92-.39 2.91-.39.99 0 1.98.13 2.91.39 2.22-1.49 3.2-1.18 3.2-1.18.63 1.59.23 2.77.11 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.69 5.41-5.25 5.69.41.36.78 1.07.78 2.16v3.2c0 .31.21.66.79.55 4.56-1.53 7.85-5.86 7.85-10.97C23.5 5.74 18.27.5 12 .5z"/>
        </svg>
      </a>

      <a href="{linkedin_url}" target="_blank" rel="noopener noreferrer" title="LinkedIn"
         style="display:inline-flex; align-items:center; justify-content:center;
                width:42px; height:42px; border-radius:12px;
                border:1px solid rgba(229,231,235,.12);
                background: rgba(229,231,235,.06);
                box-shadow: 0 10px 30px rgba(0,0,0,.20);
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"
             style="fill: rgba(229,231,235,.92);">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.047c.476-.9 1.637-1.85 3.369-1.85 3.603 0 4.266 2.37 4.266 5.455v6.286zM5.337 7.433a2.067 2.067 0 1 1 0-4.134 2.067 2.067 0 0 1 0 4.134zM6.814 20.452H3.86V9h2.954v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.727v20.545C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.273V1.727C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      </a>

    </div>

    <script>
      const links = document.querySelectorAll('a');
      links.forEach(a => {{
        a.addEventListener('mouseenter', () => {{
          a.style.borderColor = 'rgba(163,230,53,.28)';
          a.style.transform = 'translateY(-1px)';
          const svg = a.querySelector('svg');
          if (svg) svg.style.fill = '#A3E635';
        }});
        a.addEventListener('mouseleave', () => {{
          a.style.borderColor = 'rgba(229,231,235,.12)';
          a.style.transform = 'translateY(0px)';
          const svg = a.querySelector('svg');
          if (svg) svg.style.fill = 'rgba(229,231,235,.92)';
        }});
      }});
    </script>
    """
    components.html(html, height=70)


def normalize_math(md_text: str) -> str:
    md_text = md_text.replace(r"\(", "$").replace(r"\)", "$")
    md_text = md_text.replace(r"\[", "$$").replace(r"\]", "$$")
    return md_text


def compute_oee(planned_time_sec: int, downtime_sec: int, total_count: int, good_count: int, ideal_cycle_time_sec: int) -> Dict[str, float]:
    run_time = planned_time_sec - downtime_sec
    if planned_time_sec <= 0 or run_time <= 0 or total_count <= 0 or good_count < 0:
        return {"availability": 0.0, "performance": 0.0, "quality": 0.0, "oee": 0.0}

    availability = run_time / planned_time_sec
    performance = (total_count * ideal_cycle_time_sec) / run_time
    quality = good_count / total_count

    availability = max(0.0, min(1.0, availability))
    performance = max(0.0, min(1.0, performance))
    quality = max(0.0, min(1.0, quality))

    oee = availability * performance * quality
    return {"availability": availability, "performance": performance, "quality": quality, "oee": oee}


def render_oee_interactive():
    st.markdown("## Interactive OEE calculation (click to run)")
    st.markdown(
        "<div class='muted'>This demo generates a realistic shift scenario, calculates OEE, and tells you what to fix first based on the biggest loss.</div>",
        unsafe_allow_html=True,
    )

    cA, cB = st.columns([1, 1])
    with cA:
        seed = st.number_input("Optional seed (repeat the same example)", min_value=0, max_value=999999, value=0, step=1)
    with cB:
        st.markdown("<div class='tiny'>Tip: set seed to 0 for fresh random outputs.</div>", unsafe_allow_html=True)

    run = st.button("Run randomized example", key="run_oee_demo")

    with st.expander("Show Python code"):
        st.code(
            """def compute_oee(planned_time_sec, downtime_sec, total_count, good_count, ideal_cycle_time_sec):
    run_time = planned_time_sec - downtime_sec
    availability = run_time / planned_time_sec
    performance  = (total_count * ideal_cycle_time_sec) / run_time
    quality      = good_count / total_count
    oee = availability * performance * quality
    return availability, performance, quality, oee
""",
            language="python",
        )

    if not run:
        st.markdown("<div class='oee-box tiny'>Click the button to generate inputs and see the output metrics + takeaway.</div>", unsafe_allow_html=True)
        return

    if seed != 0:
        random.seed(int(seed))

    planned_time_min = random.choice([420, 450, 480])      # 7h, 7.5h, 8h
    downtime_min = random.randint(15, 90)
    total_count = random.randint(700, 1600)
    scrap = random.randint(0, max(1, int(0.12 * total_count)))
    good_count = max(0, total_count - scrap)
    ideal_cycle_time_sec = random.choice([18, 20, 22, 24, 26])

    planned_time_sec = planned_time_min * 60
    downtime_sec = downtime_min * 60

    out = compute_oee(
        planned_time_sec=planned_time_sec,
        downtime_sec=downtime_sec,
        total_count=total_count,
        good_count=good_count,
        ideal_cycle_time_sec=ideal_cycle_time_sec,
    )

    st.markdown("### Inputs")
    st.write(
        {
            "planned_time_min": planned_time_min,
            "downtime_min": downtime_min,
            "total_count": total_count,
            "good_count": good_count,
            "ideal_cycle_time_sec": ideal_cycle_time_sec,
        }
    )

    st.markdown("### Outputs")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Availability", f"{out['availability']*100:.1f}%")
    c2.metric("Performance", f"{out['performance']*100:.1f}%")
    c3.metric("Quality", f"{out['quality']*100:.1f}%")
    c4.metric("OEE", f"{out['oee']*100:.1f}%")

    # Key takeaway generator based on biggest loss
    losses = {
        "Availability (downtime, setups, breakdowns)": 1 - out["availability"],
        "Performance (micro-stops, slow cycles, minor jams)": 1 - out["performance"],
        "Quality (scrap, rework, startup rejects)": 1 - out["quality"],
    }
    worst = max(losses, key=losses.get)
    worst_loss = losses[worst]

    st.markdown("### Key takeaway")
    if worst_loss < 0.04:
        st.success(
            "This run is fairly balanced. Biggest gains come from tightening measurement, standard work, and small continuous improvements."
        )
    else:
        if "Availability" in worst:
            st.info(
                "Availability is the main limiter. Reduce unplanned stops, improve changeovers, and shorten maintenance response time."
            )
        elif "Performance" in worst:
            st.info(
                "Performance is the main limiter. Hunt micro-stops and speed losses: feeding issues, small jams, slow cycles, and drift from the ideal."
            )
        else:
            st.info(
                "Quality is the main limiter. Focus on defect root causes, startup stability, process parameters, and catching issues earlier in the line."
            )

    st.markdown(
        f"<div class='tiny'>Biggest loss in this run: <b>{worst}</b> (approx. {(worst_loss*100):.1f}% loss)</div>",
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
st.sidebar.markdown('<div class="muted">Portfolio and personal blog</div>', unsafe_allow_html=True)
st.sidebar.markdown("")

current_index = PAGES.index(st.session_state["page"]) if st.session_state["page"] in PAGES else 0
page = st.sidebar.radio("Navigate", PAGES, index=current_index, label_visibility="collapsed")
st.session_state["page"] = page


# ---------------------------
# Pages
# ---------------------------
if st.session_state["page"] == "Home":
    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown(
            """
            <div style="margin-top: 6px;">
              <div style="font-size: clamp(2.1rem, 4vw, 3.2rem); font-weight: 900; line-height: 1.1;">
                Sujash Bharadwaj's Portfolio
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
                st.session_state["page"] = "Projects"
                st.rerun()
        with c2:
            if st.button("Read the blog", use_container_width=True):
                st.session_state["page"] = "Blog"
                st.rerun()

        st.markdown("")
        st.markdown("### Latest article")
        latest = posts[0] if posts else None
        if latest:
            card(latest["title"], latest["excerpt"], meta=latest["date"])
            if st.button("Open article", key="open_latest"):
                st.session_state["selected_post"] = str(latest["path"])
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
            """
            <span class="pill">AI & ML</span>
            <span class="pill">Statistics</span>
            <span class="pill">Reproducible notebooks</span>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="muted" style="margin-top:10px;">Hands-on mini projects, clean analysis, and short write-ups as I learn.</div>',
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

elif st.session_state["page"] == "Projects":
    st.markdown("## Projects")
    st.markdown('<div class="muted">Reports, dashboards, and longer experiments.</div>', unsafe_allow_html=True)
    st.markdown("")

    if not projects:
        st.info("No projects found.")
    else:
        titles = [p["title"] for p in projects]
        slug_by_title = {p["title"]: p["slug"] for p in projects}

        default_title = None
        if st.session_state["selected_project"]:
            for p in projects:
                if p["slug"] == st.session_state["selected_project"]:
                    default_title = p["title"]
                    break

        idx = titles.index(default_title) if (default_title in titles) else 0
        selected_title = st.selectbox("Select a project", titles, index=idx)

        slug = slug_by_title[selected_title]
        st.session_state["selected_project"] = slug

        desc = next((p["desc"] for p in projects if p["slug"] == slug), "")
        if desc:
            st.markdown(f'<div class="muted">{desc}</div>', unsafe_allow_html=True)
            st.markdown("")

        pdfs, others = list_project_files(slug)

        cols = st.columns([1.4, 1], gap="large")
        with cols[0]:
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

elif st.session_state["page"] == "Blog":
    st.markdown("## Blog")
    st.markdown('<div class="muted">Short learning notes and project logs.</div>', unsafe_allow_html=True)
    st.markdown("")

    if not posts:
        st.info("No posts found yet.")
    else:
        q = st.text_input("Search posts", placeholder="Type to search by title or content…")
        filtered = posts
        if q.strip():
            qq = q.strip().lower()
            filtered = [p for p in posts if qq in p["title"].lower() or qq in p["content"].lower()]

        if not filtered:
            st.info("No posts match your search.")
        else:
            post_titles = [p["title"] for p in filtered]

            default_idx = 0
            if st.session_state["selected_post"]:
                for i, p in enumerate(filtered):
                    if str(p["path"]) == st.session_state["selected_post"]:
                        default_idx = i
                        break

            selected = st.selectbox("Select a post", post_titles, index=default_idx)
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
                meta_bits.append(" • ".join([f"`{t}`" for t in post["tags"]]))
            if meta_bits:
                st.markdown(f"<div class='tiny'>{' | '.join(meta_bits)}</div>", unsafe_allow_html=True)

            st.markdown("---")

            content = normalize_math(post["content"])

            # Replace the snippet section with interactive demo for OEE post
            if is_oee_post and OEE_MARKER in content:
                before, after = content.split(OEE_MARKER, 1)
                st.markdown(before, unsafe_allow_html=True)
                st.markdown("---")
                render_oee_interactive()

                # remove the old fenced python block if it immediately follows the marker in "after"
                # (so the old snippet doesn't show under the demo)
                after_clean = re.sub(r"^\s*```python[\s\S]*?```\s*", "", after, count=1).lstrip()
                st.markdown("---")
                st.markdown(after_clean, unsafe_allow_html=True)
            else:
                # normal rendering for all other posts
                st.markdown(content, unsafe_allow_html=True)

elif st.session_state["page"] == "About":
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

        quick_links(
            email="sujashbharadwaj10@gmail.com",
            github_url="https://github.com/SujashBharadwaj",
            linkedin_url="https://www.linkedin.com/in/sujash-bharadwaj-14752827a/",
        )
