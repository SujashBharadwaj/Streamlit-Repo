# Streamlit Portfolio & Interactive Showcase

An interactive, high-performance Streamlit portfolio featuring modular page views, dynamic blog post reading, rich project showcases with live embeds, and interactive scientific / engineering playgrounds.

---

## 🚀 Quick Start

### 1. Run locally
```bash
# Navigate to the portfolio folder
cd streamlit_portfolio

# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run Homepage.py
```

### 2. Deploy (e.g. Streamlit Community Cloud / Render)
- Push your changes to GitHub.
- In Streamlit Cloud, point to `Homepage.py` as the main app entrypoint.
- Theme settings are configured under `.streamlit/config.toml`.

---

## 📁 Repository & Architecture Structure

```text
streamlit_portfolio/
├── Homepage.py              # Main application entry point & router
├── projects.json            # Centralized project metadata configuration
├── context.md               # Codebase architectural context & audit history
├── .streamlit/
│   └── config.toml          # Custom dark mode theme styling
├── assets/                  # Core static assets (favicons, CSS, profile images)
├── components/              # Interactive playgrounds & reusable UI components
│   ├── gradient_descent.py  # 1D cubic optimization interactive widget
│   ├── means_calculator.py  # Interactive multi-mean statistics suite
│   ├── oee_simulator.py     # Shift scenario OEE simulator
│   └── iframe.py            # Custom iframe renderer for live apps
├── posts/                   # Markdown blog posts with YAML frontmatter
├── views/                   # Page view controllers
│   ├── about.py             # About page & career profile
│   ├── blog.py              # Dynamic blog engine & reader view
│   ├── home.py              # Hero landing page & quick highlights
│   └── projects.py          # Interactive project gallery & detail renderer
└── utils/                   # Helper modules
    ├── base64_utils.py      # Image base64 encoding helpers
    ├── helpers.py           # Frontmatter and post parsing logic
    └── metadata_utils.py    # projects.json loader and parser
```

---

## 🌟 Key Features

- **Modular Architecture**: Clean separation between views (`/views`), interactive widgets (`/components`), and data parsing (`/utils`).
- **Live App Embed Support**: Integrated responsive iframe renderer for embedded web applications with role credential overlays and external repository links.
- **Dedicated Index/Detail Views**: Direct navigation and quick-jump dropdowns for both blog posts and projects.
- **Interactive Playgrounds**: Built-in interactive models for Statistics (Means Calculator), Machine Learning (1D Gradient Descent Simulator), and Industrial Engineering (OEE Simulator).
- **JSON-Driven Project Metadata**: Easily maintainable `projects.json` structure for adding new notebooks, web apps, PDFs, and repositories.

