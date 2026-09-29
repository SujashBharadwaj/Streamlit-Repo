"use client";

import React, { useState } from "react";

function parseNumericList(str: string): number[] {
  return str
    .split(/[\s,]+/)
    .map((s) => s.trim())
    .filter(Boolean)
    .map(Number)
    .filter((n) => Number.isFinite(n));
}

function computeMeans(values: number[], weights: number[], trimPct: number, p: number) {
  const out: Record<string, number> = {};
  const n = values.length;
  if (n === 0) return out;

  out["Arithmetic"] = values.reduce((a, b) => a + b, 0) / n;
  out["RMS"] = Math.sqrt(values.reduce((a, b) => a + b * b, 0) / n);

  const allPositive = values.every((v) => v > 0);
  if (allPositive) {
    out["Geometric"] = Math.exp(values.reduce((a, b) => a + Math.log(b), 0) / n);
    const denom = values.reduce((a, b) => a + 1.0 / b, 0);
    if (denom !== 0) out["Harmonic"] = n / denom;
  }

  if (p === 0 && allPositive) {
    out["Power (Mp)"] = out["Geometric"];
  } else if (values.every((v) => v >= 0) || Math.abs(p - Math.round(p)) < 1e-9) {
    out["Power (Mp)"] = Math.pow(
      values.reduce((a, b) => a + Math.pow(b, p), 0) / n,
      1.0 / p
    );
  }

  if (values.every((v) => v >= 0) && values.reduce((a, b) => a + b, 0) > 0) {
    out["Contraharmonic"] = values.reduce((a, b) => a + b * b, 0) / values.reduce((a, b) => a + b, 0);
  }

  if (weights.length === n && weights.reduce((a, b) => a + b, 0) !== 0) {
    out["Weighted"] = values.reduce((a, b, i) => a + b * weights[i], 0) / weights.reduce((a, b) => a + b, 0);
  }

  const sortedVals = [...values].sort((a, b) => a - b);
  const k = Math.floor((n * Math.max(0, Math.min(40, trimPct))) / 100.0);
  if (2 * k < n) {
    const trimmed = sortedVals.slice(k, n - k);
    out["Trimmed"] = trimmed.reduce((a, b) => a + b, 0) / trimmed.length;
  }

  return out;
}

export default function MeansPlayground() {
  const [rawValues, setRawValues] = useState("1, 2, 8");
  const [rawWeights, setRawWeights] = useState("");
  const [trimPct, setTrimPct] = useState(0);
  const [pVal, setPVal] = useState(1.0);
  const [selected, setSelected] = useState<string[]>(["Arithmetic", "Geometric", "Harmonic", "RMS", "Power (Mp)"]);

  const values = parseNumericList(rawValues);
  const weights = parseNumericList(rawWeights);
  const bundle = computeMeans(values, weights, trimPct, pVal);
  const am = bundle["Arithmetic"];

  const toggleSelect = (key: string) => {
    setSelected((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]));
  };

  const options = ["Arithmetic", "Geometric", "Harmonic", "RMS", "Contraharmonic", "Weighted", "Trimmed", "Power (Mp)"];
  const maxVal = Math.max(...Object.values(bundle).filter((v) => !isNaN(v)), 0) || 1;

  return (
    <div className="card" style={{ marginTop: "1rem" }}>
      <h3 style={{ margin: "0 0 16px 0", fontSize: "1.25rem", color: "var(--neon-blue)" }}>Interactive Means Comparator</h3>
      <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "1fr 1fr" }}>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Numbers (comma separated)</label>
          <input type="text" value={rawValues} onChange={(e) => setRawValues(e.target.value)} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Weights (optional)</label>
          <input type="text" value={rawWeights} onChange={(e) => setRawWeights(e.target.value)} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Trim Percent: {trimPct}%</label>
          <input type="range" min="0" max="40" value={trimPct} onChange={(e) => setTrimPct(Number(e.target.value))} style={{ width: "100%" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Power Mean (p): {pVal}</label>
          <input type="range" min="-2" max="4" step="0.1" value={pVal} onChange={(e) => setPVal(Number(e.target.value))} style={{ width: "100%" }} />
        </div>
      </div>

      <div style={{ marginTop: "16px", display: "flex", flexWrap: "wrap", gap: "8px" }}>
        {options.map((opt) => (
          <button
            key={opt}
            onClick={() => toggleSelect(opt)}
            style={{
              padding: "4px 12px",
              borderRadius: "99px",
              border: `1px solid ${selected.includes(opt) ? "var(--neon-blue)" : "var(--border-subtle)"}`,
              background: selected.includes(opt) ? "rgba(32, 164, 243, 0.2)" : "transparent",
              color: selected.includes(opt) ? "var(--text-snow)" : "var(--text-muted)",
              cursor: "pointer",
              fontSize: "0.85rem",
            }}
          >
            {opt}
          </button>
        ))}
      </div>

      <div style={{ marginTop: "24px" }}>
        {selected.map((key) => {
          if (bundle[key] === undefined) return null;
          const val = bundle[key];
          const pct = Math.max(0, (val / maxVal) * 100);
          return (
            <div key={key} style={{ marginBottom: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "4px" }}>
                <span>{key}</span>
                <span style={{ color: "var(--neon-teal)" }}>{val.toFixed(4)}</span>
              </div>
              <div style={{ width: "100%", height: "8px", background: "var(--surface-2)", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{ width: `${pct}%`, height: "100%", background: "var(--neon-blue)", transition: "width 0.3s" }} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="table-wrapper" style={{ marginTop: "24px" }}>
        <table style={{ width: "100%", fontSize: "0.9rem", textAlign: "left", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
              <th style={{ padding: "8px" }}>Mean</th>
              <th style={{ padding: "8px" }}>Value</th>
              <th style={{ padding: "8px" }}>Δ from AM</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(bundle).map(([key, val]) => (
              <tr key={key} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                <td style={{ padding: "8px" }}>{key}</td>
                <td style={{ padding: "8px" }}>{val.toFixed(4)}</td>
                <td style={{ padding: "8px", color: am && val < am ? "var(--neon-pink)" : "var(--neon-teal)" }}>
                  {am !== undefined ? (val - am).toFixed(4) : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
