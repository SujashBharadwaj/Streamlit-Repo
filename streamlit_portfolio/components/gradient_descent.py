import streamlit as st
from typing import Dict, List
from utils.helpers import sanitize_html


def render_gradient_descent_interactive():
    st.markdown("## Interactive playground (1-D, cubic only)")
    st.markdown(sanitize_html("<div class='muted'>Define f(x) = a3x^3 + a2x^2 + a1x + a0 and simulate gradient descent.</div>"), unsafe_allow_html=True)

    a_cols = st.columns(4)
    a3 = a_cols[0].number_input("a3", value=0.0, step=0.1, key="gd_a3")
    a2 = a_cols[1].number_input("a2", value=1.0, step=0.1, key="gd_a2")
    a1 = a_cols[2].number_input("a1", value=0.0, step=0.1, key="gd_a1")
    a0 = a_cols[3].number_input("a0", value=0.0, step=0.1, key="gd_a0")

    c1, c2, c3, c4 = st.columns(4)
    x0 = c1.number_input("Initial x0", value=2.0, step=0.1, key="gd_x0")
    alpha = c2.number_input("Learning rate alpha", value=0.2, step=0.01, min_value=0.0001, key="gd_alpha")
    max_steps = c3.number_input("Max steps", min_value=1, max_value=200, value=20, step=1, key="gd_steps")
    round_steps = c4.checkbox("Round each step to 2 decimals", value=True, key="gd_round")

    tol = st.number_input("Stop when |f'(x)| < tol", min_value=0.0001, max_value=1.0, value=0.01, step=0.001, key="gd_tol")

    def f(x: float) -> float:
        return a3 * x * x * x + a2 * x * x + a1 * x + a0

    def df(x: float) -> float:
        return 3 * a3 * x * x + 2 * a2 * x + a1

    x = float(x0)
    rows: List[Dict] = []
    diverged = False
    for step in range(int(max_steps) + 1):
        fx = f(x)
        dfx = df(x)
        rows.append({"Step": step, "x": round(x, 6), "f(x)": round(fx, 6), "f'(x)": round(dfx, 6)})
        if abs(dfx) < float(tol):
            break
        x = x - float(alpha) * dfx
        if round_steps:
            x = round(x, 2)
        if abs(x) > 1e9:
            diverged = True
            break

    st.dataframe(rows, use_container_width=True)
    st.line_chart({"f(x)": [r["f(x)"] for r in rows], "f'(x)": [r["f'(x)"] for r in rows]})
    if diverged:
        st.warning("The run diverged. Try a smaller learning rate.")
