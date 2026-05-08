# Implementation Plan: Streamlit Portfolio Cleanup & Modernization

This plan outlines the restructuring, modularization, and cleanup of the Streamlit portfolio website. The main objective is to make it incredibly easy for the user to add or update projects and blogs, while drastically improving the visual presentation, maintainability, and code quality.

---

## User Review Required

> [!IMPORTANT]
> - **Replacing BeautifulSoup HTML parsing with a `projects.json` config**: We will eliminate the dependency on the legacy `projects_static/index.html` file. Instead, we will define a clean, structured JSON file that maps all project titles, descriptions, tags, files, and external URLs. This makes adding or updating a project as simple as editing a text block.
> - **Native Streamlit Project Views**: We will replace the nested legacy project HTML pages (which contain duplicate navigation bars, headers, and footers, creating a cluttered "website inside a website" appearance) with a premium, native Streamlit detail view. The Maze mini-game will be embedded cleanly as a standalone component without the surrounding legacy elements.
> - **Markdown Image base64 Resolution**: We will implement a preprocessor that automatically resolves and embeds markdown images (like `cauchy.png`) into Streamlit as base64 data URLs. This fixes the broken image links on any Streamlit hosting platform.

---

## Proposed Changes

### 1. Configuration & Metadata

#### [NEW] [projects.json](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/projects.json)
Create a central structured JSON metadata file to define all portfolio projects.
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
    "desc": "Dataset, exception flags, and MI summaries with a live embed and interactive table.",
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
    "desc": "Client segmentation and retention analysis for Raftaar. Proposal, mid term, final, and presentation embedded on one page.",
    "eyebrow": "Capstone Study",
    "tags": ["Customer Analytics", "Retention", "Business Research", "Presentation"],
    "type": "multi_report",
    "pdfs": [
      {"name": "proposal.pdf", "label": "Proposal"},
      {"name": "midterm.pdf", "label": "Mid Term"},
      {"name": "final.pdf", "label": "Final"},
      {"name": "presentation.pdf", "label": "Presentation"}
    ]
  }
]
```

---

### 2. Utilities Layer

#### [NEW] [helpers.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/utils/helpers.py)
A module of helper functions to keep the main views clean and decoupled.
- `read_text(path)`: Safe file reading with utf-8 decoding.
- `load_posts()`: Dynamic parsing of `.md` blog posts with YAML frontmatter.
- `load_projects()`: Reads project details from `projects.json`.
- `embed_pdf(pdf_path, height)`: Renders PDF using native Streamlit or encoded data URLs.
- `resolve_markdown_images(content, base_dir)`: Detects relative image references (e.g. `../assets/img/...`) in markdown, encodes them as base64, and replaces them to render successfully.
- `normalize_math(content)`: Reformats math delimiters for Streamlit's LaTeX engine.
- `card(...)`, `quick_links(...)`: Reusable visual component renderers.

---

### 3. Components Layer (Interactive Dashboards)

#### [NEW] [means.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/components/means.py)
Move `render_means_interactive()` and its mathematical calculation engine (`compute_means_bundle()`) out of `Homepage.py`.

#### [NEW] [gradient_descent.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/components/gradient_descent.py)
Move `render_gradient_descent_interactive()` and its cubic optimizer engine out of `Homepage.py`.

#### [NEW] [oee.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/components/oee.py)
Move `render_oee_interactive()` and `compute_oee()` out of `Homepage.py`.

---

### 4. Views Layer (Pages)

#### [NEW] [home.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/views/home.py)
Renders the premium introduction page with the bio, profile picture, social icons, skills list, and "Latest Article" + "Latest Project" quick links.

#### [NEW] [blog.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/views/blog.py)
Renders the blog view with a clean text search bar, selector, and markdown body rendering. Resolves math symbols and embeds local image assets automatically.

#### [NEW] [projects.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/views/projects.py)
Renders a gorgeous native Streamlit project catalog and detail view:
- A responsive grid of modern project cards.
- Clean selector/quick jump.
- For games, embeds the canvas mini-game standalone without surrounding headers/footers.
- For sheets/embeds, renders the process report PDF and Google Sheet in native tabs or columns.
- For report collections, provides a clean card picker that loads the selected PDF directly using native layouts.

#### [NEW] [about.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/views/about.py)
Renders the refined profile view, skill pills, and personal interests.

---

### 5. Main Entry Point

#### [MODIFY] [Homepage.py](file:///c:/Users/User/Documents/GitHub/Streamlit-Repo/streamlit_portfolio/Homepage.py)
Rewrite `Homepage.py` as a lightweight router and design system coordinator:
- Imports custom CSS variables and sets fonts.
- Manages sidebar navigation and global page state.
- Dispatches routing to the modular views (`home_view()`, `projects_view()`, `blog_view()`, `about_view()`).
- Drastically reduces file size from 1,157 lines to ~100 lines!

---

## Verification Plan

### Automated / Interactive Verification
1. **Local Dev Server Execution**:
   - Run `streamlit run Homepage.py` inside the virtual environment.
   - Verify that the app launches instantly and successfully without any import or module errors.
2. **Visual Audit (Home, About)**:
   - Verify that the dark mode style, fonts, buttons, and responsive grid render correctly.
   - Ensure the social links and skill cards remain functional.
3. **Blog Verification**:
   - Navigate to the Blog page and search for posts.
   - Verify that the Cauchy portrait and mathematical charts in the Gradient Descent post display perfectly (resolved as base64).
   - Test each interactive playground (Means, Gradient Descent, OEE) within the blog to ensure they calculate and plot results in real-time.
4. **Projects Verification**:
   - Navigate to the Projects page.
   - Click "Open project" on several cards.
   - Verify that the BDM Capstone allows picking from Proposal, Midterm, Final, and Presentation PDFs, loading them beautifully.
   - Verify that the Wall Jump Maze is fully playable inside the embedded frame with arrow keys without showing duplicate headers/footers.
   - Verify that the Energy Equities project shows the Google Sheet and process PDF in a modern clean format.
