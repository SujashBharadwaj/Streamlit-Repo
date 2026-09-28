"use client";
import Link from "next/link";
import { useRef } from "react";

interface Post {
  slug: string;
  title: string;
  date: string;
  tags: string[];
  excerpt: string;
}

export default function BlogSlider({ posts }: { posts: Post[] }) {
  const trackRef = useRef<HTMLDivElement>(null);

  const scroll = (dir: number) => {
    trackRef.current?.scrollBy({ left: dir * 340, behavior: "smooth" });
  };

  if (posts.length === 0) {
    return <p className="muted">No posts yet.</p>;
  }

  return (
    <div className="slider-wrapper">
      <button className="slider-nav prev" onClick={() => scroll(-1)} aria-label="Previous">
        ‹
      </button>
      <div className="slider-track" ref={trackRef}>
        {posts.map((post) => (
          <Link key={post.slug} href={`/blog/${post.slug}`} style={{ textDecoration: "none" }}>
            <div className="slider-card">
              <div className="card" style={{ minHeight: 150, cursor: "pointer" }}>
                <div style={{ fontSize: "1rem", fontWeight: 600, color: "var(--text-snow)" }}>
                  {post.title}
                </div>
                <div className="muted" style={{ fontSize: "0.76rem", marginTop: 4 }}>
                  {post.date}
                </div>
                <p
                  className="muted"
                  style={{ fontSize: "0.86rem", marginTop: 8, lineHeight: 1.55 }}
                >
                  {post.excerpt.length > 130 ? post.excerpt.slice(0, 130) + "…" : post.excerpt}
                </p>
                <div style={{ marginTop: 8 }}>
                  {post.tags.slice(0, 2).map((t) => (
                    <span key={t} className="chip">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
      <button className="slider-nav next" onClick={() => scroll(1)} aria-label="Next">
        ›
      </button>
    </div>
  );
}
