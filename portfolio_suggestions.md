# Portfolio Suggestions — Sujash Bharadwaj

Tailored recommendations for a final-year Applied Statistics & Data Science student who builds practical projects, writes technical blog posts with interactive demos, and is targeting roles in data science / ML / analytics.

---

## 🏠 1. Home Page

### What's working
- Hero text is punchy and clear — "I build practical projects, write what I learn, and keep things reproducible" is a great tagline.
- Latest article + latest project cards give visitors an immediate entry point.

### What's missing

| Gap | Why it matters | Suggested fix |
|-----|---------------|--------------|
| **No resume / CV download** | Recruiters land on portfolios to grab a resume. If they can't, they leave. | Add a prominent "Download Resume" button next to "Explore projects" / "Read the blog". Store it as `assets/resume.pdf`. |
| **No "at a glance" stats** | You have 4 projects and 3 blog posts — show that you're productive. | Add a small metrics row: `st.columns(3)` with `st.metric("Projects", "4")`, `st.metric("Blog Posts", "3")`, `st.metric("Interactive Demos", "3")`. These are cheap but visually impressive. |
| **The "What I'm doing now" section is vague** | "AI & ML", "Statistics", "Reproducible notebooks" are labels, not activities. | Replace with 2–3 concrete bullet points: e.g., *"Building an NLP pipeline for biomedical abstracts"*, *"Writing a guide on bootstrap confidence intervals"*. Show intent, not just interests. |
| **No call-to-action for hiring** | You're a final-year student — the site should scream "I'm available". | Add a subtle banner or sidebar note: *"Open to data science & analytics roles — June 2026 onward."* with your email or a contact form link. |

---

## 📂 2. Projects Page

### What's working
- The card grid with eyebrow labels, tag chips, and descriptions is clean.
- The pdf.js renderer is a smart engineering choice — it sidesteps Chrome's iframe PDF blocking.
- The Wall Jump Maze game is a unique differentiator. Very few DS portfolios have a playable game.

### What would elevate it

| Suggestion | Details |
|-----------|---------|
| **Add GitHub repo links per project** | Add a `"repo"` key in `projects.json` and render a "View on GitHub" link button next to each project's download buttons. Recruiters *will* click through to see your code quality. |
| **Add a "Key Findings" summary for each report** | Right now, clicking a project shows the raw PDF. Add a 3–5 bullet "TL;DR" above the PDF viewer (a new `"findings"` field in `projects.json`). This saves the visitor from reading a 20-page report to figure out what you did. |
| **Add a "Tech Stack" section per project** | You have `tags`, but they're small chips. Add a visible list: *"Built with: Python, Pandas, Granger causality tests, rolling beta regression"*. This maps directly to keywords recruiters search for. |
| **Add more projects** | 4 projects is a decent start, but for a final-year student targeting DS roles, aim for 6–8. Candidates you're competing with have Kaggle notebooks, end-to-end ML pipelines, and deployed models. Consider adding: an EDA notebook (e.g., a public dataset), an ML classification project, or a small API/dashboard. |
| **Add thumbnail images** | Each project card is currently text-only. A `"thumbnail"` field in `projects.json` pointing to a screenshot of the project output (a chart, a game screenshot) would make the grid feel alive. |

---

## 📝 3. Blog Page

### What's working
- The interactive demos (OEE calculator, means playground, gradient descent simulator) are **exceptional** differentiators. Very few portfolios have live, usable widgets embedded in blog posts.
- The card-based post selector with search is clean.

### What would elevate it

| Suggestion | Details |
|-----------|---------|
| **Write more posts** | 3 posts is thin. Aim for 6–10. Strong topic ideas for your profile: *Bootstrap & Confidence Intervals*, *A/B Testing from Scratch*, *PCA Explained Visually*, *Regex for Data Cleaning*, *How I Built This Portfolio in Streamlit*. Each post with an interactive widget would be a portfolio showpiece. |
| **Add estimated reading time** | Parse `len(content.split())` and show *"5 min read"* on each card. It's a tiny UX win that signals professionalism. |
| **Add "Related posts" at the bottom** | After reading a post, show links to other posts. With 3 posts this is trivial, but it builds the habit for when you have 10+. |
| **Add social sharing / copy-link button** | If someone likes your gradient descent explainer, they should be able to share it. A simple "Copy link" button (using Streamlit Community Cloud URL + post slug) goes a long way. |
| **Fix the `:contentReference` artifacts** | The OEE blog post contains raw `:contentReference[oaicite:0]{index=0}` strings throughout. These are likely leftover from AI-assisted drafting and render as visible noise. Strip them. |

---

## 🧑 4. About Page

### What's working
- The bio is genuine and human — F1, cricket, Age of Empires. That's memorable.
- The skill pills are clean.

### What would elevate it

