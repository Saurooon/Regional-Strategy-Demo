import streamlit as st
import pandas as pd

# --- Page Config & Styling ---
st.set_page_config(page_title="Open View | Regional Strategy Demo", layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Open View: Strategic Operations Dashboard")
st.markdown("### *Bridging the gap between the P&L and the Daily Shift*")

# --- Sidebar: The Consulting "Levers" ---
st.sidebar.header("Operational Levers")
labor_target = st.sidebar.slider("Target Labor %", 15, 35, 22)
food_cost_target = st.sidebar.slider("Target Food Cost %", 20, 40, 28)
waste_pct = st.sidebar.slider("Daily Waste/Loss %", 0.0, 10.0, 2.5)
fixed_costs_pct = st.sidebar.slider("Fixed Ops % (Rent/Utilities)", 10, 30, 20)

# --- Data Generation & Chronological Fix ---
data = {
    "Day": ["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"],
    "Sales": [4500, 1950, 5200, 3800, 2800, 2100, 2400],
    "Labor_Hours": [85, 42, 95, 75, 55, 45, 50]
}
df = pd.DataFrame(data)
days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)
df = df.sort_values('Day')

# Calculations
df['Labor_Cost'] = df['Labor_Hours'] * 16 
df['Daily_Waste'] = df['Sales'] * (waste_pct / 100)
df['Daily_Food_Cost'] = df['Sales'] * (food_cost_target / 100)
df['Daily_Fixed'] = df['Sales'] * (fixed_costs_pct / 100)
df['Daily_Profit'] = df['Sales'] - (df['Labor_Cost'] + df['Daily_Waste'] + df['Daily_Food_Cost'] + df['Daily_Fixed'])

# --- Metrics Section ---
total_sales = df['Sales'].sum()
total_profit = df['Daily_Profit'].sum()
avg_labor = (df['Labor_Cost'].sum() / total_sales) * 100
waste_total = df['Daily_Waste'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Weekly Sales", f"${total_sales:,.2f}")

with col2:
    # THE NEW TOTAL PROFIT METRIC
    st.metric("Total Net Profit", f"${total_profit:,.2f}", delta="Check Margins" if total_profit < (total_sales * 0.1) else "Healthy")

with col3:
    st.metric("Avg Labor %", f"{avg_labor:.1f}%", delta=f"{avg_labor - labor_target:.1f}%", delta_color="inverse")

with col4:
    st.metric("Weekly Waste", f"${waste_total:,.2f}")

# --- Visualizing the Narrative ---
st.divider()
st.subheader("Real-Time Sales, Labor, and Waste Trends")
# Added Daily_Waste to the line chart
st.line_chart(df.set_index("Day")[["Sales", "Labor_Cost", "Daily_Waste"]])

# --- The "Regional Coach" Insight Section ---
st.subheader("💡 Strategic Insights")
c1, c2 = st.columns(2)
with c1:
    if total_profit < (total_sales * 0.15):
        st.warning(f"**Margin Warning:** Your net profit is currently { (total_profit/total_sales)*100 :.1f}%. A healthy target is 15-20%. Check your Waste and Food Cost sliders.")
    else:
        st.success("**Strong Performance:** Your systems are generating healthy cashflow.")
with c2:
    st.info(f"**Visual Proof:** Notice how the 'Daily Waste' line stays flat or climbs. Even at {waste_pct}%, you are losing ${df['Daily_Waste'].max():,.2f} on your busiest day (Saturday).")

st.sidebar.divider()
st.sidebar.write("Developed by **Open View Consulting**")
