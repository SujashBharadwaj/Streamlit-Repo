import Link from "next/link";
import fs from "fs";
import path from "path";
import projects from "./data/projects.json";
import ProjectsSlider from "./components/ProjectsSlider";
import BlogSlider from "./components/BlogSlider";

/* eslint-disable @typescript-eslint/no-explicit-any */

function loadRecentPosts() {
  const postsDir = path.join(process.cwd(), "app", "data", "posts");
  if (!fs.existsSync(postsDir)) return [];
  const files = fs.readdirSync(postsDir).filter((f) => f.endsWith(".md")).sort().reverse();

  return files.slice(0, 6).map((filename) => {
    const raw = fs.readFileSync(path.join(postsDir, filename), "utf-8");
    const slug = filename.replace(/\.md$/, "");
    let title = slug, date = "", tags: string[] = [], bodyStart = 0;

    if (raw.startsWith("---")) {
      const endIdx = raw.indexOf("---", 3);
      if (endIdx > 0) {
        const fm = raw.slice(3, endIdx);
        bodyStart = endIdx + 3;
        for (const line of fm.split("\n")) {
          const [key, ...rest] = line.split(":");
          const val = rest.join(":").trim();
          if (key.trim() === "title") title = val;
          if (key.trim() === "date") date = val;
          if (key.trim() === "tags") tags = val.split(",").map((t) => t.trim());
        }
      }
    }

    const body = raw.slice(bodyStart).trim();
    const excerpt = body.replace(/^#.*$/gm, "").replace(/\*\*/g, "").replace(/\*/g, "").trim().slice(0, 150);
    return { slug, title, date, tags, excerpt };
  });
}

export default function HomePage() {
  const posts = loadRecentPosts();

  return (
    <>
      {/* Hero */}
      <section style={{ marginBottom: "3rem" }}>
        <h1 className="hero-name">Sujash Bharadwaj</h1>
        <div className="speed-line" />
        <p className="hero-tagline">
          Software Engineer at sfhawk Solutions. Building production systems,
          exploring vision &amp; language models, and keeping things reproducible.
        </p>
        <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
          <Link href="/projects" className="btn btn-primary">Explore Projects</Link>
          <Link href="/blog" className="btn">Read the Blog</Link>
        </div>
      </section>

      {/* Projects Slider */}
      <section className="section">
        <div className="section-title">Projects</div>
        <ProjectsSlider projects={projects as any} />
      </section>

      {/* Blog Slider */}
      {posts.length > 0 && (
        <section className="section">
          <div className="section-title">Writing</div>
          <BlogSlider posts={posts} />
        </section>
      )}

      {/* Current Focus */}
      <section className="section">
        <div className="section-title">Current Focus</div>
        <div className="focus-grid">
          {["Computer Vision", "SLM & VLM", "AI & ML", ".NET & Angular", "React", "Statistics"].map((s) => (
            <span key={s} className="pill">{s}</span>
          ))}
        </div>
      </section>
    </>
  );
}
