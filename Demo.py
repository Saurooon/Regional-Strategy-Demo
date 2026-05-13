import streamlit as st
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Open View | Regional Strategy Demo", layout="wide")

st.title("Open View: Strategic Dashboard")
st.markdown("### *Turning the 'Autopsy' (P&L) into a Live Roadmap*")

# --- Sidebar: The "Levers" ---
# This demonstrates to the client how YOU help them control their numbers.
st.sidebar.header("Operational Levers")
st.sidebar.info("Adjust these to see how operational changes impact your bottom line.")
waste_pct = st.sidebar.slider("Daily Waste/Loss %", 0.0, 10.0, 2.5)

labor_target = st.sidebar.slider("Target Labor %", 15, 35, 22)
food_cost_target = st.sidebar.slider("Target Food Cost %", 20, 40, 28)
avg_ticket = st.sidebar.number_input("Average Ticket Size ($)", value=18.50)

# --- Simulated Data Generation ---
data = {
    "Day": ["Fri", "Mon", "Sat", "Sun", "Thu", "Tue", "Wed"], # Out of order data
    "Sales": [4500, 1950, 5200, 3800, 2800, 2100, 2400],
    "Labor_Hours": [85, 42, 95, 75, 55, 45, 50]
}
df = pd.DataFrame(data)

# --- THE FIX STARTS HERE ---
days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)
df = df.sort_values('Day')
# --- THE FIX ENDS HERE ---

# Now calculate the costs AFTER sorting
df['Labor_Cost'] = df['Labor_Hours'] * 16 
df['Labor_Pct'] = (df['Labor_Cost'] / df['Sales']) * 100

# --- Key Metrics (The "Gauges") ---
total_sales = df['Sales'].sum()
avg_labor = df['Labor_Pct'].mean()
# Calculate the literal dollar amount being 'thrown away'
waste_total = total_sales * (waste_pct / 100)

with col3:
    st.metric("Weekly Waste Cost", f"${waste_total:,.2f}", delta="- Action Needed" if waste_total > 500 else None)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Weekly Sales", f"${total_sales:,.2f}")
    
with col2:
    # Color-coded logic to show "Regional Manager" oversight
    delta = f"{avg_labor - labor_target:.1f}%"
    color = "inverse" if avg_labor > labor_target else "normal"
    st.metric("Avg Labor %", f"{avg_labor:.1f}%", delta=delta, delta_color=color)

with col3:
    projected_profit = total_sales * (1 - (labor_target/100 + food_cost_target/100 + 0.20)) # 20% fixed ops
    st.metric("Projected Weekly Profit", f"${projected_profit:,.2f}")

# --- Visualizing the Narrative ---
st.divider()
st.subheader("Real-Time Sales vs. Labor Performance")
st.line_chart(df.set_index("Day")[["Sales", "Labor_Cost"]])

# --- The "Regional Coach" Insight ---
st.subheader("Strategic Insights")
if avg_labor > labor_target:
    st.warning(f"**Action Required:** Labor is currently {avg_labor - labor_target:.1f}% over target. Suggest cutting 'on-call' shifts for Tuesday/Wednesday based on sales trends.")
else:
    st.success("**Performance:** Labor is optimized. Focus on upselling to increase Average Ticket beyond $18.50.")

# --- Footer ---
st.sidebar.divider()
st.sidebar.write("Developed by **Open View Consulting**")
