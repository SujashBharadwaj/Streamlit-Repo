"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

export default function MathRenderer() {
  const pathname = usePathname();

  useEffect(() => {
    let timeoutId: any;
    const renderMath = () => {
      if (typeof window !== "undefined" && (window as any).MathJax && (window as any).MathJax.typesetPromise) {
        (window as any).MathJax.typesetClear();
        (window as any).MathJax.typesetPromise().catch((err: any) => console.log('MathJax error:', err));
      } else {
        timeoutId = setTimeout(renderMath, 100);
      }
    };
    renderMath();
    return () => clearTimeout(timeoutId);
  }, [pathname]); // Run on mount and path change

  return null;
}
