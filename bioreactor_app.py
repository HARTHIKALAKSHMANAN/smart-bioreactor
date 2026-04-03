import numpy as np
from scipy.integrate import odeint
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="AI Smart Bioreactor", layout="wide")
st.title("🧪 AI-Integrated Smart Bioreactor")
st.subheader("Waste-to-Biopolymer (PHA) Conversion System")
st.markdown("**Real-time Simulation & Optimization Dashboard**")

# Sidebar controls
st.sidebar.header("Process Controls")
temp = st.sidebar.slider("Temperature (°C)", 25, 45, 37, help="Optimal range: 30-40°C")
ph = st.sidebar.slider("pH Level", 5.0, 9.0, 7.0, help="Optimal range: 6.5-7.5")
feed_rate = st.sidebar.slider("Feed Rate (g/h)", 0.0, 10.0, 2.0, help="Waste input rate")

# Simple AI Suggestion Button
if st.sidebar.button("🤖 Get AI Optimal Suggestion"):
    st.sidebar.success("**AI Recommendation:** Set Temperature = 36°C, pH = 7.0, Feed Rate = 3.5 g/h for maximum PHA yield!")

# Bioreactor kinetic model
def bioreactor_model(y, t, T, pH, feed):
    X, S, P = y  # Biomass, Substrate, PHA
    # Temperature and pH effect on growth rate
    mu_max = 0.35 * np.exp(-((T - 36)**2) / 50) * (1 - abs(pH - 7.0) / 4)
    mu = mu_max * S / (S + 8) if S > 0 else 0
    Yxs = 0.48  # Biomass yield
    Ypx = 0.45  # PHA yield
    dXdt = mu * X
    dSdt = feed - (mu * X) / Yxs
    dPdt = Ypx * mu * X
    return [dXdt, dSdt, dPdt]

# Run simulation for 72 hours
t = np.linspace(0, 72, 500)
y0 = [0.2, 25.0, 0.0]  # Initial biomass, substrate, PHA
sol = odeint(bioreactor_model, y0, t, args=(temp, ph, feed_rate))

df = pd.DataFrame(sol, columns=['Biomass (g/L)', 'Substrate (g/L)', 'PHA (g/L)'])
df['Time (h)'] = t

# Main Dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Max PHA Produced", f"{df['PHA (g/L)'].max():.2f} g/L", "↑ Yield")
with col2:
    st.metric("Final Biomass", f"{df['Biomass (g/L)'].iloc[-1]:.2f} g/L")
with col3:
    st.metric("Waste Consumed", f"{25 - df['Substrate (g/L)'].iloc[-1]:.1f} g/L")

# Graphs
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['PHA (g/L)'], name='PHA (Biopolymer)', line=dict(color='#00ff88', width=3)))
fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['Biomass (g/L)'], name='Biomass', line=dict(color='#4488ff')))
fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['Substrate (g/L)'], name='Remaining Waste', line=dict(color='#ff4444')))

fig.update_layout(
    title="Biopolymer Production Over Time",
    xaxis_title="Time (hours)",
    yaxis_title="Concentration (g/L)",
    height=500,
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

st.success(f"✅ Simulation Complete! Predicted PHA Yield after 72 hours: **{df['PHA (g/L)'].max():.2f} g/L**")
st.info("💡 Move the sliders in the sidebar to see real-time changes. This simulates the AI-adaptive bioreactor behavior.")

st.caption("AI-Integrated Smart Bioreactor Dashboard | For academic project use")
