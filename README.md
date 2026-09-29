# Sujash Bharadwaj — Portfolio & Engineering Showcase

A modern, interactive developer portfolio built with **Next.js 14** (App Router). Features an animated cat mascot (⚡ Bijli), dynamic markdown blogging, interactive project showcases, and live web application embedding.

> **v4.1.0 ⚡ Bijli Edition** — [Full Changelog](CHANGELOG.md)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/SujashBharadwaj/Streamlit-Repo.git
cd Streamlit-Repo/portfolio-nextjs

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the portfolio.

---

## 📂 Repository Layout

```text
Streamlit-Repo/
├── CHANGELOG.md                    # Version history and release notes
├── README.md                       # This file
├── render.yaml                     # Render deployment configuration
│
├── portfolio-nextjs/               # ★ Next.js 14 Portfolio Application
│   ├── app/
│   │   ├── page.tsx                # Homepage (hero + Bijli + sliders)
│   │   ├── layout.tsx              # Root layout (sidebar + fonts)
│   │   ├── globals.css             # Neon Skyline design system
│   │   ├── components/
│   │   │   ├── BijliCharacter.tsx   # ⚡ Interactive animated cat mascot
│   │   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   │   ├── ProjectsSlider.tsx   # Horizontal project card slider
│   │   │   └── BlogSlider.tsx       # Horizontal blog post slider
│   │   ├── data/
│   │   │   ├── projects.json        # Centralized project metadata
│   │   │   └── posts/               # Blog post markdown files (YAML frontmatter)
│   │   ├── about/page.tsx           # About page
│   │   ├── blog/                    # Blog index + [slug] reader
│   │   └── projects/                # Projects index + [slug] detail
│   ├── public/
│   │   ├── bijli.jpg                # Bijli mascot portrait asset
│   │   ├── profile.png              # Profile photo
│   │   ├── demos/                   # Demo videos and screenshots
│   │   └── projects/                # Embedded project static files
│   ├── package.json
│   ├── tsconfig.json
│   └── render.yaml                  # Next.js-specific Render config
│
├── DatabaseStudy/                   # Open source chaos ERP database project
│   ├── generator.py                 # Randomized dirty data generator
│   ├── schema.sql                   # 28-table enterprise ERP schema
│   └── challenges/                  # Role-specific SQL challenge sets
│
└── streamlit_portfolio/             # Legacy Streamlit Application (archived)
    ├── Homepage.py                  # Entry point & navigation router
    ├── views/                       # View controllers
    ├── components/                  # Interactive widget calculators
    └── posts/                       # Blog post markdown files
```

---

## 🐱 Bijli — Interactive Mascot

**Bijli** (⚡ बिजली, "Lightning") is the portfolio's animated digital familiar — a fluffy, chubby, short-legged black cat with glowing amber-yellow eyes and a red collar.

### Features
- **Cursor Eye Tracking**: Bijli's eyes follow your mouse across the screen in real-time.
- **Click Interactions**: Click Bijli for randomized witty developer-cat speech bubbles.
- **Idle Animations**: Gentle breathing pulse, natural double-blink cycle, and hover alert state.
- **Sleep / Wake Toggle**: Let Bijli nap (curls into a loaf with 💤) or wake her up.
- **Sidebar Presence**: `⚡ Bijli watching` status badge with pulsing indicator across all pages.

### Technical Implementation
- Zero external animation dependencies — pure React state + CSS keyframes.
- Client component with `"use client"` directive, loaded via `next/dynamic` (SSR disabled).
- Coordinate interpolation with capped offset for smooth, non-jittery eye movement.

---

## 🛠️ Main Features

- **Neon Skyline Theme**: Dark ink (`#011627`) background with neon pink, blue, and teal accents. Inter + Syne typography.
- **Dynamic Blog Engine**: Markdown files with YAML frontmatter, auto-parsed excerpts, tag filtering, and horizontal slider on homepage.
- **Project Showcase**: Cards with iframe embedding for interactive HTML projects, live app links, and GitHub repository links.
- **Responsive Design**: Fixed sidebar on desktop, collapsed horizontal nav on mobile (< 900px).
- **Render Deployment**: Pre-configured `render.yaml` for zero-config deployment on Render.

---

## 🏗️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| Framework | Next.js 14 (App Router, React 18) |
| Language | TypeScript |
| Styling | Vanilla CSS (custom design tokens) |
| Fonts | Inter, Syne (Google Fonts) |
| Deployment | Render (Static / Node) |
| Mascot | Pure React + CSS Animations |

---

## 📜 License

This is a personal portfolio project. All rights reserved.
