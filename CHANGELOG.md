# Changelog

All notable changes to this project will be documented in this file.

## [v2.4.0] — 2026-09-18

### Added
- **Faulty Scientific Calculator**: Satirical, maliciously compliant simulation of the infamous GATE / TCS iON on-screen exam calculator (`projects_static/faulty-scientific-calc/index.html`). Features authentic TCS iON styling, broken mouse click resistance (simulating dust under test center rubber membranes), keypad musical chairs (button reshuffle), multilingual script roulette (Devanagari and Roman numerals, literal Hindi translations), over-engineered mathematical outcomes (`1 + 1` -> `sin(90°) + cos(0°)`), synthesized Web Audio click sounds, and a proctor surveillance paranoia simulator.
- **Portfolio Showcase**: Integrated Faulty Scientific Calculator into `projects.json` with dedicated in-app iframe rendering, HTML download, and backstory writeup.
- **Homepage Showcase**: Elevated Faulty Scientific Calculator as the featured latest project and the Modern AI Taxonomy article as the featured latest article on the portfolio homepage.
- **Version Bump**: Bumped project release to `v2.4.0`.

---

## [v2.3.5] — 2026-09-18

### Added
- **Blog Post**: "Beyond the Monolith — Deconstructing SLMs, VLMs, VLAs, World Models, and the Post-LLM Frontier" (`posts/2026-09-18-modern-ai-taxonomy.md`). Comprehensive technical survey of the post-scaling landscape covering Small Language Models (0.5B–8B edge efficiency), Vision-Language Models (dynamic patchification & grounding), Vision-Language-Action Models & LAMs (embodied robotics & GUI control), World Models (spatial simulation & predictive physics), JEPAs & Large Concept Models (latent-space non-autoregressive reasoning), complete with an architectural comparison matrix.

### Fixed
- **Blog Code Block & Backtick Corruption**: In `views/blog.py`, markdown was previously being passed through `bleach.clean()`, which stripped backticks and severely corrupted fenced code blocks (````python) and inline code tags into plain text. Fixed by rendering markdown cleanly through `st.markdown(content, unsafe_allow_html=True)` while preserving math normalization and image resolution.
- **Blog Reader Duplicate Heading**: Fixed duplicate title rendering where posts with leading `# Title` rendered both the Streamlit `### Title` component and the markdown `# Title` line. Redundant leading headings that match post metadata are now cleanly stripped.
- **DatabaseStudy SQLite Connection Safety**: In `components/db_study_preview.py`, refactored database queries to use a context manager (`with sqlite3.connect(...) as conn:`) ensuring connections are safely closed even if sample table queries encounter exceptions.
- **Version Badge Update**: Updated sidebar version badge to `v2.3.5` in `Homepage.py`.

---

## [v2.3.0] — 2026-09-13

### Added
- **DatabaseStudy — Open Source Project**: Chaos-simulated enterprise ERP database generator (`DatabaseStudy/`). 28 interconnected tables across 6 modules (Finance, Sales, Procurement, Inventory, Logistics, HR) with fully randomized dirty data, JSON payloads, mixed date formats, orphan FKs, and ledger drift. Non-deterministic by design.
- **Challenge Suite**: 4 role-specific SQL & analytics challenge sets targeting Data Analysts, Data Scientists, Analytics Engineers, and DBAs (`DatabaseStudy/challenges/`).
- **Portfolio Integration**: New `db_study` project type in `projects.json` with `head(5)` dirty data previews, schema overview cards, tabbed challenge viewer, and GitHub links (`components/db_study_preview.py`).

---

## [v2.2.0] — 2026-09-11

### Added
- **Live App Embed Support**: Added native `live_app` project renderer in `views/projects.py` with embedded iframe (`components.iframe`), full-screen launch, repository links, and styled demo credentials display.
- **MAD-1 Trekking Management App**: Updated project metadata with live Render hosted link (`https://mad-1-project-g7e0.onrender.com/`), IIT Madras MAD-1 course context, and default role-based test credentials (Admin, Staff, Trekker).

### Changed
- **Projects page — Gallery / Detail split**: Clicking "Open project" now transports the user to a dedicated detail page with `← Back to all projects` button, quick-jump dropdown, and prev/next navigation. The card grid is no longer stacked above the detail content.
- **Blog page — Index / Reader split**: Clicking "Read article →" now transports the user to a dedicated reader page with `← Back to all posts` button, quick-jump dropdown, and prev/next navigation.
- **Home page direct-jumps**: "Open project" and "Open article" shortcuts on the Home page now land directly in the detail/reader views.

---

## [v2.1.0] — 2026-08-18

### Changed
- **Bio updated**: Graduated from MIT-WPU + IITM BS. Now a Software Engineer at sfhawk Solutions.
- **"What I'm doing now"**: Added Computer Vision, SLM & VLM, .NET & Angular, React.
- **About page**: Updated bio, role, and expanded Focus & Skills pills.
- **External project renderer**: Now shows one-liner descriptions for each linked notebook/repo.

### Fixed
- Favicon white border — cropped and converted from JFIF to tightly-cropped PNG.

---

## [v2.0.0] — 2026-08-18

### Added
- **`.gitignore`**: Comprehensive ignore rules for Python caches, virtual environments, secrets, IDE configs, and OS files.
- **Custom favicon**: `<SB>` branded favicon loaded via PIL in `st.set_page_config`.
- **Version badge**: Emerald-tinted `v2.x.x` pill badge in the sidebar.
- **Blog Post**: "Demystifying Version Control — History, Architecture & Git Mechanics".
- **Blog Post**: "Frameworks vs. Languages — Inversion of Control & Knowing the Difference".
- **Project**: Kaggle ML Competitions Suite (7 notebooks across 2 MLP terms).
- **Project**: MCA Agent — Agentic AI RAG (experimental).
- **Project**: Trekking Management App (MAD-1) — Flask full-stack.
- **External project type**: New `"type": "external"` renderer in projects view for Kaggle/GitHub-hosted projects.

### Changed
- **Page title**: Updated to "Sujash Bharadwaj | Software & ML Engineer".
- **Header font**: Changed from Oswald to Copperplate Gothic (with Copperplate and Oswald fallbacks).

---

## [v1.0.0] — 2025-06-xx (pre-versioning)

Initial Streamlit portfolio with:
- Dark emerald theme with Crimson Text + Oswald typography.
- Blog engine with YAML frontmatter and interactive playgrounds (Means, Gradient Descent, OEE).
- Projects page with PDF embedding, Google Sheets embed, and Canvas mini-game.
- About page with social links.
