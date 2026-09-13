# Streamlit Portfolio Repository

A modern, interactive Streamlit portfolio and engineering showcase. Features dynamic markdown blogging, interactive data & ML playgrounds, modular view routing, and live web application embedding.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/SujashBharadwaj/Streamlit-Repo.git
cd Streamlit-Repo/streamlit_portfolio

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run Homepage.py
```

---

## 📂 Repository Layout

```text
Streamlit-Repo/
├── CHANGELOG.md               # Version history and release notes
├── audit_report.md            # Codebase audit & structural refactoring records
├── portfolio_suggestions.md   # Architectural & feature improvement roadmap
└── streamlit_portfolio/       # Streamlit Application Source
    ├── Homepage.py            # Entry point & navigation router
    ├── projects.json          # Centralized project metadata registry
    ├── context.md             # Subsystem documentation & contextual history
    ├── README.md              # Application specific documentation
    ├── components/            # Interactive widget calculators & iframe embedder
    ├── posts/                 # Blog post Markdown files
    ├── utils/                 # Helper utilities (base64, metadata loader, helpers)
    └── views/                 # View controllers (home, about, blog, projects)
```

---

## 🛠️ Main Features

- **Live App Embed Support**: Native iframe rendering for web applications with overlay demo credentials.
- **Dynamic Blog Reader**: Clean Markdown renderer with YAML frontmatter parsing, interactive widgets, and deep-link routing.
- **Modular Architecture**: Separate view controllers (`views/`), calculation components (`components/`), and utility functions (`utils/`).
- **Configurable Projects**: Standardized schema in `projects.json` for external notebooks, live apps, PDFs, and internal tools.
