import streamlit as st
import pandas as pd

# --- Page Config & Styling ---
st.set_page_config(page_title="Open View | Regional Strategy Demo", layout="wide")

# Custom CSS for a professional "Leadership" look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Open View: Strategic Operations Dashboard")
st.markdown("### *Bridging the gap between the P&L and the Daily Shift*")

# --- Sidebar: The Consulting "Levers" ---
st.sidebar.header("Operational Levers")
st.sidebar.info("Adjust these to see how operational coaching impacts the bottom line.")

# Client-facing inputs
labor_target = st.sidebar.slider("Target Labor %", 15, 35, 22)
food_cost_target = st.sidebar.slider("Target Food Cost %", 20, 40, 28)
waste_pct = st.sidebar.slider("Daily Waste/Loss %", 0.0, 10.0, 2.5)
avg_ticket = st.sidebar.number_input("Average Ticket Size ($)", value=18.50)

# --- Data Generation & Chronological Fix ---
data = {
    "Day": ["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"],
    "Sales": [4500, 1950, 5200, 3800, 2800, 2100, 2400],
    "Labor_Hours": [85, 42, 95, 75, 55, 45, 50]
}
df = pd.DataFrame(data)

# THE SORTING FIX: Tells Python the days have a specific order
days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)
df = df.sort_values('Day')

# Calculations based on your levers
df['Labor_Cost'] = df['Labor_Hours'] * 16 # Baseline $16/hr
df['Labor_Pct'] = (df['Labor_Cost'] / df['Sales']) * 100

# --- Top Level Metrics ---
total_sales = df['Sales'].sum()
avg_labor = df['Labor_Pct'].mean()
waste_total = total_sales * (waste_pct / 100)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Weekly Sales", f"${total_sales:,.2f}")
    
with col2:
    # Shows the gap between reality and the "Regional Manager" target
    delta_val = f"{avg_labor - labor_target:.1f}%"
    st.metric("Avg Labor %", f"{avg_labor:.1f}%", delta=delta_val, delta_color="inverse")

with col3:
    # Shows the literal cost of waste
    st.metric("Weekly Waste Cost", f"${waste_total:,.2f}", delta="Action Needed" if waste_total > 500 else None)

# --- Visualizing the Narrative ---
st.divider()
st.subheader("Real-Time Sales vs. Labor Performance")
# Line chart using the sorted data
st.line_chart(df.set_index("Day")[["Sales", "Labor_Cost"]])

# --- The "Regional Coach" Insight Section ---
st.subheader("💡 Strategic Insights")
col_a, col_b = st.columns(2)

with col_a:
    if avg_labor > labor_target:
        st.warning(f"**Labor Alert:** You are running {avg_labor - labor_target:.1f}% over your goal. Based on the chart, Mon-Wed are 'heavy' relative to sales. Consider a 'Staggered Clock-in' for those days or cutting hours.")
    else:
        st.success("**Labor Optimized:** Your scheduling is tight. Focus can shift to growth.")

with col_b:
    if waste_total > 400:
        st.error(f"**Profit Leak:** Your waste is costing you ${waste_total:,.0f}/week. That is equivalent to losing {total_sales/avg_ticket * (waste_pct/100):.0f} customers per week.")
    else:
        st.info("**Waste Control:** Loss is within acceptable limits.")

# --- Footer Call to Action ---
st.sidebar.divider()
st.sidebar.write("Developed by **Open View Consulting**")
st.sidebar.caption("Empowering Owners with Live Data")
