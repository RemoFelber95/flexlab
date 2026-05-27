import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def figure_with_forecast(ubound, lbound, title, xtitle, ytitle, label,colorplot):
    now_idx = 12  # "now" at 12:00
    time_index = pd.date_range("2026-01-01", periods=24, freq="H")
    # Calculate uncertainty with power of 0.5 for future values
    measerument = np.random.uniform(lbound, ubound, 24)
    uncertainty_upper = np.zeros(24)
    uncertainty_lower = np.zeros(24)
    for i in range(24):
        if i < now_idx:
            uncertainty = 0
        else:
            uncertainty = 0.05*max(measerument) * (i - now_idx)  ** 0.5
        uncertainty_upper[i] = measerument[i] +  uncertainty
        uncertainty_lower[i] = measerument[i] -  uncertainty
    
    
    
    # Combined plot with measured values and uncertainty band

    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_index[:now_idx+1], y=measerument[:now_idx+1], name=label, mode="lines", line=dict(color=colorplot)))
    fig.add_trace(go.Scatter(x=time_index[now_idx:], y=uncertainty_upper[now_idx:], name="", fill=None, mode="lines", line=dict(color=colorplot)))
    fig.add_trace(go.Scatter(x=time_index[now_idx:], y=uncertainty_lower[now_idx:], fill="tonexty", mode="lines", line=dict(color=colorplot), name="Unsicherheitsband"))
    fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title=ytitle)

    return fig
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="FlexLab",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("⚡ FlexLab")
st.sidebar.markdown("Physical Twin Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Energy Markets",
        
        "Demand",
        "Storage",
        "Flexibility",
        "Schedule",
        "Economics",
        "Weather Data"
    ]
)

# ---------------------------------------------------
# DUMMY DATA
# ---------------------------------------------------

time_index = pd.date_range("2026-01-01", periods=24, freq="H")

DayAhead = np.random.uniform(80, 220, 24)
AncServicesPower = np.random.uniform(20, 60, 24)
AncServicesEnergy = np.random.uniform(15, 50, 24)
DemandHeat = np.random.uniform(20, 80, 24)
DemandCooling = np.random.uniform(0, 30, 24)
DemandEl = np.random.uniform(15, 60, 24)
StorageBattery = np.random.uniform(30, 90, 24)
StorageTES = np.random.uniform(40, 95, 24)
StorageBuilding = np.random.uniform(20, 75, 24)
ScheduleRef = np.random.uniform(50, 150, 24)
ScheduleOpt = ScheduleRef * np.random.uniform(0.75, 0.95, 24)

df = pd.DataFrame({
    "DayAhead": DayAhead,
    "AncServicesPower": AncServicesPower,
    "AncServicesEnergy": AncServicesEnergy,
    "DemandHeat": DemandHeat,
    "DemandCooling": DemandCooling,
    "DemandEl": DemandEl,
    "StorageBattery": StorageBattery,
    "StorageTES": StorageTES,
    "StorageBuilding": StorageBuilding,
    "ScheduleRef": ScheduleRef,
    "ScheduleOpt": ScheduleOpt
}, index=time_index)

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

# ---------------------------------------------------
# ENERGY MARKETS
# ---------------------------------------------------
if page == "Energy Markets":

    st.title("📈 Energy Markets")

    st.subheader("Day-Ahead Prices")
    st.line_chart(df["DayAhead"])

    st.subheader("Ancillary Services Prices")
    st.line_chart(df[["AncServicesPower", "AncServicesEnergy"]])
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current Price", "145 CHF/MWh")

    with col2:
        st.metric("Max Price Today", "220 CHF/MWh")

    st.subheader("PV Production")
    fig = figure_with_forecast(ubound=50, lbound=0, title="PV Production", xtitle="Time", ytitle="Price (CHF/MWh)",label="PV Production", colorplot="orange")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Market Signals")
    st.info("High prices between 17:00 - 21:00")
    st.info("Low prices between 00:00 - 06:00")
# ---------------------------------------------------
# DEMAND
# ---------------------------------------------------

elif page == "Demand":

    st.title("🏠 Demand")

    st.subheader("Electric Demand")
    fig = figure_with_forecast(ubound=80, lbound=0, title="Electric Demand", xtitle="Time", ytitle="kW",label="Electric Demand", colorplot="yellow")
    st.plotly_chart(fig, use_container_width=True)

    

    st.subheader("Heat Demand")
    fig = figure_with_forecast(ubound=80, lbound=0, title="Heat Demand", xtitle="Time", ytitle="kW",label="Heat Demand", colorplot="red")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cooling Demand")
    fig = figure_with_forecast(ubound=30, lbound=0, title="Cooling Demand", xtitle="Time", ytitle="kW",label="Cooling Demand", colorplot="blue")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# FLEXIBILITY
# ---------------------------------------------------
elif page == "Flexibility":

    st.title("🔋 Flexibility")

    st.subheader("Flexible Power")
    fig = figure_with_forecast(ubound=80, lbound=0, title="Flexible Power", xtitle="Time", ytitle="kW",label="Flexible Power", colorplot="green")
    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("Flexible Energy")
    fig = figure_with_forecast(ubound=80, lbound=0, title="Flexible Energy", xtitle="Time", ytitle="kWh",label="Flexible Energy", colorplot="blue")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Storage":
    st.title("🔋 Storage")

    st.subheader("Battery Storage")
    fig = figure_with_forecast(ubound=1, lbound=0, title="Battery Storage", xtitle="Time", ytitle="SOC",label="Battery Storage", colorplot="green")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Thermal Storage")
    fig = figure_with_forecast(ubound=1, lbound=0, title="Thermal Storage", xtitle="Time", ytitle="SOC",label="Thermal Storage", colorplot="red")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Building Inertia")
    fig = figure_with_forecast(ubound=1, lbound=0, title="Building Inertia", xtitle="Time", ytitle="SOC",label="Building Inertia", colorplot="blue")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# SCHEDULE
