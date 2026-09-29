"use client";

import React, { useState, useRef, useEffect } from "react";

export default function GradientDescentPlayground() {
  const [a3, setA3] = useState(0.0);
  const [a2, setA2] = useState(1.0);
  const [a1, setA1] = useState(0.0);
  const [a0, setA0] = useState(0.0);
  const [x0, setX0] = useState(2.0);
  const [alpha, setAlpha] = useState(0.2);
  const [maxSteps, setMaxSteps] = useState(20);
  const [roundSteps, setRoundSteps] = useState(true);
  const [tol, setTol] = useState(0.01);

  const [history, setHistory] = useState<{ step: number; x: number; fx: number; dfx: number }[]>([]);
  const [diverged, setDiverged] = useState(false);

  const canvasRef = useRef<HTMLCanvasElement>(null);

  const f = (x: number) => a3 * x * x * x + a2 * x * x + a1 * x + a0;
  const df = (x: number) => 3 * a3 * x * x + 2 * a2 * x + a1;

  const runSimulation = (steps: number) => {
    let currentX = x0;
    const newHistory = [];
    let isDiverged = false;

    for (let i = 0; i <= steps; i++) {
      const fx = f(currentX);
      const dfx = df(currentX);
      newHistory.push({ step: i, x: currentX, fx, dfx });

      if (Math.abs(dfx) < tol) break;

      currentX = currentX - alpha * dfx;
      if (roundSteps) currentX = Math.round(currentX * 100) / 100;

      if (Math.abs(currentX) > 1e9) {
        isDiverged = true;
        break;
      }
    }
    setHistory(newHistory);
    setDiverged(isDiverged);
  };

  useEffect(() => {
    // Initial run on mount
    runSimulation(0);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);

    if (history.length === 0) return;

    // Determine bounds
    let minX = history[0].x, maxX = history[0].x;
    for (const h of history) {
      if (h.x < minX) minX = h.x;
      if (h.x > maxX) maxX = h.x;
    }
    const padding = Math.max(2, (maxX - minX) * 0.5);
    minX -= padding;
    maxX += padding;

    // Sample function to find Y bounds
    const samples = 100;
    let minY = f(minX), maxY = f(minX);
    const curvePoints = [];
    for (let i = 0; i <= samples; i++) {
      const x = minX + (i / samples) * (maxX - minX);
      const y = f(x);
      curvePoints.push({ x, y });
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }

    const yPadding = Math.max(1, (maxY - minY) * 0.2);
    minY -= yPadding;
    maxY += yPadding;

    const mapX = (x: number) => ((x - minX) / (maxX - minX)) * width;
    const mapY = (y: number) => height - ((y - minY) / (maxY - minY)) * height;

    // Draw axes
    ctx.strokeStyle = "rgba(255,255,255,0.1)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, mapY(0));
    ctx.lineTo(width, mapY(0));
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(mapX(0), 0);
    ctx.lineTo(mapX(0), height);
    ctx.stroke();

    // Draw curve
    ctx.strokeStyle = "#20A4F3";
    ctx.lineWidth = 2;
    ctx.beginPath();
    curvePoints.forEach((p, i) => {
      if (i === 0) ctx.moveTo(mapX(p.x), mapY(p.y));
      else ctx.lineTo(mapX(p.x), mapY(p.y));
    });
    ctx.stroke();

    // Draw descent points
    history.forEach((h, i) => {
      ctx.fillStyle = i === history.length - 1 ? "#FF3366" : "#2EC4B6";
      ctx.beginPath();
      ctx.arc(mapX(h.x), mapY(h.fx), 4, 0, 2 * Math.PI);
      ctx.fill();

      if (i > 0) {
        ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(mapX(history[i - 1].x), mapY(history[i - 1].fx));
        ctx.lineTo(mapX(h.x), mapY(h.fx));
        ctx.stroke();
        ctx.setLineDash([]);
      }
    });
  }, [history, a3, a2, a1, a0]); // Re-draw on history or function change

  return (
    <div className="card" style={{ marginTop: "1rem" }}>
      <h3 style={{ margin: "0 0 16px 0", fontSize: "1.25rem", color: "var(--neon-pink)" }}>Interactive Gradient Descent</h3>
      <p className="muted" style={{ fontSize: "0.95rem", marginBottom: "16px" }}>
        Define f(x) = a₃x³ + a₂x² + a₁x + a₀ and simulate gradient descent.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(80px, 1fr))", gap: "12px", marginBottom: "16px" }}>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>a₃</label>
          <input type="number" step="0.1" value={a3} onChange={(e) => setA3(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>a₂</label>
          <input type="number" step="0.1" value={a2} onChange={(e) => setA2(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>a₁</label>
          <input type="number" step="0.1" value={a1} onChange={(e) => setA1(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>a₀</label>
          <input type="number" step="0.1" value={a0} onChange={(e) => setA0(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: "12px", marginBottom: "20px" }}>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Initial x₀</label>
          <input type="number" step="0.1" value={x0} onChange={(e) => setX0(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Learning rate α</label>
          <input type="number" step="0.01" value={alpha} onChange={(e) => setAlpha(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Max Steps</label>
          <input type="number" value={maxSteps} onChange={(e) => setMaxSteps(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div style={{ display: "flex", alignItems: "center", paddingTop: "20px" }}>
          <label style={{ display: "flex", alignItems: "center", fontSize: "0.85rem", cursor: "pointer" }}>
            <input type="checkbox" checked={roundSteps} onChange={(e) => setRoundSteps(e.target.checked)} style={{ marginRight: "8px" }} />
            Round steps
          </label>
        </div>
      </div>

      <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
        <button className="btn" onClick={() => runSimulation(history.length > 0 ? history[history.length - 1].step + 1 : 1)}>
          Step once
        </button>
        <button className="btn" onClick={() => runSimulation(maxSteps)}>
          Run to Convergence
        </button>
        <button className="btn" style={{ background: "transparent", border: "1px solid var(--border-subtle)" }} onClick={() => runSimulation(0)}>
          Reset
        </button>
      </div>

      {diverged && (
        <div style={{ padding: "12px", borderRadius: "6px", background: "rgba(255, 51, 102, 0.1)", border: "1px solid var(--border-hover)", marginBottom: "16px", color: "var(--neon-pink)", fontSize: "0.9rem" }}>
          The run diverged. Try a smaller learning rate!
        </div>
      )}

      <div style={{ width: "100%", height: "250px", border: "1px solid var(--border-subtle)", borderRadius: "8px", overflow: "hidden", background: "var(--surface)", marginBottom: "20px" }}>
        <canvas ref={canvasRef} width={800} height={250} style={{ width: "100%", height: "100%", display: "block" }} />
      </div>

      <div className="table-wrapper">
        <table style={{ width: "100%", fontSize: "0.85rem", textAlign: "left", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
              <th style={{ padding: "8px" }}>Step</th>
              <th style={{ padding: "8px" }}>x</th>
              <th style={{ padding: "8px" }}>f(x)</th>
              <th style={{ padding: "8px" }}>f'(x)</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h, i) => (
              <tr key={i} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                <td style={{ padding: "8px" }}>{h.step}</td>
                <td style={{ padding: "8px" }}>{h.x.toFixed(4)}</td>
                <td style={{ padding: "8px" }}>{h.fx.toFixed(4)}</td>
                <td style={{ padding: "8px" }}>{h.dfx.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
