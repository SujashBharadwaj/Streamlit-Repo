import fs from "fs";
import path from "path";
import Link from "next/link";

export const metadata = { title: "Blog | Sujash Bharadwaj" };

interface Post {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  excerpt: string;
}

function loadPosts(): Post[] {
  const postsDir = path.join(process.cwd(), "app", "data", "posts");
  if (!fs.existsSync(postsDir)) return [];

  const files = fs.readdirSync(postsDir).filter((f) => f.endsWith(".md")).sort().reverse();

  return files.map((filename) => {
    const raw = fs.readFileSync(path.join(postsDir, filename), "utf-8");
    const slug = filename.replace(/\.md$/, "");

    // Parse simple YAML frontmatter
    let title = slug;
    let date = "";
    let tags: string[] = [];
    let bodyStart = 0;

    if (raw.startsWith("---")) {
      const endIdx = raw.indexOf("---", 3);
      if (endIdx > 0) {
        const frontmatter = raw.slice(3, endIdx);
        bodyStart = endIdx + 3;
        for (const line of frontmatter.split("\n")) {
          const [key, ...rest] = line.split(":");
          const val = rest.join(":").trim();
          if (key.trim() === "title") title = val;
          if (key.trim() === "date") date = val;
          if (key.trim() === "tags") tags = val.split(",").map((t) => t.trim());
        }
      }
    }

    const body = raw.slice(bodyStart).trim();
    const excerpt = body
      .replace(/^#.*$/gm, "")
      .replace(/\*\*/g, "")
      .replace(/\*/g, "")
      .trim()
      .slice(0, 180);

    return { slug, title, date, tags, excerpt };
  });
}

export default function BlogPage() {
  const posts = loadPosts();

  return (
    <>
      <h2>Blog</h2>
      <p className="muted" style={{ marginBottom: 24 }}>Short learning notes and project logs.</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 14 }}>
        {posts.map((post) => (
          <Link key={post.slug} href={`/blog/${post.slug}`} style={{ textDecoration: "none" }}>
            <div className="card" style={{ minHeight: 130, cursor: "pointer" }}>
              <div style={{ fontSize: "1.08rem", fontWeight: 700 }}>{post.title}</div>
              <div className="muted" style={{ fontSize: "0.82rem", marginTop: 4 }}>{post.date}</div>
              <p className="muted" style={{ fontSize: "0.92rem", marginTop: 6 }}>{post.excerpt}…</p>
              <div style={{ marginTop: 8 }}>
                {post.tags.slice(0, 3).map((t) => <span key={t} className="chip">{t}</span>)}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </>
  );
}
