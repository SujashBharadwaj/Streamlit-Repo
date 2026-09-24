"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { label: "Home", href: "/" },
  { label: "Projects", href: "/projects" },
  { label: "Blog", href: "/blog" },
  { label: "About", href: "/about" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div>
        <div className="sidebar-name">Sujash Bharadwaj</div>
        <div className="sidebar-role">Software &amp; ML Engineer</div>
        <span className="version-badge">v3.0.0</span>
      </div>

      <nav className="sidebar-nav">
        {NAV.map((n) => (
          <Link
            key={n.href}
            href={n.href}
            className={`sidebar-link${pathname === n.href ? " active" : ""}`}
          >
            {n.label}
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <a href="mailto:sujashbharadwaj10@gmail.com" title="Email">✉</a>
        <a href="https://github.com/SujashBharadwaj" target="_blank" rel="noopener noreferrer" title="GitHub">GitHub</a>
        <a href="https://www.linkedin.com/in/sujash-bharadwaj-14752827a/" target="_blank" rel="noopener noreferrer" title="LinkedIn">LinkedIn</a>
      </div>
    </aside>
  );
}
