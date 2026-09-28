import fs from "fs";
import path from "path";
import BlogSlider from "../components/BlogSlider";

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
      <p className="muted" style={{ marginBottom: 20 }}>Short learning notes and project logs.</p>
      <BlogSlider posts={posts} />
    </>
  );
}
