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
avg_ticket = st.sidebar.number_input("Average Ticket Size ($)", value=18.50)

# --- Data Generation & Chronological Fix ---
data = {
    "Day": ["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"],
    "Sales": [4500, 1950, 2400, 2800, 3200, 2100, 2400], # Adjusted for a realistic week
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

# --- Top Metrics Section ---
total_sales = df['Sales'].sum()
total_profit = df['Daily_Profit'].sum()
avg_labor_pct = (df['Labor_Cost'].sum() / total_sales) * 100
waste_total = df['Daily_Waste'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Weekly Sales", f"${total_sales:,.2f}")

with col2:
    profit_margin = (total_profit / total_sales) * 100
    st.metric("Total Net Profit", f"${total_profit:,.2f}", delta=f"{profit_margin:.1f}% Margin")

with col3:
    st.metric("Avg Labor %", f"{avg_labor_pct:.1f}%", delta=f"{avg_labor_pct - labor_target:.1f}%", delta_color="inverse")

with col4:
    st.metric("Weekly Waste", f"${waste_total:,.2f}")

# --- Visualizing the Narrative ---
st.divider()
st.subheader("Real-Time Sales, Labor, and Waste Trends")
# 3-line chart showing the relationship between revenue and costs
st.line_chart(df.set_index("Day")[["Sales", "Labor_Cost", "Daily_Waste"]])

# --- The "Regional Coach" Strategic Insights ---
st.subheader("💡 Strategic Insights")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**Labor Strategy**")
    if avg_labor_pct > labor_target:
        st.warning(f"Labor is {avg_labor_pct - labor_target:.1f}% over target. Monday and Tuesday show excessive hours relative to volume. Recommend 'staggered' starts.")
    else:
        st.success("Labor is optimized. You have successfully aligned your payroll with your traffic flow.")

with c2:
    st.markdown("**Profitability Analysis**")
    if profit_margin < 15:
        st.error(f"Profit Margin ({profit_margin:.1f}%) is below the 15% hospitality benchmark. Your 'Fixed Ops' and 'Food Cost' sliders are currently eating your take-home pay.")
    else:
        st.success(f"Strong healthy margins at {profit_margin:.1f}%. This allows for reinvestment or expansion.")

with c3:
    st.markdown("**Waste & Retention**")
    if waste_pct > 3:
        st.info(f"Waste is at {waste_pct}%. On your peak day (Saturday), you are losing ${df['Daily_Waste'].max():,.2f}. Tighten prep-sheets to recover this.")
    else:
        st.write("Waste is within acceptable limits. Maintain current inventory controls.")

# --- Footer ---
st.sidebar.divider()
st.sidebar.write("Developed by **Open View Consulting**")
st.sidebar.caption("Empowering Owners with Live Data")
