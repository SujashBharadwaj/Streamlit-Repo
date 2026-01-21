# Streamlit Portfolio (Forest + Lime)

## Run locally
```bash
pip install -r requirements.txt
streamlit run Homepage.py
```

## Deploy (Streamlit Community Cloud)
- Push this folder to a GitHub repo
- In Streamlit Cloud, set the main file to: `Homepage.py`
- It will pick up the theme from `.streamlit/config.toml`

## Notes
- Blog posts are stored in `/posts` as Markdown.
- Original static site files were kept in:
  - `/blog_static`
  - `/projects_static`
  - `/about_static`
