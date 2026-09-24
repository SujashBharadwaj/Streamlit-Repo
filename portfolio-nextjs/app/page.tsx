import Link from "next/link";
import projects from "./data/projects.json";

export default function HomePage() {
  const featured = projects[0];

  return (
    <>
      {/* Hero */}
      <section style={{ marginBottom: "3rem" }}>
        <h1>Sujash Bharadwaj&rsquo;s Portfolio</h1>
        <p className="muted" style={{ marginTop: 10, fontSize: "1.12rem", maxWidth: 680 }}>
          Software Engineer at sfhawk Solutions. BSc(Hons) Applied Statistics &amp;
          Data Analytics (MIT-WPU) + IITM BS (Data Science &amp; Applications).
          I build practical projects, write what I learn, and keep things reproducible.
        </p>

        <div style={{ display: "flex", gap: 12, marginTop: 20 }}>
          <Link href="/projects" className="btn btn-primary">Explore Projects</Link>
          <Link href="/blog" className="btn">Read the Blog</Link>
        </div>
      </section>

      {/* Featured Project */}
      <section style={{ marginBottom: "2.5rem" }}>
        <h3>Latest Project</h3>
        <div className="card" style={{ marginTop: 12 }}>
          <div className="eyebrow">{featured.eyebrow}</div>
          <div className="project-title">{featured.title}</div>
          <p className="muted" style={{ fontSize: "0.95rem" }}>{featured.desc}</p>
          <div style={{ marginTop: 10 }}>
            {featured.tags.map((t: string) => (
              <span key={t} className="chip">{t}</span>
            ))}
          </div>
          <div style={{ marginTop: 14 }}>
            <Link href={`/projects/${featured.slug}`} className="btn">Open Project</Link>
          </div>
        </div>
      </section>

      {/* What I'm doing now */}
      <section>
        <h3>What I&rsquo;m Doing Now</h3>
        <div style={{ marginTop: 10 }}>
          {["Computer Vision", "SLM & VLM", "AI & ML", "Creative Web Apps", ".NET & Angular", "React", "Statistics", "Reproducible Notebooks"].map(s => (
            <span key={s} className="pill">{s}</span>
          ))}
        </div>
        <p className="muted" style={{ marginTop: 14 }}>
          Building production systems, exploring vision &amp; language models, and writing about what I learn along the way.
        </p>
      </section>
    </>
  );
}
