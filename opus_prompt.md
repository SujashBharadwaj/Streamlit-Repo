# Prompt for Claude Opus: Restructure & Modularize Streamlit Portfolio

You can copy and paste the entire content of this prompt into Claude Opus. It contains everything needed to refactor the monolithic portfolio into a state-of-the-art, modular Streamlit application.

---

```text
You are an expert software architect and Streamlit engineer. Your task is to perform a complete, clean refactoring, cleanup, and visual enhancement of a Streamlit portfolio website.

Currently, the portfolio has a monolithic 1,157-line `Homepage.py` that handles navigation, global styling, helper utilities, loading and parsing of Markdown blogs and legacy HTML projects (using BeautifulSoup on a static HTML index file), and three complex interactive play-ground dashboards.

Your goal is to split this monolithic file into a clean, modular, and highly maintainable directory structure, replacing the fragile HTML-parsing project system with a robust JSON configuration, fixing broken markdown images by resolving them to base64, and rendering projects using clean, native Streamlit layout views.

---

### 1. Target Directory Structure
Refactor the app to use this exact directory layout inside `streamlit_portfolio/`:

streamlit_portfolio/
├── .streamlit/
│   └── config.toml          # Custom dark-theme settings (Keep existing)
├── assets/                  # Existing static assets (images, etc.)
│   └── img/                 # Image assets (profile.png, cauchy.png, etc.)
├── posts/                   # Blog posts (.md files with YAML frontmatter)
├── projects_static/         # Project reports, data, and mini-games
├── projects.json            # [NEW] Project metadata file
├── Homepage.py              # [REWRITTEN] High-level routing & layout entry point
├── utils/
│   ├── __init__.py
│   └── helpers.py           # [NEW] Core utilities (file I/O, base64 images, dynamic loaders)
├── components/
│   ├── __init__.py
│   ├── means.py             # [NEW] Interactive Means dashboard
│   ├── gradient_descent.py  # [NEW] Interactive Gradient Descent dashboard
│   └── oee.py               # [NEW] Interactive OEE calculator dashboard
└── views/
    ├── __init__.py
    ├── home.py              # [NEW] Bio, social cards, latest activity view
    ├── projects.py          # [NEW] Modern projects grid & native PDF/Sheets details
    ├── blog.py              # [NEW] Blog post search & mathematical renderer
    └── about.py             # [NEW] Profile detailed view & skills matrix

---

### 2. Precise File Specifications & Code Architectures

You must write the code for each of the new/modified files as specified below.

#### File A: `projects.json`
Create a structured JSON database for all portfolio projects.
Path: `streamlit_portfolio/projects.json`
```json
[
  {
    "slug": "wall-jump-maze",
    "title": "Wall Jump Maze Runner",
    "desc": "Pac-Man-inspired interactive portfolio mini game built in Canvas, with pellet collection, ghost collision, and a timed wall-jump ability.",
    "eyebrow": "Interactive Mini Game",
    "tags": ["Canvas API", "JavaScript", "Game Logic", "Streamlit Embed"],
    "type": "game",
    "html_file": "index.html"
  },
  {
    "slug": "EnergyEquitiesMI",
    "title": "Energy Equities MI Reporting",
    "desc": "Dataset generation, exception monitoring, and MI-style reporting for 10 NSE energy companies.",
    "eyebrow": "Operations + Reporting",
    "tags": ["Google Sheets", "MI Reporting", "Data QA", "Process Documentation"],
    "type": "embed",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1M6gXq5Dq1Al95RO6OqCx3ZyLTTeW2uLR7vi1UGiqBWk/edit?usp=sharing",
    "pdf_file": "Process_Report.pdf"
  },
  {
    "slug": "commodity-equity-linkages",
    "title": "Commodity-Equity Linkages",
    "desc": "Global commodities vs Nifty 50 with timing, causality, rolling betas, and a ranked indicator dashboard. Embedded full report.",
    "eyebrow": "Market Analysis",
    "tags": ["Econometrics", "Rolling Betas", "Causality Tests", "Nifty 50"],
    "type": "report",
    "pdf_file": "final_report.pdf"
  },
  {
    "slug": "BDMcapstone",
    "title": "IITM BDM Capstone",
    "desc": "Client segmentation and retention analysis for Raftaar. Proposal, midterm, final, and presentation embedded on one page.",
    "eyebrow": "Capstone Study",
    "tags": ["Customer Analytics", "Retention", "Business Research", "Presentation"],
    "type": "multi_report",
    "pdfs": [
      {"name": "proposal.pdf", "label": "Proposal"},
      {"name": "midterm.pdf", "label": "Midterm"},
      {"name": "final.pdf", "label": "Final"},
      {"name": "presentation.pdf", "label": "Presentation"}
    ]
  }
]
```

#### File B: `utils/helpers.py`
Implement all loading, parsing, math formatting, base64-encoding, and card rendering utilities.
Path: `streamlit_portfolio/utils/helpers.py`
```python
import base64
import re
import streamlit as st
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
PROJECTS_DIR = ROOT / "projects_static"

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
            posts.append({
                "title": title,
                "date": date_ or "",
                "tags": tags,
                "path": p,
                "content": content,
                "excerpt": excerpt
            })
    return posts

