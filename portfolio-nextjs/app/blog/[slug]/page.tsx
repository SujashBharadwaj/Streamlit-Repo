import fs from "fs";
import path from "path";
import Link from "next/link";
import { notFound } from "next/navigation";

type Props = { params: { slug: string } };

function getPostSlugs(): string[] {
  const postsDir = path.join(process.cwd(), "app", "data", "posts");
  if (!fs.existsSync(postsDir)) return [];
  return fs.readdirSync(postsDir).filter((f) => f.endsWith(".md")).map((f) => f.replace(/\.md$/, ""));
}

function loadPost(slug: string) {
  const filePath = path.join(process.cwd(), "app", "data", "posts", slug + ".md");
  if (!fs.existsSync(filePath)) return null;
  const raw = fs.readFileSync(filePath, "utf-8");

  let title = slug;
  let date = "";
  let tags: string[] = [];
  let body = raw;

  if (raw.startsWith("---")) {
    const endIdx = raw.indexOf("---", 3);
    if (endIdx > 0) {
      const frontmatter = raw.slice(3, endIdx);
      body = raw.slice(endIdx + 3).trim();
      for (const line of frontmatter.split("\n")) {
        const [key, ...rest] = line.split(":");
        const val = rest.join(":").trim();
        if (key.trim() === "title") title = val;
        if (key.trim() === "date") date = val;
        if (key.trim() === "tags") tags = val.split(",").map((t) => t.trim());
      }
    }
  }

  // Strip leading heading that duplicates the title
  if (body.startsWith("# ")) {
    const firstNewline = body.indexOf("\n");
    const headingText = body.slice(2, firstNewline > 0 ? firstNewline : undefined).trim();
    if (headingText.toLowerCase() === title.toLowerCase() || headingText.includes(title.slice(0, 20))) {
      body = body.slice(firstNewline > 0 ? firstNewline + 1 : body.length).trim();
    }
  }

  return { title, date, tags, body };
}

function markdownToHtml(md: string): string {
  let html = md;
  html = html.replace(/^### (.*)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.*)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.*)$/gm, '<h1>$1</h1>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  html = html.replace(/^\* (.*)$/gm, '<li>$1</li>');
  html = html.replace(/^- (.*)$/gm, '<li>$1</li>');
  html = html.replace(/((?:<li>.*<\/li>\s*)+)/g, '<ul>$1</ul>');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  html = html.replace(/\n\n/g, '</p><p>');
  html = '<p>' + html + '</p>';
  html = html.replace(/<p>\s*<\/p>/g, '');
  html = html.replace(/<p>\s*<h/g, '<h');
  html = html.replace(/<\/h([1-6])>\s*<\/p>/g, '</h$1>');
  html = html.replace(/<p>\s*<ul>/g, '<ul>');
  html = html.replace(/<\/ul>\s*<\/p>/g, '</ul>');
  return html;
}

export async function generateStaticParams() {
  return getPostSlugs().map((slug) => ({ slug }));
}

export function generateMetadata({ params }: Props) {
  const post = loadPost(params.slug);
  return { title: post ? `${post.title} | Sujash Bharadwaj` : "Blog" };
}

export default function BlogPostPage({ params }: Props) {
  const post = loadPost(params.slug);
  if (!post) notFound();

  const slugs = getPostSlugs().sort().reverse();
  const idx = slugs.indexOf(params.slug);
  const prev = idx < slugs.length - 1 ? slugs[idx + 1] : null;
  const next = idx > 0 ? slugs[idx - 1] : null;

  const contentHtml = markdownToHtml(post.body);

  return (
    <>
      <Link href="/blog" className="btn" style={{ marginBottom: 16, display: "inline-flex" }}>
        ← Back to all posts
      </Link>

      <article>
        <div className="card" style={{ marginTop: 8, marginBottom: 24 }}>
          <h1 style={{ fontSize: "1.5rem" }}>{post.title}</h1>
          <div className="muted" style={{ marginTop: 6, fontSize: "0.88rem" }}>{post.date}</div>
          <div style={{ marginTop: 8 }}>
            {post.tags.map((t) => <span key={t} className="chip">{t}</span>)}
          </div>
        </div>

        <div
          className="card"
          style={{ lineHeight: 1.8 }}
          dangerouslySetInnerHTML={{ __html: contentHtml }}
        />
      </article>

      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 28, borderTop: "1px solid var(--night-border)", paddingTop: 16 }}>
        {prev ? <Link href={`/blog/${prev}`} className="btn">← Previous</Link> : <span />}
        {next ? <Link href={`/blog/${next}`} className="btn">Next →</Link> : <span />}
      </div>
    </>
  );
}
