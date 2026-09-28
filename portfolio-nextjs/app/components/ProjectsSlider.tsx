"use client";
import Link from "next/link";
import { useRef, useState } from "react";

const CATEGORIES = [
  { key: "all", label: "All" },
  { key: "sim", label: "Simulations & Games" },
  { key: "ml", label: "ML & Analytics" },
  { key: "sys", label: "Systems & Tools" },
];

function getCategory(type: string): string {
  if (type === "game") return "sim";
  if (["external", "embed", "report", "multi_report"].includes(type)) return "ml";
  return "sys";
}

interface Project {
  slug: string;
  title: string;
  desc: string;
  eyebrow: string;
  tags: string[];
  type: string;
  github_url?: string;
  live_url?: string;
}

export default function ProjectsSlider({ projects }: { projects: Project[] }) {
  const trackRef = useRef<HTMLDivElement>(null);
  const [cat, setCat] = useState("all");

  const filtered =
    cat === "all" ? projects : projects.filter((p) => getCategory(p.type) === cat);

  const scroll = (dir: number) => {
    trackRef.current?.scrollBy({ left: dir * 340, behavior: "smooth" });
  };

  return (
    <div>
      <div className="filter-bar">
        {CATEGORIES.map((c) => (
          <button
            key={c.key}
            className={`filter-chip${cat === c.key ? " active" : ""}`}
            onClick={() => setCat(c.key)}
          >
            {c.label}
          </button>
        ))}
      </div>

      <div className="slider-wrapper">
        <button className="slider-nav prev" onClick={() => scroll(-1)} aria-label="Previous">
          ‹
        </button>
        <div className="slider-track" ref={trackRef}>
          {filtered.map((p) => (
            <Link key={p.slug} href={`/projects/${p.slug}`} style={{ textDecoration: "none" }}>
              <div className="slider-card">
                <div className="project-card">
                  <div className="eyebrow">{p.eyebrow}</div>
                  <div className="project-title">{p.title}</div>
                  <p className="muted" style={{ fontSize: "0.86rem", marginTop: 4 }}>
                    {p.desc.length > 120 ? p.desc.slice(0, 120) + "…" : p.desc}
                  </p>
                  <div style={{ marginTop: 10 }}>
                    {p.tags.slice(0, 3).map((t: string) => (
                      <span key={t} className="chip">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </Link>
          ))}
          {filtered.length === 0 && (
            <div style={{ padding: 20, color: "var(--text-muted)", fontSize: "0.9rem" }}>
              No projects in this category yet.
            </div>
          )}
        </div>
        <button className="slider-nav next" onClick={() => scroll(1)} aria-label="Next">
          ›
        </button>
      </div>
    </div>
  );
}
