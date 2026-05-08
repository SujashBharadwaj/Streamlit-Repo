import base64
import json
import re
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
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
            posts.append(
                {"title": title, "date": date_ or "", "tags": tags, "path": p, "content": content, "excerpt": excerpt}
            )
    return posts


def load_projects() -> List[Dict]:
    json_path = ROOT / "projects.json"
    if json_path.exists():
        try:
            return json.loads(read_text(json_path))
        except Exception:
            pass
    # Fallback: scan directories
    projects: List[Dict] = []
    if PROJECTS_DIR.exists():
        for p in sorted(PROJECTS_DIR.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                projects.append({"slug": p.name, "title": p.name.replace("-", " ").title(), "desc": "", "eyebrow": "Project", "tags": [], "type": "report"})
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


def read_project_embed_html(slug: str, html_file: str = "index.html") -> str:
    path = PROJECTS_DIR / slug / html_file
    if path.exists():
        return read_text(path)
    return ""


def embed_pdf(pdf_path: Path, height: int = 860):
    """Render a PDF using pdf.js canvas rendering inside components.html.
    This bypasses Chrome's PDF plugin which gets blocked in sandboxed iframes.
    """
    data = pdf_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    uid = f"pdf-{abs(hash(str(pdf_path)))}"
    html = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <style>
      #{uid}-container {{
        width: 100%;
        height: {height}px;
        overflow-y: auto;
        border: 1px solid rgba(229,231,235,.10);
        border-radius: 14px;
        background: rgba(11,20,17,.60);
        padding: 8px 0;
      }}
      #{uid}-container canvas {{
        display: block;
        margin: 0 auto 12px auto;
        max-width: 100%;
        border-radius: 4px;
      }}
      #{uid}-info {{
        color: rgba(229,231,235,.78);
        font-size: .88rem;
        text-align: center;
        padding: 6px 0;
      }}
    </style>
    <div id="{uid}-info">Loading PDF...</div>
    <div id="{uid}-container"></div>
    <script>
      (function() {{
        const b64 = "{b64}";
        const container = document.getElementById("{uid}-container");
        const info = document.getElementById("{uid}-info");

        function b64ToUint8Array(base64) {{
          const binary = atob(base64);
          const len = binary.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
          return bytes;
        }}

        pdfjsLib.GlobalWorkerOptions.workerSrc =
          "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

        const pdfData = b64ToUint8Array(b64);
        const loadingTask = pdfjsLib.getDocument({{ data: pdfData }});
        loadingTask.promise.then(function(pdf) {{
          info.textContent = pdf.numPages + " page" + (pdf.numPages > 1 ? "s" : "");
          for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {{
            pdf.getPage(pageNum).then(function(page) {{
              const scale = 1.5;
              const viewport = page.getViewport({{ scale: scale }});
              const canvas = document.createElement("canvas");
              canvas.width = viewport.width;
              canvas.height = viewport.height;
              container.appendChild(canvas);
              const ctx = canvas.getContext("2d");
              page.render({{ canvasContext: ctx, viewport: viewport }});
            }});
          }}
        }}).catch(function(err) {{
          info.textContent = "Could not render PDF. Use the download button.";
          console.error(err);
        }});
      }})();
    </script>
    """
    components.html(html, height=height + 50, scrolling=True)


def resolve_markdown_images(content: str, base_dir: Path) -> str:
    """Resolves relative markdown image paths to base64 data URLs."""
    def replacer(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        # Skip already-resolved data URLs or http links
        if rel_path.startswith("data:") or rel_path.startswith("http"):
            return match.group(0)
        full_path = (base_dir / rel_path).resolve()
        if not full_path.exists():
            full_path = (ROOT / rel_path.replace("../", "")).resolve()
        if not full_path.exists():
            full_path = (ROOT / "assets" / "img" / Path(rel_path).name).resolve()
        if full_path.exists() and full_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif"):
            mime = f"image/{full_path.suffix.lower().lstrip('.')}"
            if mime == "image/jpg":
                mime = "image/jpeg"
            img_b64 = base64.b64encode(full_path.read_bytes()).decode("utf-8")
            return f'<img src="data:{mime};base64,{img_b64}" alt="{alt_text}" style="max-width:100%; border-radius:12px; margin:10px 0;">'
        return match.group(0)

    return re.sub(r'!\[(.*?)\]\((.*?)\)', replacer, content)


def normalize_math(md_text: str) -> str:
    md_text = md_text.replace(r"\(", "$").replace(r"\)", "$")
    md_text = md_text.replace(r"\[", "$$").replace(r"\]", "$$")
    return md_text


def parse_numeric_list(raw: str) -> List[float]:
    parts = re.split(r"[\s,]+", raw.strip())
    nums: List[float] = []
    for p in parts:
        if not p:
            continue
        try:
            nums.append(float(p))
        except ValueError:
            continue
    return nums


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
