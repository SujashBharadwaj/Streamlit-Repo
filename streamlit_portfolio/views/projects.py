import streamlit as st
import streamlit.components.v1 as components
from utils.helpers import load_projects, list_project_files, read_project_embed_html, embed_pdf, sanitize_html, PROJECTS_DIR


def projects_view():
    projects = load_projects()

    st.markdown("## Projects")
    st.markdown(sanitize_html('<div class="muted">Reports, dashboards, and interactive builds with downloadable outputs.</div>'), unsafe_allow_html=True)
    st.markdown("")

    if not projects:
        st.info("No projects found.")
        return

    slugs = [p["slug"] for p in projects]
    if st.session_state.get("selected_project") not in slugs:
        st.session_state["selected_project"] = projects[0]["slug"]

    # --- Project grid ---
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
                st.rerun()

    # --- Detail view ---
    st.markdown("")
    titles = [p["title"] for p in projects]
    slug_by_title = {p["title"]: p["slug"] for p in projects}
    selected_title = next(p["title"] for p in projects if p["slug"] == st.session_state["selected_project"])
    selected_title = st.selectbox("Quick jump", titles, index=titles.index(selected_title), key="project_selectbox")

    slug = slug_by_title[selected_title]
    st.session_state["selected_project"] = slug
    project = next(p for p in projects if p["slug"] == slug)

    # Detail card
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

    ptype = project.get("type", "report")

    # --- Type: game ---
    if ptype == "game":
        _render_game(project)
    elif ptype == "embed":
        _render_embed(project)
    elif ptype == "multi_report":
        _render_multi_report(project)
    else:
        _render_report(project)


def _render_game(project):
    slug = project["slug"]
    html_file = project.get("html_file", "index.html")
    html = read_project_embed_html(slug, html_file)
    if html:
        st.markdown("#### Play the game")
        components.html(html, height=750, scrolling=False)

        html_path = PROJECTS_DIR / slug / html_file
        st.download_button(
            label="Download game HTML",
            data=html_path.read_bytes(),
            file_name=html_file,
            mime="text/html",
            use_container_width=True,
        )
    else:
        st.info("Game file not found.")

    st.markdown("")
    st.markdown("### Why I Built This")
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
