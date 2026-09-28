import projects from "../data/projects.json";
import ProjectsSlider from "../components/ProjectsSlider";

/* eslint-disable @typescript-eslint/no-explicit-any */

export const metadata = { title: "Projects | Sujash Bharadwaj" };

export default function ProjectsPage() {
  return (
    <>
      <h2>Projects</h2>
      <p className="muted" style={{ marginBottom: 20 }}>
        Reports, dashboards, interactive builds, and open-source tools.
      </p>
      <ProjectsSlider projects={projects as any} />
    </>
  );
}
