import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar";

export const metadata: Metadata = {
  title: "Sujash Bharadwaj | Software & ML Engineer",
  description:
    "Portfolio and personal blog — Software Engineer at sfhawk Solutions. BSc(Hons) Applied Statistics & Data Analytics (MIT-WPU) + IITM BS.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="starfield-bg">
        <Sidebar />
        <main className="main-content">{children}</main>
      </body>
    </html>
  );
}
