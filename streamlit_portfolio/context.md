# Codebase Context: Streamlit Portfolio

This document provides a comprehensive overview of the portfolio website's architecture, key components, and current issues identified during our codebase audit. It serves as the baseline for the cleanup and modernization plan.

---

## 1. Project Background
The portfolio was originally built as a static website hosted on **GitHub Pages**. The user transitioned to **Streamlit** to leverage Python's rich ecosystem and build interactive data applications/dashboards directly into the portfolio. However, the migration left behind legacy static elements and introduced some complex parsing mechanisms, making it difficult to update projects and blogs.

---

## 2. Directory Structure
Here is the current layout of the repository:

```text
Streamlit-Repo/
├── streamlit_portfolio/
│   ├── .streamlit/
│   │   └── config.toml          # Custom dark mode theme configuration
│   ├── assets/                  # Legacy static site assets
│   │   ├── css/                 # Old stylesheet (style.css)
│   │   ├── img/                 # Images used in blog posts & profile
│   │   └── js/                  # Old JS scripts
│   ├── posts/                   # Blog posts stored as Markdown (.md)
│   │   ├── 2025-09-02-means-guide.md
│   │   ├── 2025-09-08-gradient-descent.md
│   │   └── 2026-01-22-oee.md
│   ├── blog_static/             # Legacy static HTML blog pages (unused in Streamlit)
│   ├── about_static/            # Legacy static HTML about page (unused in Streamlit)
│   ├── projects_static/         # Project reports, data, and mini-games
│   │   ├── BDMcapstone/         # PDFs & metadata for Capstone project
│   │   ├── EnergyEquitiesMI/    # MI spreadsheet & process report PDF
│   │   ├── commodity-equity-linkages/ # Market analysis PDF
│   │   ├── wall-jump-maze/      # Self-contained Canvas JS mini-game (index.html)
│   │   └── index.html           # Old HTML project index used by Streamlit to parse metadata
│   ├── Homepage.py              # Single entry point for Streamlit (1,157 lines)
│   └── requirements.txt         # App dependencies (streamlit, beautifulsoup4, markdownify)
```

---

## 3. How the Current Site Works

### 3.1. Navigation & State
- Navigation is managed using a sidebar radio selector (`st.sidebar.radio`), which updates `st.session_state["page"]`.
- The pages available are: `"Home"`, `"Projects"`, `"Blog"`, and `"About"`.

### 3.2. Blog Pages (`/posts`)
- Loaded dynamically via `load_posts()` which reads markdown files from the `posts/` directory.
- Supports simple YAML-like frontmatter parsing for `title`, `date`, and `tags`.
- **Special Interactive Demos**: In `Homepage.py`, the system intercepts specific blog posts (`means-guide`, `gradient-descent`, `oee`) and replaces placeholder markers with fully functional Streamlit playgrounds:
  - `means-guide`: Interactive statistics calculator for multiple types of means (arithmetic, geometric, harmonic, RMS, contraharmonic, power, etc.).
  - `gradient-descent`: 1D cubic function optimizer simulation.
  - `oee`: Shift scenario simulator calculating Overall Equipment Effectiveness.

### 3.3. Projects Page (`/projects_static`)
- Loaded using `load_projects()` which parses `projects_static/index.html` via **BeautifulSoup** to extract project cards, titles, descriptions, and folders.
- If a project is selected, the application can load the legacy `index.html` from that project's folder using `st.components.v1.html`.
- If legacy mode is disabled, it lists available PDFs and spreadsheets in `projects_static/<slug>/` and provides native PDF viewers and download buttons.

---

## 4. Key Friction Points & Issues

### ❌ Fragile Project Configuration
Currently, adding or updating projects requires manually editing the HTML in `projects_static/index.html` with precise structures (`<a class="tile">`, etc.) so that BeautifulSoup can parse it. This is highly fragile, unintuitive, and goes against Streamlit best practices.

### ❌ Duplicate Header/Footer inside Iframe Embeds
When using `use_legacy_project_page`, the app embeds the legacy project's `index.html` in an iframe. Since these legacy files have their own header/footer navigation links (which point to non-existent pages like `../../homepage.html`), it results in a "website inside a website" look, with broken links that ruin the user experience.

### ❌ Broken Markdown Images
Markdown files in `posts/` reference images with relative paths like `../assets/img/cauchy.png`. Since Streamlit does not serve parent directories of `posts/` as a static assets folder by default, these images fail to render on the blog page.

### ❌ Single Massive 1,157-Line `Homepage.py` File
All styling, custom CSS, state routing, loading helpers, and three complex interactive dashboards are crammed into a single python file. This makes debugging, cleaning up, and expanding the portfolio extremely difficult.

---

## 5. Architectural Recommendations

1. **JSON Metadata Configuration (`projects.json`)**: Eliminate BeautifulSoup parsing of static HTML. Move all project descriptions, tags, and file mappings to a clean JSON file that is simple to edit.
2. **Modularize Streamlit Structure**: Split `Homepage.py` into distinct page modules (`views/`) and dashboard helpers (`components/`) to improve maintainability.
3. **Robust Image Encoding**: Implement a Markdown preprocessor that detects relative image paths, loads them from disk, converts them to base64, and injects them as data URLs. This ensures blog images render perfectly in any Streamlit hosting environment.
4. **Native Project Viewers**: Replace duplicate legacy HTML pages with a clean, native Streamlit layout for each project, embedding files (PDFs, Google Sheets, or the self-contained Maze HTML) beautifully without surrounding headers/footers.
