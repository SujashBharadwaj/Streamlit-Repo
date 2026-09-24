import Link from "next/link";
import projects from "../data/projects.json";

export const metadata = { title: "Projects | Sujash Bharadwaj" };

export default function ProjectsPage() {
  return (
    <>
      <h2>Projects</h2>
      <p className="muted" style={{ marginBottom: 24 }}>
        Reports, dashboards, interactive builds, and open-source tools.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))", gap: 16 }}>
        {projects.map((p) => (
          <Link key={p.slug} href={`/projects/${p.slug}`} style={{ textDecoration: "none" }}>
            <div className="project-card">
              <div className="eyebrow">{p.eyebrow}</div>
              <div className="project-title">{p.title}</div>
              <p className="muted" style={{ fontSize: "0.9rem", marginTop: 4 }}>
                {p.desc.length > 140 ? p.desc.slice(0, 140) + "…" : p.desc}
              </p>
              <div style={{ marginTop: 10 }}>
                {p.tags.slice(0, 4).map((t: string) => (
                  <span key={t} className="chip">{t}</span>
                ))}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </>
  );
}
