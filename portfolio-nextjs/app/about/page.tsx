/* eslint-disable @next/next/no-img-element */
import Image from "next/image";

export const metadata = { title: "About | Sujash Bharadwaj" };

export default function AboutPage() {
  return (
    <>
      <h2>About</h2>

      <div style={{ display: "grid", gridTemplateColumns: "200px 1fr", gap: 32, marginTop: 24, alignItems: "start" }}>
        <Image
          src="/profile.png"
          alt="Sujash Bharadwaj"
          width={200}
          height={200}
          style={{ borderRadius: 16, border: "1px solid var(--night-border)" }}
        />

        <div className="card">
          <div style={{ fontSize: "1.4rem", fontWeight: 900 }}>Hi, I&rsquo;m Sujash.</div>
          <p className="muted" style={{ marginTop: 10, fontSize: "1.05rem" }}>
            I&rsquo;m a Software Engineer at sfhawk Solutions. I graduated with a BSc(Hons) in Applied Statistics &amp; Data Analytics
            from MIT-WPU and hold a BS in Data Science &amp; Applications from IIT Madras.
          </p>
          <p className="muted" style={{ marginTop: 10, fontSize: "1.05rem" }}>
            I&rsquo;m 22 (born 10 Jan 2004). I work across Computer Vision, Small &amp; Vision Language Models, .NET, Angular, and React.
            I like machine learning, AI, math, and statistics.
          </p>
          <p className="muted" style={{ marginTop: 10, fontSize: "1.05rem" }}>
            Outside work: F1 and cricket fan, I go karting and play cricket when I can.
            I&rsquo;m an avid music listener and still log hours on Age of Empires II DE.
          </p>
        </div>
      </div>

      {/* Contact */}
      <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
        <a href="mailto:sujashbharadwaj10@gmail.com" className="btn">✉ Email</a>
        <a href="https://github.com/SujashBharadwaj" target="_blank" rel="noopener noreferrer" className="btn">GitHub</a>
        <a href="https://www.linkedin.com/in/sujash-bharadwaj-14752827a/" target="_blank" rel="noopener noreferrer" className="btn">LinkedIn</a>
      </div>

      <hr style={{ borderColor: "var(--night-border)", margin: "28px 0" }} />

      <h3>Focus &amp; Skills</h3>
      <div style={{ marginTop: 12 }}>
        {["Python", ".NET", "Angular", "React", "Computer Vision", "SLM & VLM", "Pandas", "FastAPI", "Scikit-learn", "EDA & Visualization", "ML Pipelines", "Vector DB basics"].map(s => (
          <span key={s} className="pill">{s}</span>
        ))}
      </div>
    </>
  );
}
