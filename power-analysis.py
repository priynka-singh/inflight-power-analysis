import streamlit as st
from statsmodels.stats.power import tt_solve_power
from math import ceil

st.title("📈 Inflight Power Analysis")

st.markdown("Estimate how many more weeks of data you need to achieve statistical significance based on current test performance.")

# Input fields
mean = st.number_input("🔹 Mean Sales Lift ($)", value=14396.13)
std_dev = st.number_input("🔹 Standard Deviation ($)", value=27896.51)
current_weeks = st.number_input("🔹 Weeks of Data Collected", value=8, step=1)

effect_size = mean / std_dev if std_dev else 0

st.markdown(f"📏 **Effect Size**: {effect_size:.3f}" if std_dev else "⚠️ Please enter a valid standard deviation.")

def required_weeks(alpha):
    if effect_size == 0:
        return None
    return ceil(tt_solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=0.8,
        alternative='two-sided'
    ))

# Confidence levels to evaluate
ci_levels = [
    (0.2, "80%"),
    (0.15, "85%"),
    (0.1, "90%")
]

st.subheader("🧪 Results")

for alpha, label in ci_levels:
    req_weeks = required_weeks(alpha)
    if req_weeks is None:
        st.warning(f"{label} CI: Cannot compute due to invalid inputs.")
        continue

    if current_weeks < req_weeks:
        st.info(f"{label} CI → 🕒 {req_weeks - current_weeks} more week(s) needed (total required: {req_weeks})")
    else:
        st.success(f"{label} CI → ✅ Statistical significance reached with {current_weeks} weeks (needed: {req_weeks})")