| Suggestion | Details |
|-----------|---------|
| **Add an Education timeline** | You have two degrees running in parallel (MIT-WPU + IITM BS). A visual timeline (even just a styled `st.markdown` list with years) would make this clearer than a paragraph. |
| **Expand the skills section** | The current list (Python, Pandas, FastAPI, Scikit-learn, EDA & Visualization, ML Pipelines, Vector DB basics) is decent but generic. Group them into tiers: *"Strong: Python, Pandas, Scikit-learn, Statistical Modeling"* / *"Working with: FastAPI, Docker, LLM APIs"* / *"Exploring: Bioinformatics, Vector DBs"*. Honesty about skill levels is more impressive than a flat list. |
| **Add certifications or coursework** | If you've completed any NPTEL, Coursera, or IITM courses with certificates, list them. They're social proof. |
| **Add a "Currently reading / learning" section** | This signals growth mindset. E.g., *"Reading: Elements of Statistical Learning. Learning: BioPython for sequence analysis."* |

---

## 🎨 5. Design & UX (Global)

| Area | Issue | Fix |
|------|-------|-----|
| **Favicon** | No custom favicon set in `st.set_page_config`. The tab shows the default Streamlit icon. | Generate a small logo/icon and pass `page_icon="assets/img/favicon.png"` to `st.set_page_config()`. |
| **Page title doesn't update per page** | The browser tab always says "Sujash Bharadwaj's Portfolio" even on the Blog or About page. | Dynamically set the title by using `st.set_page_config(page_title=f"Sujash Bharadwaj — {page}")`. Note: this must be the first Streamlit call — you'd need to restructure slightly. Alternatively, add an HTML `<title>` override in CSS. |
| **No footer** | The page just… ends. There's no closing element. | Add a simple footer at the bottom of every page: *"© 2026 Sujash Bharadwaj · Built with Streamlit"* with your social links. This is standard on professional portfolios. |
| **Sidebar lacks a photo** | The sidebar shows your name and "Portfolio and personal blog" but no face. | Add a small circular profile image to the sidebar above the navigation radio. People remember faces. |
| **No loading state / skeleton** | When navigating between pages, there's a brief flash of nothing. | Use `st.spinner("Loading...")` or `st.status()` wrappers around heavy sections (especially the PDF renderer). |
| **Card hover effects are CSS-only** | The `.card:hover` border-color change is subtle. | Consider adding a slight `box-shadow` expansion on hover for more tactile feedback: `box-shadow: 0 14px 40px rgba(0,0,0,.55);` |

---

## 🔧 6. Technical / Code Quality

| Area | Issue | Fix |
|------|-------|-----|
| **Legacy static directories** | `about_static/`, `blog_static/`, `projects_static/index.html` are leftovers from the GitHub Pages era. They add confusion and repo bloat. | Delete `about_static/` and `blog_static/` entirely. Remove `projects_static/index.html` (the old HTML index). Keep only the actual project subdirectories. |
| **No `.gitignore` for `__pycache__`** | The `__pycache__` directory is presumably tracked. | Add a `.gitignore` with `__pycache__/`, `*.pyc`, `.DS_Store`. |
| **No error boundaries** | If a blog post has malformed frontmatter or a project JSON entry is missing a required field, the app crashes with a raw Python traceback. | Wrap `load_posts()` and `load_projects()` with try/except and show `st.error()` messages instead of crashing. Similarly, add `try/except` around `embed_pdf()`. |
| **`projects_static/.DS_Store`** | macOS metadata file is checked in. | Delete it and add `.DS_Store` to `.gitignore`. |

---

## 📈 7. Career-Impact Suggestions (the "So What?" Layer)

These are the suggestions that will have the most impact on *getting hired*:

> [!IMPORTANT]
> ### The #1 thing your portfolio is missing: **Outcomes and Impact**
>
> Every project description says *what you did*, but none say *what happened*. Compare:
> - ❌ "Client segmentation and retention analysis for Raftaar"
> - ✅ "Segmented 1,200+ clients into 4 behavioral clusters, identifying a high-churn segment that represented 35% of revenue"
>
> Add a `"impact"` field to `projects.json` and render it prominently on each project card.

| Suggestion | Why |
|-----------|-----|
| **Quantify your project outcomes** | "Ranked indicator dashboard" → "Dashboard tracking 12 commodity-equity pairs with 5-year rolling betas, used to flag 3 divergence signals". Numbers stick. |
| **Add a "How I'd improve this" section** | For each project, write 2–3 things you'd do differently or next. This shows self-awareness and growth — traits hiring managers look for in junior candidates. |
| **Link to live deployed versions** | If any project is deployed (Streamlit Cloud, Hugging Face Spaces, etc.), add a "Live Demo" button. The portfolio itself should be deployed too. |
| **Add a contact / hire-me CTA** | A final-year student's portfolio should have a clear, visible *"I'm looking for opportunities"* section. Add this to the Home page and the About page. |

---

## Priority Order

If you're short on time, tackle these in order:

1. **Fix the `:contentReference` artifacts in the OEE post** — it's broken content visible to everyone (5 min)
2. **Add a resume download button** — highest recruiter impact (10 min)
3. **Add GitHub repo links to projects** — proves code quality (15 min)
4. **Delete legacy directories** — reduces confusion (5 min)
5. **Add outcome/impact lines to project descriptions** — career impact (30 min)
6. **Write 2–3 more blog posts** — fills out the portfolio (ongoing)
7. **Add a footer and favicon** — polish (20 min)
8. **Add an education timeline to About** — context for dual-degree (20 min)
