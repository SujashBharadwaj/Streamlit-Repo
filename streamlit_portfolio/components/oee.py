import random
import streamlit as st
from typing import Dict


def compute_oee(planned_time_sec: int, downtime_sec: int, total_count: int, good_count: int, ideal_cycle_time_sec: int) -> Dict[str, float]:
    run_time = planned_time_sec - downtime_sec
    if planned_time_sec <= 0 or run_time <= 0 or total_count <= 0 or good_count < 0:
        return {"availability": 0.0, "performance": 0.0, "quality": 0.0, "oee": 0.0}

    availability = run_time / planned_time_sec
    performance = (total_count * ideal_cycle_time_sec) / run_time
    quality = good_count / total_count

    availability = max(0.0, min(1.0, availability))
    performance = max(0.0, min(1.0, performance))
    quality = max(0.0, min(1.0, quality))

    oee = availability * performance * quality
    return {"availability": availability, "performance": performance, "quality": quality, "oee": oee}


def render_oee_interactive():
    st.markdown("## Interactive OEE calculation (click to run)")
    st.markdown(
        "<div class='muted'>This demo generates a realistic shift scenario, calculates OEE, and tells you what to fix first based on the biggest loss.</div>",
        unsafe_allow_html=True,
    )

    cA, cB = st.columns([1, 1])
    with cA:
        seed = st.number_input("Optional seed (repeat the same example)", min_value=0, max_value=999999, value=0, step=1)
    with cB:
        st.markdown("<div class='tiny'>Tip: set seed to 0 for fresh random outputs.</div>", unsafe_allow_html=True)

    run = st.button("Run randomized example", key="run_oee_demo")

    with st.expander("Show Python code"):
        st.code(
            """def compute_oee(planned_time_sec, downtime_sec, total_count, good_count, ideal_cycle_time_sec):
    run_time = planned_time_sec - downtime_sec
    availability = run_time / planned_time_sec
    performance  = (total_count * ideal_cycle_time_sec) / run_time
    quality      = good_count / total_count
    oee = availability * performance * quality
    return availability, performance, quality, oee
""",
            language="python",
        )

    if not run:
        st.markdown("<div class='oee-box tiny'>Click the button to generate inputs and see the output metrics + takeaway.</div>", unsafe_allow_html=True)
        return

    if seed != 0:
        random.seed(int(seed))

    planned_time_min = random.choice([420, 450, 480])
    downtime_min = random.randint(15, 90)
    total_count = random.randint(700, 1600)
    scrap = random.randint(0, max(1, int(0.12 * total_count)))
    good_count = max(0, total_count - scrap)
    ideal_cycle_time_sec = random.choice([18, 20, 22, 24, 26])

    planned_time_sec = planned_time_min * 60
    downtime_sec = downtime_min * 60

    out = compute_oee(
        planned_time_sec=planned_time_sec,
        downtime_sec=downtime_sec,
        total_count=total_count,
        good_count=good_count,
        ideal_cycle_time_sec=ideal_cycle_time_sec,
    )

    st.markdown("### Inputs")
    st.write({
        "planned_time_min": planned_time_min,
        "downtime_min": downtime_min,
        "total_count": total_count,
        "good_count": good_count,
        "ideal_cycle_time_sec": ideal_cycle_time_sec,
    })

    st.markdown("### Outputs")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Availability", f"{out['availability']*100:.1f}%")
    c2.metric("Performance", f"{out['performance']*100:.1f}%")
    c3.metric("Quality", f"{out['quality']*100:.1f}%")
    c4.metric("OEE", f"{out['oee']*100:.1f}%")

    losses = {
        "Availability (downtime, setups, breakdowns)": 1 - out["availability"],
        "Performance (micro-stops, slow cycles, minor jams)": 1 - out["performance"],
        "Quality (scrap, rework, startup rejects)": 1 - out["quality"],
    }
    worst = max(losses, key=losses.get)
    worst_loss = losses[worst]

    st.markdown("### Key takeaway")
    if worst_loss < 0.04:
        st.success("This run is fairly balanced. Biggest gains come from tightening measurement, standard work, and small continuous improvements.")
    else:
        if "Availability" in worst:
            st.info("Availability is the main limiter. Reduce unplanned stops, improve changeovers, and shorten maintenance response time.")
        elif "Performance" in worst:
            st.info("Performance is the main limiter. Hunt micro-stops and speed losses: feeding issues, small jams, slow cycles, and drift from the ideal.")
        else:
            st.info("Quality is the main limiter. Focus on defect root causes, startup stability, process parameters, and catching issues earlier in the line.")

    st.markdown(
        f"<div class='tiny'>Biggest loss in this run: <b>{worst}</b> (approx. {(worst_loss*100):.1f}% loss)</div>",
        unsafe_allow_html=True,
    )
