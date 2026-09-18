import streamlit as st
import streamlit.components.v1 as components
from utils.helpers import load_projects, list_project_files, read_project_embed_html, embed_pdf, sanitize_html, PROJECTS_DIR
from components.db_study_preview import render_db_study_preview


def projects_view():
    projects = load_projects()

    if not projects:
        st.info("No projects found.")
        return

    slugs = [p["slug"] for p in projects]

    # Initialise session keys
    if st.session_state.get("selected_project") not in slugs:
        st.session_state["selected_project"] = projects[0]["slug"]
    if "project_detail_open" not in st.session_state:
        st.session_state["project_detail_open"] = False

    # ---- Route: Detail view or Gallery ----
    if st.session_state["project_detail_open"]:
        _detail_view(projects)
    else:
        _gallery_view(projects)


# =====================================================================
# Gallery view — card grid only, no detail content
# =====================================================================
def _gallery_view(projects):
    st.markdown("## Projects")
    st.markdown(sanitize_html('<div class="muted">Reports, dashboards, and interactive builds with downloadable outputs.</div>'), unsafe_allow_html=True)
    st.markdown("")

    st.markdown("### Featured")
    grid_cols = st.columns(2, gap="medium")
    for i, p in enumerate(projects):
        tags = p.get("tags", [])
        chips = "".join([f"<span class='project-chip'>{t}</span>" for t in tags[:4]])
        with grid_cols[i % 2]:
            st.markdown(
                sanitize_html(f"""
                <div class="project-card">
                  <div class="project-eyebrow">{p.get("eyebrow", "Project")}</div>
                  <div class="project-title">{p["title"]}</div>
                  <div class="muted">{p.get("desc", "")}</div>
                  <div class="project-chips">{chips}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )
            if st.button("Open project", key=f"open_project_{p['slug']}", use_container_width=True):
                st.session_state["selected_project"] = p["slug"]
                st.session_state["project_detail_open"] = True
                st.rerun()


# =====================================================================
# Detail view — dedicated page for a single project
# =====================================================================
def _detail_view(projects):
    slug = st.session_state["selected_project"]
    project = next((p for p in projects if p["slug"] == slug), projects[0])

    # ---- Top navigation bar ----
    st.markdown("")
    nav_left, nav_right = st.columns([1, 2], gap="small")
    with nav_left:
        if st.button("← Back to all projects", key="back_to_gallery", use_container_width=True):
            st.session_state["project_detail_open"] = False
            st.rerun()
    with nav_right:
        titles = [p["title"] for p in projects]
        slug_by_title = {p["title"]: p["slug"] for p in projects}
        selected_title = project["title"]
        new_title = st.selectbox(
            "Quick jump",
            titles,
            index=titles.index(selected_title),
            key="project_detail_selectbox",
            label_visibility="collapsed",
        )
        if slug_by_title[new_title] != slug:
            st.session_state["selected_project"] = slug_by_title[new_title]
            st.rerun()

    # ---- Detail header card ----
    tags = project.get("tags", [])
    chips = "".join([f"<span class='project-chip'>{t}</span>" for t in tags])
    st.markdown(
        sanitize_html(f"""
        <div class="card" style="margin-top:8px;">
          <div class="project-eyebrow">{project.get("eyebrow", "Project")}</div>
          <div style="font-size:1.35rem;font-weight:800;">{project["title"]}</div>
          <div class="muted" style="margin-top:8px;">{project.get("desc", "")}</div>
          <div class="project-chips">{chips}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ---- Render project payload by type ----
    ptype = project.get("type", "report")

    if ptype == "game":
        _render_game(project)
    elif ptype == "embed":
        _render_embed(project)
    elif ptype == "multi_report":
        _render_multi_report(project)
    elif ptype == "live_app":
        _render_live_app(project)
    elif ptype == "external":
        _render_external(project)
    elif ptype == "db_study":
        render_db_study_preview(project)
    else:
        _render_report(project)

    # ---- Bottom prev / next navigation ----
    st.markdown("---")
    slugs = [p["slug"] for p in projects]
    idx = slugs.index(slug)
    prev_col, _, next_col = st.columns([1, 2, 1])
    if idx > 0:
        with prev_col:
            if st.button(f"← {projects[idx - 1]['title']}", key="prev_project", use_container_width=True):
                st.session_state["selected_project"] = slugs[idx - 1]
                st.rerun()
    if idx < len(slugs) - 1:
        with next_col:
            if st.button(f"{projects[idx + 1]['title']} →", key="next_project", use_container_width=True):
                st.session_state["selected_project"] = slugs[idx + 1]
                st.rerun()


# =====================================================================
# Type-specific renderers (unchanged logic, extracted from old file)
# =====================================================================

def _render_live_app(project):
    """Render live embedded web applications with iframe, quick actions, and test credentials."""
    live_url = project.get("live_url", "")
    github_url = project.get("github_url", "")
    credentials = project.get("credentials", [])

    # Action buttons and Demo credentials section
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        if live_url:
            st.link_button("🚀 Launch Full App", live_url, use_container_width=True)
    with col2:
        if github_url:
            st.link_button("💻 GitHub Repo", github_url, use_container_width=True)

    if credentials:
        cred_items = " &nbsp;|&nbsp; ".join(
            [f"<strong>{c['role']}:</strong> <code>{c['username']}</code> / <code>{c['password']}</code>" for c in credentials]
        )
        st.markdown(
            sanitize_html(f"""
            <div class="card" style="padding:10px 16px; margin: 12px 0 16px 0; border-left: 3px solid #10B981; font-size:0.95rem;">
              <span style="color:#34D399; font-weight:700;">Default Demo Credentials:</span> {cred_items}
            </div>
            """),
            unsafe_allow_html=True,
        )

    if live_url:
        st.markdown("#### Live Interactive App")
        components.iframe(src=live_url, height=800, scrolling=True)
    else:
        st.info("Live app URL not configured.")


def _render_external(project):
    """Render projects hosted on external platforms (Kaggle, GitHub, etc.)."""
    links = project.get("links", [])
    if not links:
        st.info("No external links configured for this project.")
        return

    st.markdown("#### External Links")
    # Render links in a 2-column grid with descriptions
    link_cols = st.columns(2, gap="medium")
    for i, link in enumerate(links):
        with link_cols[i % 2]:
            desc_html = ""
            if link.get("desc"):
                desc_html = f'<div class="muted" style="font-size:.92rem; margin-top:4px;">{link["desc"]}</div>'
            st.markdown(
                sanitize_html(f"""
                <div class="card" style="min-height:90px; padding:14px 16px;">
                  <div style="font-size:1.05rem; font-weight:700;">{link['label']}</div>
                  {desc_html}
                </div>
                """),
                unsafe_allow_html=True,
            )
            st.link_button(
                f"\U0001f517 Open",
                link["url"],
                use_container_width=True,
            )


def _render_game(project):
    slug = project["slug"]
    html_file = project.get("html_file", "index.html")
    html = read_project_embed_html(slug, html_file)
    if html:
        st.markdown(f"#### Interactive Simulation")
        frame_height = 800 if slug == "faulty-scientific-calc" else 750
        components.html(html, height=frame_height, scrolling=True)

        html_path = PROJECTS_DIR / slug / html_file
        st.download_button(
            label=f"Download {project['title']} HTML",
            data=html_path.read_bytes(),
            file_name=html_file,
            mime="text/html",
            use_container_width=True,
        )
    else:
        st.info("Interactive project file not found.")

    st.markdown("")
    st.markdown("### Why I Built This")
    if slug == "faulty-scientific-calc":
        st.markdown(
            """
            Back in my college days, I used to joke about building a completely faulty scientific calculator as my final year project.
            Anyone who has ever prepared for the **GATE exam** or appeared for a **TCS iON virtual test** remembers the collective trauma of using their rigid, on-screen exam calculator with a worn-out test center mouse.

            I built this satirical web app to recreate the worst possible UX while staying maliciously compliant:
            - **Broken Mouse Click Resistance**: Buttons require between 2 and 4 rapid clicks before registering key contact, simulating dust under the exam center rubber membrane.
            - **Keypad Musical Chairs**: Every few clicks, the numeric buttons scramble their positions.
            - **Multilingual Script Roulette**: Number labels swap into Devanagari numerals (`१, २, ३...`) or Roman numerals, while trig functions translate literally into Hindi (`sin` -> *पाप*, `log` -> *लकड़ी*).
            - **Absurd & Over-Engineered Math**: `1 + 1` evaluates to `sin(90°) + cos(0°)`, `5 * 5` outputs `24.999999999999996 ± 4.2e-16`, and zero division deducts 2.67 negative marks.
            - **Proctor Paranoia Simulator**: Periodic notifications warn you about suspicious blinking or excessive quietness in the examination hall.
            """
        )
    else:
        st.markdown(
            """
            I wanted to add more interactive displays to my portfolio, and a Pac-Man-inspired mini game felt like a strong way to do it.
            The goal was to challenge myself to build a clean browser game using only HTML, CSS, JavaScript, and the Canvas API,
            then embed it inside Streamlit with `st.components.v1.html()`.

            How it works:
            - The maze is a 2D grid (`1` wall, `0` path, `2` pellet).
            - You move tile-by-tile with arrow keys and collect pellets to increase score.
            - A ghost moves through the maze, respects walls, and ends the run on collision.
            - Press `Space` to activate a short wall-jump window (~300ms) that lets you phase through walls.
            - Wall jump has a cooldown (~3s), so timing matters.
            """
        )


def _render_embed(project):
    slug = project["slug"]
    pdf_name = project.get("pdf_file", "")
    sheet_url = project.get("sheet_url", "")

    col_left, col_right = st.columns([1.4, 1], gap="large")

    with col_left:
        if pdf_name:
            pdf_path = PROJECTS_DIR / slug / pdf_name
            if pdf_path.exists():
                st.markdown("#### Process Report")
                embed_pdf(pdf_path, height=800)

    with col_right:
        st.markdown("### Downloads")
        if pdf_name:
            pdf_path = PROJECTS_DIR / slug / pdf_name
            if pdf_path.exists():
                st.download_button(
                    label=f"Download {pdf_name}",
                    data=pdf_path.read_bytes(),
                    file_name=pdf_name,
                    mime="application/pdf",
                    use_container_width=True,
                )

        if sheet_url:
            st.markdown("#### Live Dataset")
            st.link_button("Open Google Sheet", sheet_url, use_container_width=True)

        # Data files
        _, others = list_project_files(slug)
        if others:
            st.markdown("### Data / assets")
            for p in others:
                mime = "application/octet-stream"
                if p.suffix.lower() == ".xlsx":
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif p.suffix.lower() == ".csv":
                    mime = "text/csv"
                elif p.suffix.lower() in (".png", ".jpg", ".jpeg"):
                    mime = f"image/{p.suffix.lower().lstrip('.')}"
                st.download_button(
                    label=f"Download {p.name}",
                    data=p.read_bytes(),
                    file_name=p.name,
                    mime=mime,
                    use_container_width=True,
                )


def _render_multi_report(project):
    slug = project["slug"]
    pdfs_meta = project.get("pdfs", [])

    if not pdfs_meta:
        st.info("No reports configured for this project.")
        return

    labels = [pm["label"] for pm in pdfs_meta]
    chosen_label = st.radio("Select report", labels, horizontal=True, key=f"multi_report_{slug}")
    chosen_meta = next(pm for pm in pdfs_meta if pm["label"] == chosen_label)
    pdf_path = PROJECTS_DIR / slug / chosen_meta["name"]

    col_left, col_right = st.columns([1.6, 1], gap="large")
    with col_left:
        if pdf_path.exists():
            embed_pdf(pdf_path, height=860)
        else:
            st.warning(f"{chosen_meta['name']} not found.")

    with col_right:
        st.markdown("### Downloads")
        for pm in pdfs_meta:
            p = PROJECTS_DIR / slug / pm["name"]
            if p.exists():
                st.download_button(
                    label=f"Download {pm['label']}",
                    data=p.read_bytes(),
                    file_name=pm["name"],
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_{slug}_{pm['name']}",
                )


def _render_report(project):
    slug = project["slug"]
    pdf_name = project.get("pdf_file", "")

    pdfs, others = list_project_files(slug)
    # If a specific pdf_file is given, prioritize it
    if pdf_name:
        specific = PROJECTS_DIR / slug / pdf_name
        if specific.exists():
            pdfs = [specific] + [p for p in pdfs if p.name != pdf_name]

    col_left, col_right = st.columns([1.6, 1], gap="large")
    with col_left:
        if pdfs:
            if len(pdfs) > 1:
                pdf_names = [p.name for p in pdfs]
                chosen = st.selectbox("View report", pdf_names, index=0, key=f"report_select_{slug}")
                chosen_path = next(p for p in pdfs if p.name == chosen)
            else:
                chosen_path = pdfs[0]
            embed_pdf(chosen_path, height=860)
        else:
            st.info("No project preview found.")

    with col_right:
        st.markdown("### Downloads")
        if pdfs:
            for p in pdfs:
                st.download_button(
                    label=f"Download {p.name}",
                    data=p.read_bytes(),
                    file_name=p.name,
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_{slug}_{p.name}",
                )
        if others:
            st.markdown("### Data / assets")
            for p in others:
                mime = "application/octet-stream"
                if p.suffix.lower() == ".xlsx":
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif p.suffix.lower() == ".csv":
                    mime = "text/csv"
                elif p.suffix.lower() in (".png", ".jpg", ".jpeg"):
                    mime = f"image/{p.suffix.lower().lstrip('.')}"
                st.download_button(
                    label=f"Download {p.name}",
                    data=p.read_bytes(),
                    file_name=p.name,
                    mime=mime,
                    use_container_width=True,
                    key=f"dl_{slug}_{p.name}",
                )
