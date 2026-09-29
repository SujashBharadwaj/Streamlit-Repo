# Portfolio — Next.js 14

The production-ready Next.js 14 (App Router) portfolio for **Sujash Bharadwaj**. Migrated from a Streamlit application to a static/SSR-capable Next.js build.

> **v4.1.0 ⚡ Bijli Edition**

---

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Production build
npm run build && npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the portfolio.

---

## Architecture

```text
app/
├── page.tsx                   # Homepage (hero with Bijli mascot, project & blog sliders)
├── layout.tsx                 # Root layout (sidebar navigation, Google Fonts, global CSS)
├── globals.css                # Neon Skyline design system (tokens, components, animations)
├── favicon.ico                # Browser tab icon (placeholder — pending custom designer asset)
│
├── components/
│   ├── BijliCharacter.tsx     # ⚡ Interactive animated cat mascot (client component)
│   │                            → Cursor eye tracking, click speech bubbles,
│   │                              idle breathing/blink animations, sleep/wake toggle
│   ├── Sidebar.tsx            # Fixed sidebar navigation with Bijli presence badge
│   ├── ProjectsSlider.tsx     # Horizontal scrollable project card carousel
│   └── BlogSlider.tsx         # Horizontal scrollable blog post carousel
│
├── data/
│   ├── projects.json          # Centralized project metadata (title, type, tags, links)
│   └── posts/                 # Blog post markdown files with YAML frontmatter
│       ├── 2025-09-02-means-guide.md
│       ├── 2025-09-08-gradient-descent.md
│       ├── 2026-01-22-oee.md
│       ├── 2026-08-18-frameworks-vs-languages.md
│       ├── 2026-08-18-version-control.md
│       └── 2026-09-18-modern-ai-taxonomy.md
│
├── about/page.tsx             # About page
├── blog/
│   ├── page.tsx               # Blog index with tag filtering
│   └── [slug]/page.tsx        # Individual blog post reader
└── projects/
    ├── page.tsx               # Projects gallery with category filters
    └── [slug]/page.tsx        # Individual project detail with iframe embed
```

---

## Design System — Neon Skyline

| Token | Value | Usage |
| :--- | :--- | :--- |
| `--bg-ink` | `#011627` | Page background |
| `--surface` | `#051b2e` | Card backgrounds |
| `--surface-2` | `#082138` | Elevated surfaces, speech bubbles |
| `--neon-pink` | `#FF3366` | Accents, hover borders, Bijli card glow |
| `--neon-blue` | `#20A4F3` | Links, active states, primary buttons |
| `--neon-teal` | `#2EC4B6` | Tags, badges, status indicators |
| `--text-snow` | `#F6F7F8` | Primary text |
| `--text-muted` | `rgba(246,247,248,0.55)` | Secondary text |

**Typography**: Inter (body, 400–700) + Syne (headings, 700–900) via Google Fonts CDN.

---

## Bijli (⚡ बिजली) — Mascot System

Bijli is a fluffy, chubby, short-legged black cat with amber-yellow eyes and a red collar — the portfolio's interactive digital familiar.

### Component: `BijliCharacter.tsx`
- **Type**: Client component (`"use client"`)
- **Loading**: Dynamic import via `next/dynamic` with `ssr: false`
- **Dependencies**: Zero external — pure React hooks + CSS keyframes

### Behaviors
| Behavior | Trigger | Implementation |
| :--- | :--- | :--- |
| Eye tracking | Mouse move anywhere | `mousemove` listener → coordinate interpolation with capped offset |
| Speech bubble | Click on Bijli | Random line from 10 witty quips, 3.5s auto-dismiss |
| Breathing | Always (when awake) | CSS `bijli-breathe` keyframe (4s `scale` cycle) |
| Blinking | Always (when awake) | CSS `bijli-blink` keyframe (double-blink at 43% and 81%) |
| Alert state | Hover on card | CSS `bijli-alert-pulse` (subtle scale pop) |
| Sleep mode | 🌙 toggle button | Loaf transform, grayscale filter, floating 💤 emoji |
| Wake | ☀️ toggle or click | Restores all animations and tracking |
| Sidebar badge | Always | Pulsing green dot + `⚡ Bijli watching` text |

### CSS Animations
- `bijli-breathe` — Subtle 4s scale pulse (1.0 → 1.015)
- `bijli-blink` — Natural double-blink every 5s
- `bijli-alert-pulse` — Hover scale pop (1.04 → 1.07)
- `bijli-speech-in` — Speech bubble fade + slide entrance
- `bijli-zzz-float` — Sleep mode floating 💤
- `bijli-dot-pulse` — Status dot opacity pulse

---

## Deployment

Configured for **Render** via `render.yaml`:

```yaml
services:
  - type: web
    name: sujash-portfolio
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm start
```

---

## Favicon

The default Next.js favicon is a placeholder. A custom Bijli-themed favicon is pending from a designer. Required deliverables:

| Asset | Size | Format | Location |
| :--- | :--- | :--- | :--- |
| Tab icon | 32×32 (or SVG) | `.svg` / `.png` | `app/icon.svg` or `app/icon.png` |
| Apple Touch | 180×180 | `.png` | `app/apple-icon.png` |
| Legacy fallback | 32×32 multi-res | `.ico` | `app/favicon.ico` |

Next.js 14 App Router auto-discovers and injects these from the `app/` directory.