# ---------------------------------------------------

elif page == "Schedule":

    st.title("📅 Schedule")

    st.subheader("Schedule Comparison")
    
    now_idx = 12
    time_index_sched = pd.date_range("2026-01-01", periods=24, freq="H")
    ref_schedule = np.random.uniform(50, 150, 24)
    opt_schedule = ref_schedule * np.random.uniform(0.5, 1.5, 24)
    
    uncertainty_upper_ref = np.zeros(24)
    uncertainty_lower_ref = np.zeros(24)
    uncertainty_upper_opt = np.zeros(24)
    uncertainty_lower_opt = np.zeros(24)
    
    for i in range(24):
        if i < now_idx:
            uncertainty = 0
        else:
            uncertainty_ref = 0.05 * max(ref_schedule) * (i - now_idx) ** 0.5
            uncertainty_opt = 0.05 * max(opt_schedule) * (i - now_idx) ** 0.5
        uncertainty_upper_ref[i] = ref_schedule[i] + uncertainty_ref if i >= now_idx else ref_schedule[i]
        uncertainty_lower_ref[i] = ref_schedule[i] - uncertainty_ref if i >= now_idx else ref_schedule[i]
        uncertainty_upper_opt[i] = opt_schedule[i] + uncertainty_opt if i >= now_idx else opt_schedule[i]
        uncertainty_lower_opt[i] = opt_schedule[i] - uncertainty_opt if i >= now_idx else opt_schedule[i]
    
    fig_combined = go.Figure()
    fig_combined.add_trace(go.Scatter(x=time_index_sched[:now_idx+1], y=ref_schedule[:now_idx+1], name="Reference Schedule", mode="lines", line=dict(color="gray")))
    fig_combined.add_trace(go.Scatter(x=time_index_sched[now_idx:], y=uncertainty_upper_ref[now_idx:], name="", fill=None, mode="lines", line=dict(color="gray")))
    fig_combined.add_trace(go.Scatter(x=time_index_sched[now_idx:], y=uncertainty_lower_ref[now_idx:], fill="tonexty", mode="lines", line=dict(color="gray"), name="Reference Uncertainty"))
    
    fig_combined.add_trace(go.Scatter(x=time_index, y=opt_schedule, name="Optimized Schedule", mode="lines", line=dict(color="green")))

    
    fig_combined.update_layout(title="Schedule Comparison", xaxis_title="Time", yaxis_title="Power (kW)")
    st.plotly_chart(fig_combined, use_container_width=True)

# ---------------------------------------------------
# ECONOMICS
# ---------------------------------------------------
elif page == "Economics":

    st.title("💰 Economics")

    st.subheader("Economics Analysis")
    
    reference_cost = np.random.uniform(50, 150, 24)
    income_anc_services = np.random.uniform(10, 40, 24)
    optimized_cost = reference_cost * 0.9 - income_anc_services
    
    fig_econ = go.Figure()
    
    # Electricity Cost (negative, red)
    fig_econ.add_trace(go.Bar(x=time_index, y=-reference_cost, name="Electricity Cost", marker=dict(color="red")))
    
    # Income Ancillary Services (positive, green)
    fig_econ.add_trace(go.Bar(x=time_index, y=income_anc_services, name="Income Ancillary Services", marker=dict(color="green")))
    
    # Optimized Cost (line)
    fig_econ.add_trace(go.Scatter(x=time_index, y=optimized_cost, name="Optimized Cost", mode="lines", line=dict(color="blue", width=2)))
    fig_econ.add_trace(go.Scatter(x=time_index, y=reference_cost, name="Reference Cost", mode="lines", line=dict(color="orange", width=2)))
    fig_econ.update_layout(title="Economics Analysis", xaxis_title="Time", yaxis_title="Cost/Income (CHF)", barmode="relative")
    st.plotly_chart(fig_econ, use_container_width=True)

elif page == "Weather Data":

    st.title("🌤️ Weather Data")
    
    st.subheader("Weather Forecast Analysis")
    
    # Generate weather data
    temperature = np.random.uniform(10, 30, 24)
    sunshine_duration = np.random.uniform(0, 12, 24)
    
    # Temperature plot
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=time_index, y=temperature, name="Temperature", mode="lines+markers", line=dict(color="orange", width=2)))
    fig_temp.update_layout(title="Temperature Forecast", xaxis_title="Time", yaxis_title="Temperature (°C)")
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Sunshine duration plot
    fig_sunshine = go.Figure()
    fig_sunshine.add_trace(go.Bar(x=time_index, y=sunshine_duration, name="Sunshine Duration", marker=dict(color="gold")))
    fig_sunshine.update_layout(title="Sunshine Duration Forecast", xaxis_title="Time", yaxis_title="Duration (hours)")
    st.plotly_chart(fig_sunshine, use_container_width=True)
