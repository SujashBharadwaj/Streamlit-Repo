"use client";

import React, { useState } from "react";

function computeOEE(plannedTimeMin: number, downtimeMin: number, totalCount: number, goodCount: number, cycleTimeSec: number) {
  const plannedTimeSec = plannedTimeMin * 60;
  const downtimeSec = downtimeMin * 60;
  const runTimeSec = plannedTimeSec - downtimeSec;

  if (plannedTimeSec <= 0 || runTimeSec <= 0 || totalCount <= 0 || goodCount < 0) {
    return { availability: 0, performance: 0, quality: 0, oee: 0 };
  }

  const availability = Math.max(0, Math.min(1, runTimeSec / plannedTimeSec));
  const performance = Math.max(0, Math.min(1, (totalCount * cycleTimeSec) / runTimeSec));
  const quality = Math.max(0, Math.min(1, goodCount / totalCount));

  return {
    availability,
    performance,
    quality,
    oee: availability * performance * quality,
  };
}

export default function OEEPlayground() {
  const [plannedTime, setPlannedTime] = useState(480);
  const [downtime, setDowntime] = useState(45);
  const [totalCount, setTotalCount] = useState(1200);
  const [scrap, setScrap] = useState(50);
  const [cycleTime, setCycleTime] = useState(20);

  const goodCount = Math.max(0, totalCount - scrap);
  const metrics = computeOEE(plannedTime, downtime, totalCount, goodCount, cycleTime);

  const losses = {
    "Availability (downtime, setups)": 1 - metrics.availability,
    "Performance (micro-stops, slow cycles)": 1 - metrics.performance,
    "Quality (scrap, rework)": 1 - metrics.quality,
  };

  const worstLossKey = Object.keys(losses).reduce((a, b) => (losses[a as keyof typeof losses] > losses[b as keyof typeof losses] ? a : b));
  const worstLossVal = losses[worstLossKey as keyof typeof losses];

  const handleRandomize = () => {
    setPlannedTime([420, 450, 480][Math.floor(Math.random() * 3)]);
    setDowntime(Math.floor(Math.random() * (90 - 15 + 1) + 15));
    const newTotal = Math.floor(Math.random() * (1600 - 700 + 1) + 700);
    setTotalCount(newTotal);
    setScrap(Math.floor(Math.random() * (newTotal * 0.12)));
    setCycleTime([18, 20, 22, 24, 26][Math.floor(Math.random() * 5)]);
  };

  return (
    <div className="card" style={{ marginTop: "1rem" }}>
      <h3 style={{ margin: "0 0 16px 0", fontSize: "1.25rem", color: "var(--neon-teal)" }}>Interactive OEE Simulator</h3>
      <p className="muted" style={{ fontSize: "0.95rem", marginBottom: "16px" }}>
        Adjust shift inputs or randomize to see how OEE and the biggest loss driver react.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "12px", marginBottom: "20px" }}>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Planned Time (min)</label>
          <input type="number" value={plannedTime} onChange={(e) => setPlannedTime(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Downtime (min)</label>
          <input type="number" value={downtime} onChange={(e) => setDowntime(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Total Count</label>
          <input type="number" value={totalCount} onChange={(e) => setTotalCount(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Scrap Count</label>
          <input type="number" value={scrap} onChange={(e) => setScrap(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "4px" }}>Ideal Cycle (sec)</label>
          <input type="number" value={cycleTime} onChange={(e) => setCycleTime(Number(e.target.value))} className="input-field" style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", background: "var(--surface-2)", color: "white" }} />
        </div>
      </div>

      <button onClick={handleRandomize} className="btn" style={{ marginBottom: "20px" }}>
        Randomize Scenario
      </button>

      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", marginBottom: "20px" }}>
        <div style={{ flex: 1, minWidth: "120px", padding: "16px", background: "var(--surface-2)", borderRadius: "8px", borderLeft: "4px solid var(--neon-teal)" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>Availability</div>
          <div style={{ fontSize: "1.75rem", fontWeight: "bold" }}>{(metrics.availability * 100).toFixed(1)}%</div>
        </div>
        <div style={{ flex: 1, minWidth: "120px", padding: "16px", background: "var(--surface-2)", borderRadius: "8px", borderLeft: "4px solid var(--neon-blue)" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>Performance</div>
          <div style={{ fontSize: "1.75rem", fontWeight: "bold" }}>{(metrics.performance * 100).toFixed(1)}%</div>
        </div>
        <div style={{ flex: 1, minWidth: "120px", padding: "16px", background: "var(--surface-2)", borderRadius: "8px", borderLeft: "4px solid var(--neon-pink)" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>Quality</div>
          <div style={{ fontSize: "1.75rem", fontWeight: "bold" }}>{(metrics.quality * 100).toFixed(1)}%</div>
        </div>
        <div style={{ flex: 1, minWidth: "120px", padding: "16px", background: "rgba(32, 164, 243, 0.1)", borderRadius: "8px", border: "1px solid var(--neon-blue)" }}>
          <div style={{ fontSize: "0.85rem", color: "var(--neon-blue)" }}>Overall OEE</div>
          <div style={{ fontSize: "2rem", fontWeight: "bold", color: "var(--text-snow)" }}>{(metrics.oee * 100).toFixed(1)}%</div>
        </div>
      </div>

      <div style={{ padding: "16px", borderRadius: "8px", background: "rgba(255, 51, 102, 0.05)", border: "1px solid var(--border-hover)" }}>
        <h4 style={{ margin: "0 0 8px 0", color: "var(--neon-pink)" }}>Diagnostics: {worstLossKey}</h4>
        <p style={{ margin: 0, fontSize: "0.95rem" }}>
          {worstLossVal < 0.04 && "This is a highly optimized run. Focus on small continuous improvements."}
          {worstLossVal >= 0.04 && worstLossKey.includes("Availability") && "Availability is the main limiter. Reduce unplanned stops, improve changeovers, and shorten maintenance response time."}
          {worstLossVal >= 0.04 && worstLossKey.includes("Performance") && "Performance is the main limiter. Hunt micro-stops and speed losses: feeding issues, small jams, slow cycles, and drift from the ideal."}
          {worstLossVal >= 0.04 && worstLossKey.includes("Quality") && "Quality is the main limiter. Focus on defect root causes, startup stability, process parameters, and catching issues earlier."}
        </p>
      </div>
    </div>
  );
}