def load_projects() -> List[Dict]:
    import json
    json_path = ROOT / "projects.json"
    if json_path.exists():
        try:
            return json.loads(read_text(json_path))
        except Exception:
            pass
    # Fallback scanning
    projects = []
    if PROJECTS_DIR.exists():
        for p in sorted(PROJECTS_DIR.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                projects.append({
                    "slug": p.name,
                    "title": p.name.replace("-", " ").title(),
                    "desc": "Portfolio project folder assets.",
                    "eyebrow": "Project",
                    "tags": ["Asset-Folder"],
                    "type": "report"
                })
    return projects

def list_project_files(slug: str) -> Tuple[List[Path], List[Path]]:
    pdir = PROJECTS_DIR / slug
    if not pdir.exists():
        return [], []
    pdfs = sorted(pdir.rglob("*.pdf"))
    others = []
    for ext in ("*.xlsx", "*.csv", "*.png", "*.jpg", "*.jpeg"):
        others.extend(pdir.rglob(ext))
    others = sorted([p for p in others if p.suffix.lower() != ".pdf"])
    return pdfs, others

def read_project_embed_html(slug: str, html_file: str = "index.html") -> str:
    path = PROJECTS_DIR / slug / html_file
    if path.exists():
        return read_text(path)
    return ""

def embed_pdf(pdf_path: Path, height: int = 860, mode: str = "Native Streamlit PDF"):
    data = pdf_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    if mode == "Native Streamlit PDF":
        try:
            st.pdf(data, width="stretch")
            return
        except TypeError:
            try:
                st.pdf(data)
                return
            except Exception:
                pass

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

def resolve_markdown_images(content: str, base_dir: Path) -> str:
    # Resolves Markdown images like `![alt](../assets/img/cauchy.png)` to Base64
    def replacer(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        full_path = (base_dir / rel_path).resolve()
        if not full_path.exists():
            # Try workspace absolute lookup as fallback
            full_path = (ROOT / rel_path.replace("../", "")).resolve()
            if not full_path.exists():
                full_path = (ROOT / "assets" / "img" / Path(rel_path).name).resolve()

        if full_path.exists() and full_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
            mime_type = f"image/{full_path.suffix.lower().lstrip('.')}"
            img_data = base64.b64encode(full_path.read_bytes()).decode("utf-8")
            return f'![{alt_text}](data:{mime_type};base64,{img_data})'
        return match.group(0)

    # Match `![alt_text](path)`
    return re.sub(r'!\[(.*?)\]\((.*?)\)', replacer, content)

def normalize_math(md_text: str) -> str:
    md_text = md_text.replace(r"\(", "$").replace(r"\)", "$")
    md_text = md_text.replace(r"\[", "$$").replace(r"\]", "$$")
    return md_text

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
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" style="fill: rgba(229,231,235,.92);">
          <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/>
        </svg>
      </a>
      <a href="{github_url}" target="_blank" rel="noopener noreferrer" title="GitHub"
         style="display:inline-flex; align-items:center; justify-content:center;
                width:42px; height:42px; border-radius:12px;
                border:1px solid rgba(229,231,235,.12);
                background: rgba(229,231,235,.06);
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" style="fill: rgba(229,231,235,.92);">
          <path d="M12 .5C5.73.5.5 5.74.5 12.02c0 5.11 3.29 9.44 7.86 10.97.57.1.78-.25.78-.55v-2.05c-3.2.7-3.88-1.38-3.88-1.38-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.72-1.55-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .98-.31 3.2 1.18.93-.26 1.92-.39 2.91-.39.99 0 1.98.13 2.91.39 2.22-1.49 3.2-1.18 3.2-1.18.63 1.59.23 2.77.11 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.69 5.41-5.25 5.69.41.36.78 1.07.78 2.16v3.2c0 .31.21.66.79.55 4.56-1.53 7.85-5.86 7.85-10.97C23.5 5.74 18.27.5 12 .5z"/>
        </svg>
      </a>
      <a href="{linkedin_url}" target="_blank" rel="noopener noreferrer" title="LinkedIn"
         style="display:inline-flex; align-items:center; justify-content:center;
                width:42px; height:42px; border-radius:12px;
                border:1px solid rgba(229,231,235,.12);
                background: rgba(229,231,235,.06);
                text-decoration:none; transition: transform .12s ease;">
        <svg width="22" height="22" viewBox="0 0 24 24" style="fill: rgba(229,231,235,.92);">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.047c.476-.9 1.637-1.85 3.369-1.85 3.603 0 4.266 2.37 4.266 5.455v6.286zM5.337 7.433a2.067 2.067 0 1 1 0-4.134 2.067 2.067 0 0 1 0 4.134zM6.814 20.452H3.86V9h2.954v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.727v20.545C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.273V1.727C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      </a>
    </div>
    """
    st.components.v1.html(html, height=70)
```

#### File C: `components/means.py`
Path: `streamlit_portfolio/components/means.py`
Move `compute_means_bundle()` and `render_means_interactive()` here. Ensure all references use standard Streamlit inputs (`st.text_area`, `st.text_input`, `st.slider`, `st.multiselect`, `st.table`, `st.bar_chart`) with distinct keys to prevent session collisions. Include the math support limits.

#### File D: `components/gradient_descent.py`
Path: `streamlit_portfolio/components/gradient_descent.py`
Move the 1D cubic gradient descent calculator and `render_gradient_descent_interactive()` here. Ensure standard math calculations for $f(x)$ and $f'(x)$ are modular and clean, rendering via `st.dataframe` and `st.line_chart` dynamically.

#### File E: `components/oee.py`
Path: `streamlit_portfolio/components/oee.py`
Move `compute_oee()` and `render_oee_interactive()` here. Keep the randomized inputs, metrics, loss calculations, expandable code blocks, and the dynamic key takeaway messaging intact.

#### File F: `views/home.py`
Path: `streamlit_portfolio/views/home.py`
```python
import streamlit as st
from pathlib import Path
from utils.helpers import card, quick_links, ROOT, ASSETS

def home_view(posts, projects):
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
            if st.button("Explore projects", use_container_width=True, key="home_btn_projects"):
                st.session_state["page"] = "Projects"
                st.rerun()
        with c2:
            if st.button("Read the blog", use_container_width=True, key="home_btn_blog"):
                st.session_state["page"] = "Blog"
                st.rerun()

        st.markdown("")
        st.markdown("### Latest article")
        latest = posts[0] if posts else None
        if latest:
            card(latest["title"], latest["excerpt"], meta=latest["date"])
            if st.button("Open article", key="open_latest_home", use_container_width=True):
                st.session_state["selected_post"] = str(latest["path"])
                st.session_state["page"] = "Blog"
                st.rerun()
        else:
            st.info("No blog posts found yet.")

        st.markdown("### Latest project")
        if projects:
            card(projects[0]["title"], projects[0]["desc"])
            if st.button("Open project", key="open_latest_project_home", use_container_width=True):
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
            <div class="muted" style="margin-top:10px;">Hands-on mini projects, clean analysis, and short write-ups as I learn.</div>
            """,
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
```

#### File G: `views/blog.py`
Path: `streamlit_portfolio/views/blog.py`
```python
import streamlit as st
import re
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

    q = st.text_input("Search posts", placeholder="Type to search by title or content...", key="blog_search_input")
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

    selected = st.selectbox("Select a post", post_titles, index=default_idx, key="blog_post_selectbox")
    post = next(p for p in filtered if p["title"] == selected)
    st.session_state["selected_post"] = str(post["path"])

    st.markdown(f"### {post['title']}")
    meta_bits = []
    if post["date"]:
        meta_bits.append(post["date"])
    if post.get("tags"):
        meta_bits.append(" | ".join([f"`{t}`" for t in post["tags"]]))
    if meta_bits:
        st.markdown(f"<div class='tiny'>{' | '.join(meta_bits)}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Clean markdown formatting, resolve equations, and resolve image directories to Base64
    content = normalize_math(post["content"])
    content = resolve_markdown_images(content, post["path"].parent)

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post["path"].stem.lower())
    is_oee_post = "oee" in slug or "overall equipment effectiveness" in post["title"].lower()
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
```

#### File H: `views/projects.py`
Path: `streamlit_portfolio/views/projects.py`
This module renders the visual list of project cards and the high-fidelity detail view using native components.
- Iterate over the structured JSON catalog loaded via `load_projects()`.
- Use a nice two-column responsive grid (`st.columns(2)`). Render individual custom project cards. Clicking "Open Project" sets `st.session_state["selected_project"] = project['slug']`.
- Provide a elegant native detail viewer based on project types:
  - **type == "game"**: Read and cleanly embed `wall-jump-maze/index.html` via `st.components.v1.html(html, height=750, scrolling=False)`. Provide standalone documentation and explanations natively below the frame.
  - **type == "embed"**: Render the Process Report PDF on the left and the live Google Sheet embed in a native tab, or use columns for side-by-side analysis.
  - **type == "report"**: Use native PDF rendering with a nice full-height frame, and side-by-side asset download buttons.
  - **type == "multi_report"**: Create a horizontal tab collection or an elegant sub-select radio selector allowing users to switch between Proposal, Midterm, Final, and Presentation PDFs dynamically, loading the correct file automatically into a unified embedded frame.
  - Ensure all download buttons have correct MIME types (`application/pdf`, `vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `text/csv`, etc.) and adapt container widths nicely.

#### File I: `views/about.py`
Path: `streamlit_portfolio/views/about.py`
```python
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

    st.markdown("---")
    st.markdown("### Focus & Skills")
    st.markdown(
        """
        <div style="margin-top: 10px;">
          <span class="pill">Python</span><span class="pill">Pandas</span><span class="pill">FastAPI</span>
          <span class="pill">Scikit-learn</span><span class="pill">EDA & Visualization</span>
          <span class="pill">ML Pipelines</span><span class="pill">Vector DB basics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
```

#### File J: `Homepage.py` (Rewritten Entry Point)
Path: `streamlit_portfolio/Homepage.py`
Rewrite `Homepage.py` to act as a lightweight global styles and router controller:
```python
import streamlit as st
from utils.helpers import load_posts, load_projects
from views.home import home_view
from views.projects import projects_view
from views.blog import blog_view
from views.about import about_view

st.set_page_config(
    page_title="Sujash Bharadwaj's Portfolio",
    layout="wide",
)

# Render Global Custom Styling and Fonts
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
    </style>
    """,
    unsafe_allow_html=True,
)

posts = load_posts()
projects = load_projects()

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

if st.session_state["page"] == "Home":
    home_view(posts, projects)
elif st.session_state["page"] == "Projects":
    projects_view()
elif st.session_state["page"] == "Blog":
    blog_view(posts)
elif st.session_state["page"] == "About":
    about_view()
```

---

### 3. Key Implementation Guidelines
- **Ensure imports are precise**: Do not introduce circular dependencies. Check that utility functions in `helpers.py` are properly imported in views and components.
- **Maintain session keys**: Make sure all Streamlit components (like search bars, textboxes, selectors, sliders, etc.) have explicit, unique keys to prevent state collision when switching pages.
- **Keep visual styling consistent**: Retain the precise custom CSS variables, fonts (Crimson Text + Oswald), spacing, and glassmorphic card boundaries in `Homepage.py` so the site keeps its highly premium look.
- **Do not use placeholders**: Use the existing local image files (`assets/img/profile.png`, `assets/img/cauchy.png`, etc.) and actual PDF documents inside `projects_static/` to ensure everything works flawlessly.
- **Double check math rendering**: Let Streamlit's markdown parser process the LaTeX formatted via `normalize_math` safely, with robust fallback mechanisms.
```
---

You are ready to begin. Implement all specified files cleanly and modernly!
