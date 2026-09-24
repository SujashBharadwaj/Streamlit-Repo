import Link from "next/link";
import { notFound } from "next/navigation";
import projects from "../../data/projects.json";

/* eslint-disable @typescript-eslint/no-explicit-any */

type Props = { params: { slug: string } };

export async function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }: Props) {
  const project = projects.find((p) => p.slug === params.slug);
  return { title: project ? `${project.title} | Sujash Bharadwaj` : "Project" };
}

const BACKSTORIES: Record<string, string> = {
  "flight-tracker-widget": `My friend Rohan Jain lives right next to Mumbai Chhatrapati Shivaji Maharaj International Airport (BOM / VABB). He often hears roaring jet engines overhead and always wondered: "Which flight is that?"

He asked if I could build a dedicated lightweight app that sends him instant desktop notifications whenever a plane of his choice flies over his rooftop.

Instead of building a heavyweight browser tab, I took this as a challenge to engineer a native Windows desktop widget:

• Live Geofencing Engine — Haversine spatial math bounding OpenSky ADS-B telemetry to a 5–30 km radius around Mumbai Airport.

• FlightRadar Reverse Engineering — Analyzed real-time radar data feeds and geofence triggering patterns.

• GPU-Accelerated Native GUI — Microsoft Edge WebView2 (pywebview) + Leaflet.js with CartoDB dark tiles and official SOI composite Indian boundaries.

• Native Windows Toast Notifications — win11toast with smart de-duplication and callsign filtering.

• Power & Data Throttling — Wi-Fi detection to pause polling on battery/mobile data.`,
  "faulty-scientific-calc": `Back in my college days, I used to joke about building a completely faulty scientific calculator. Anyone who has ever prepared for the GATE exam or appeared for a TCS iON virtual test remembers the collective trauma of using their rigid, on-screen exam calculator with a worn-out test center mouse.

I built this satirical web app to recreate the worst possible UX while staying maliciously compliant:

• Broken Mouse Click Resistance — Buttons require 2-4 rapid clicks before registering.

• Keypad Musical Chairs — Numeric buttons scramble their positions.

• Multilingual Script Roulette — Numbers swap into Devanagari or Roman numerals.

• Absurd Math — 1+1 evaluates to sin(90°) + cos(0°).

• Proctor Paranoia Simulator — Periodic warnings about suspicious blinking.`,
  "wall-jump-maze": `I wanted to add interactive displays to my portfolio, and a Pac-Man-inspired mini game felt like a strong way to do it. Built with only HTML, CSS, JavaScript, and the Canvas API — maze generation, pellet collection, ghost AI, and a timed wall-jump ability with cooldown.`,
};

export default function ProjectDetailPage({ params }: Props) {
  const { slug } = params;
  const project = projects.find((p) => p.slug === slug);
  if (!project) notFound();

  const idx = projects.findIndex((p) => p.slug === slug);
  const prev = idx > 0 ? projects[idx - 1] : null;
  const next = idx < projects.length - 1 ? projects[idx + 1] : null;

  const isGame = project.type === "game";
  const isExternal = project.type === "external";
  const isLiveApp = project.type === "live_app";
  const backstory = BACKSTORIES[slug];

  return (
    <>
      <Link href="/projects" className="btn" style={{ marginBottom: 16, display: "inline-flex" }}>
        ← Back to all projects
      </Link>

      <div className="card" style={{ marginTop: 8 }}>
        <div className="eyebrow">{project.eyebrow}</div>
        <div style={{ fontSize: "1.35rem", fontWeight: 800 }}>{project.title}</div>
        <p className="muted" style={{ marginTop: 8 }}>{project.desc}</p>
        <div style={{ marginTop: 10 }}>
          {project.tags.map((t: string) => <span key={t} className="chip">{t}</span>)}
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, marginTop: 16, flexWrap: "wrap" }}>
        {(project as any).github_url && (
          <a href={(project as any).github_url} target="_blank" rel="noopener noreferrer" className="btn">
            💻 GitHub Repo
          </a>
        )}
        {isLiveApp && (project as any).live_url && (
          <a href={(project as any).live_url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            🚀 Launch App
          </a>
        )}
      </div>

      {isGame && (
        <div style={{ marginTop: 24 }}>
          <h3>Interactive Simulation</h3>
          <iframe
            src={`/projects/${slug}/index.html`}
            style={{
              width: "100%",
              height: slug === "faulty-scientific-calc" ? 800 : 700,
              border: "1px solid var(--night-border)",
              borderRadius: 12,
              marginTop: 12,
              background: "#000",
            }}
            title={project.title}
          />
        </div>
      )}

      {isLiveApp && (project as any).live_url && (
        <div style={{ marginTop: 24 }}>
          <h3>Live Interactive App</h3>
          {(project as any).credentials && (
            <div className="card" style={{ padding: "10px 16px", margin: "12px 0", borderLeft: "3px solid var(--celestial-blue)", fontSize: "0.92rem" }}>
              <strong style={{ color: "var(--celestial-blue)" }}>Demo Credentials: </strong>
              {(project as any).credentials.map((c: any) => (
                <span key={c.role} style={{ marginRight: 14 }}>
                  <strong>{c.role}:</strong> <code>{c.username}</code> / <code>{c.password}</code>
                </span>
              ))}
            </div>
          )}
          <iframe
            src={(project as any).live_url}
            style={{ width: "100%", height: 800, border: "1px solid var(--night-border)", borderRadius: 12, marginTop: 12 }}
            title={project.title}
          />
        </div>
      )}

      {isExternal && (project as any).links && (
        <div style={{ marginTop: 24 }}>
          <h3>External Links</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
            {(project as any).links.map((link: any) => (
              <a key={link.url} href={link.url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: "none" }}>
                <div className="card" style={{ minHeight: 80 }}>
                  <div style={{ fontSize: "1rem", fontWeight: 700 }}>{link.label}</div>
                  {link.desc && <p className="muted" style={{ fontSize: "0.88rem", marginTop: 4 }}>{link.desc}</p>}
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {backstory && (
        <div style={{ marginTop: 30 }}>
          <h3>Why I Built This</h3>
          <div className="card" style={{ marginTop: 12, whiteSpace: "pre-wrap", lineHeight: 1.75 }}>
            {backstory}
          </div>
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 32, borderTop: "1px solid var(--night-border)", paddingTop: 16 }}>
        {prev ? <Link href={`/projects/${prev.slug}`} className="btn">← {prev.title}</Link> : <span />}
        {next ? <Link href={`/projects/${next.slug}`} className="btn">{next.title} →</Link> : <span />}
      </div>
    </>
  );
}
