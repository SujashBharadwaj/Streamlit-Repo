import math
import streamlit as st
from typing import Dict, List
from utils.helpers import parse_numeric_list, sanitize_html


def compute_means_bundle(values: List[float], weights: List[float], trim_pct: float, p: float) -> Dict[str, float]:
    out: Dict[str, float] = {}
    n = len(values)
    if n == 0:
        return out

    out["Arithmetic"] = sum(values) / n
    out["RMS"] = math.sqrt(sum(v * v for v in values) / n)

    all_positive = all(v > 0 for v in values)
    if all_positive:
        out["Geometric"] = math.exp(sum(math.log(v) for v in values) / n)
        denom = sum(1.0 / v for v in values)
        if denom != 0:
            out["Harmonic"] = n / denom
        if p <= 0:
            out["Power (Mp)"] = (sum(v ** p for v in values) / n) ** (1.0 / p) if p != 0 else out["Geometric"]
    elif p > 0:
        near_integer = abs(p - round(p)) < 1e-9
        if near_integer or all(v >= 0 for v in values):
            out["Power (Mp)"] = (sum(v ** p for v in values) / n) ** (1.0 / p)

    if p > 0 and "Power (Mp)" not in out:
        if all(v >= 0 for v in values):
            out["Power (Mp)"] = (sum(v ** p for v in values) / n) ** (1.0 / p)

    if all(v >= 0 for v in values) and sum(values) > 0:
        out["Contraharmonic"] = sum(v * v for v in values) / sum(values)

    if weights and len(weights) == n and sum(weights) != 0:
        out["Weighted"] = sum(v * w for v, w in zip(values, weights)) / sum(weights)

    sorted_vals = sorted(values)
    k = int(n * max(0.0, min(40.0, trim_pct)) / 100.0)
    if 2 * k < n:
        trimmed = sorted_vals[k : n - k]
        out["Trimmed"] = sum(trimmed) / len(trimmed)

    return out


def render_means_interactive():
    st.markdown("## Interactive playground")
    st.markdown(sanitize_html("<div class='muted'>Try your own values and compare mean choices.</div>"), unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        raw_values = st.text_area("Numbers (comma, space, or newline)", value="1, 2, 8", key="means_values")
    with c2:
        raw_weights = st.text_input("Weights (optional)", value="", key="means_weights")
    with c3:
        trim_pct = st.slider("Trim percent each tail", min_value=0, max_value=40, value=0, key="means_trim")

    p_val = st.slider("Power mean p", min_value=-2.0, max_value=4.0, value=1.0, step=0.1, key="means_p")
    selected = st.multiselect(
        "Show on chart",
        ["Arithmetic", "Geometric", "Harmonic", "RMS", "Contraharmonic", "Weighted", "Trimmed", "Power (Mp)"],
        default=["Arithmetic", "Geometric", "Harmonic", "RMS", "Power (Mp)"],
        key="means_show",
    )

    values = parse_numeric_list(raw_values)
    weights = parse_numeric_list(raw_weights) if raw_weights.strip() else []

    if not values:
        st.warning("Enter at least one valid numeric value.")
        return

    bundle = compute_means_bundle(values, weights, float(trim_pct), float(p_val))
    am = bundle.get("Arithmetic")

    rows: List[Dict[str, str]] = []
    for name, val in bundle.items():
        diff = ""
        if am is not None:
            diff = f"{(val - am):.6f}"
        rows.append({"Mean": name, "Value": f"{val:.6f}", "Difference from AM": diff})
    st.table(rows)

    chart_vals = {k: v for k, v in bundle.items() if k in selected}
    if chart_vals:
        st.bar_chart(chart_vals)
    st.caption("Notes: GM and HM and Mp with p <= 0 require all values > 0. Contraharmonic requires non-negative values with positive sum.")
