# Streamlit Portfolio Audit Report

## 1. Security Audit

### 🛑 High Severity: XSS via `unsafe_allow_html=True`
- **Location**: `views/blog.py` (lines 70, 75, 78, 84, 87, 93, 95), `Homepage.py`, `utils/helpers.py`.
- **Issue**: The application heavily relies on `st.markdown(..., unsafe_allow_html=True)` to render markdown content loaded from local `.md` files. While the current blog posts are trusted (written by the owner), if this application is ever extended to accept external inputs (e.g., comments, external project submissions) or if an attacker manages to compromise the repository's markdown files, this will lead to a **Cross-Site Scripting (XSS)** vulnerability.
- **Recommendation**: Avoid `unsafe_allow_html=True` for any content that isn't strictly static UI layout. Streamlit's native `st.markdown` (without the flag) natively supports most markdown features safely. If custom HTML is strictly required, ensure the markdown is passed through a robust HTML sanitizer (like `bleach`) before rendering.

### ⚠️ Medium Severity: Potential Path Traversal in Image Resolution
- **Location**: `utils/helpers.py` -> `resolve_markdown_images()`
- **Issue**: The function manually resolves paths (`(base_dir / rel_path).resolve()`). While it checks if the resolved path has a specific image suffix (`.png`, `.jpg`, `.jpeg`, `.gif`), it does not explicitly enforce that the resolved path stays within the `ASSETS` or `ROOT` directories. 
- **Recommendation**: Enforce a directory jail check. After resolving the path, ensure `resolved_path.is_relative_to(ROOT)` is `True` before reading the file bytes.

### ℹ️ Low Severity / Best Practice: Open/Dynamic File Embedding
- **Location**: `utils/helpers.py` -> `embed_pdf()`
- **Issue**: The `embed_pdf` function reads file contents and renders them directly into a JS script block as base64 strings. Since the files are controlled by the author, this is safe. However, dynamically interpolating strings into `<script>` blocks can be risky if any of those strings become user-controlled.
- **Recommendation**: Maintain strict access control over the `projects_static` directory.

---

## 2. UI/UX Audit

### ✅ The Good
- **Premium Aesthetics**: The custom CSS injected in `Homepage.py` applies a very polished, modern dark theme. The use of CSS variables, linear gradients on cards, and subtle hover animations (`transform: translateY(-1px)`) gives the site a premium feel.
- **Typography**: The combination of `Crimson Text` (serif) for body text and `Oswald` (sans-serif) for headers provides a highly readable and elegant contrast.
- **SPA Feel**: Utilizing `st.session_state` for navigation avoids full page reloads, providing a smooth Single Page Application experience within Streamlit.
- **PDF Handling**: The custom `pdf.js` canvas renderer (`embed_pdf`) is an excellent UX workaround to bypass Chrome's sandboxed iframe restrictions, ensuring PDFs always display properly without forcing a download.

### 🔶 Areas for Improvement (Friction Points)
- **Blog Navigation**: Currently, the blog uses an `st.selectbox` to choose posts after filtering. If the number of posts grows, a selectbox becomes unwieldy. 
  - *UX Fix*: Switch to a card-based grid layout or a paginated list for blog posts, allowing users to scroll and click on a post card to view it.
- **Search Interaction**: The search bar (`st.text_input`) in the blog requires the user to hit "Enter" or click outside to trigger the filter due to Streamlit's execution model.
  - *UX Fix*: This is a limitation of Streamlit, but you can improve it slightly by adding a visually distinct "Search" button or using Streamlit's newer `@st.fragment` (or form submission) to isolate the search rerun from the rest of the app.
- **Streamlit "Jank"**: Navigating between pages will always trigger the top-right "Running..." indicator and a brief flash. 
  - *UX Fix*: While inherent to Streamlit, you can mitigate visual disruption by ensuring components load as fast as possible (e.g., caching the file reads in `load_posts()` and `load_projects()` using `@st.cache_data`). Currently, the app re-reads all markdown files and the JSON file from the disk on *every single interaction*.

---

## 3. Summary of Recommendations
1. **Sanitize Markdown**: If you must use `unsafe_allow_html=True`, integrate `bleach` to strip malicious `<script>` tags from the markdown content.
2. **Cache Data Loading**: Add `@st.cache_data` to `load_posts()` and `load_projects()` to drastically improve page load times and UX responsiveness.
3. **Jail Image Paths**: Add `is_relative_to(ROOT)` in the image resolver to prevent arbitrary file reads.
4. **Redesign Blog List**: Move away from `st.selectbox` for blog navigation and use clickable `st.button` cards instead.
