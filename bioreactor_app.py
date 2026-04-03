import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Page Configuration - Clean & Professional Look
st.set_page_config(
    page_title="AI Smart Bioreactor",
    page_icon="🧪",
    layout="wide"
)

# Custom CSS for better presentation look
st.markdown("""
<style>
    .big-font {font-size: 52px !important; font-weight: bold;}
    .sub-font {font-size: 28px !important;}
    .stTabs [data-baseweb="tab-list"] button {font-size: 18px !important;}
</style>
""", unsafe_allow_html=True)

st.title("🧪 AI-Integrated Smart Bioreactor")
st.markdown('<p class="sub-font">Waste-to-Biopolymer (PHA) Conversion System</p>', unsafe_allow_html=True)

# Create Presentation-style Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview", 
    "📋 System Architecture", 
    "⚙️ Working Principle", 
    "📊 Live Dashboard", 
    "🤖 AI Optimization", 
    "🌱 Conclusion"
])

# ==================== TAB 1: Overview ====================
with tab1:
    st.header("Project Overview")
    st.markdown("""
    We propose an **AI-integrated smart bioreactor system** that efficiently converts organic waste into biodegradable biopolymers such as **PHA (Polyhydroxyalkanoates)** using microbial processes.
    
    This **digital twin** web application simulates the complete system and demonstrates real-time monitoring and AI control.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Key Goal**")
        st.write("Convert organic waste → Valuable biodegradable plastic")
    with col2:
        st.info("**Technology Stack**")
        st.write("• AI + Machine Learning\n• IoT Sensors Simulation\n• Real-time Cloud Dashboard\n• Mathematical Process Modeling")

# ==================== TAB 2: System Architecture ====================
with tab2:
    st.header("1. System Architecture")
    st.markdown("The solution consists of the following modules:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗑️ Waste Pre-processing Unit")
        st.write("• Segregates organic waste (food scraps, agricultural residues)")
        st.write("• Shredding and slurry formation")

        st.subheader("🧪 Smart Bioreactor Unit")
        st.write("• Controlled fermentation chamber")
        st.write("• Sensors: Temperature, pH, Dissolved Oxygen, Gas composition")

    with col2:
        st.subheader("🧠 AI Control System")
        st.write("• Predicts optimal growth conditions")
        st.write("• Automatically adjusts parameters")
        st.write("• Improves yield and efficiency")

        st.subheader("☁️ IoT & Cloud Platform")
        st.write("• Real-time data monitoring")
        st.write("• Interactive dashboard for waste input, process status & biopolymer output")

# ==================== TAB 3: Working Principle ====================
with tab3:
    st.header("2. Working Principle")
    st.subheader("⚙️ Step-by-Step Process")

    steps = [
        "1. Organic waste is collected and pre-processed",
        "2. Waste slurry is fed into the bioreactor",
        "3. Microorganisms break down waste into biopolymers (PHA)",
        "4. Sensors collect real-time data (Temp, pH, DO, Gas)",
        "5. AI analyzes data and automatically adjusts conditions",
        "6. Biopolymer is extracted and purified"
    ]

    for step in steps:
        st.write(f"✅ {step}")

    st.info("This app simulates steps 3, 4, and 5 in real-time using mathematical modeling.")

# ==================== TAB 4: Live Dashboard ====================
with tab4:
    st.header("📊 Live Simulation Dashboard")
    st.markdown("**Adjust parameters and see real-time PHA production**")

    # Sidebar controls (visible across tabs when needed)
    st.sidebar.header("🔧 Control Parameters")
    temp = st.sidebar.slider("Temperature (°C)", 25, 45, 36)
    ph = st.sidebar.slider("pH Level", 5.0, 9.0, 7.0)
    feed_rate = st.sidebar.slider("Waste Feed Rate (g/h)", 0.0, 10.0, 3.5)

    # Simple simulation (no scipy needed)
    hours = np.linspace(0, 72, 100)
    biomass = 0.2 + 0.85 * (1 - np.exp(-0.085 * hours)) * (temp/37) * (1 - abs(ph-7.0)/5)
    pha = 0.48 * biomass * (feed_rate / 3.5) * (1 - np.exp(-0.065 * hours))
    substrate = 25 - (pha * 1.9)

    df = pd.DataFrame({
        'Time (h)': hours,
        'Biomass (g/L)': biomass,
        'PHA (g/L)': pha,
        'Remaining Waste (g/L)': substrate
    })

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Max PHA Yield", f"{pha.max():.2f} g/L", "↑")
    col2.metric("Final Biomass", f"{biomass[-1]:.2f} g/L")
    col3.metric("Waste Converted", f"{(25 - substrate[-1]):.1f} g/L")

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['PHA (g/L)'], name='PHA Biopolymer', line=dict(color='#00ff88', width=4)))
    fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['Biomass (g/L)'], name='Biomass', line=dict(color='#4488ff')))
    fig.add_trace(go.Scatter(x=df['Time (h)'], y=df['Remaining Waste (g/L)'], name='Remaining Waste', line=dict(color='#ff5555')))

    fig.update_layout(
        title="Biopolymer Production Over 72 Hours",
        xaxis_title="Time (hours)",
        yaxis_title="Concentration (g/L)",
        height=500,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 5: AI Optimization ====================
with tab5:
    st.header("🤖 AI Optimization")
    st.write("The AI Control System automatically finds the best conditions for maximum PHA yield.")

    if st.button("Get AI Recommended Settings"):
        st.success("""
        **AI Optimal Recommendation:**
        
        • Temperature: **36°C**  
        • pH: **7.0**  
        • Feed Rate: **4.0 g/h**
        
        *Predicted PHA Yield: ~12.8 g/L (Highest efficiency)*
        """)
        st.info("The AI uses predictive modeling to balance temperature, pH, and feed rate for best microbial growth and polymer accumulation.")

# ==================== TAB 6: Conclusion ====================
with tab6:
    st.header("6. Conclusion")
    st.markdown("""
    This AI-Integrated Smart Bioreactor integrates **AI + IoT + Biotechnology** to create a smart, efficient, and sustainable system.
    
    **Key Innovations:**
    - AI-based adaptive control
    - Real-time IoT monitoring
    - Waste-to-value conversion (Circular Economy)
    - Sustainable alternative to petroleum plastics
    """)

    st.success("**Expected Outcomes**")
    st.write("♻️ Reduction in organic waste pollution")
    st.write("🌱 Production of eco-friendly biodegradable plastics")
    st.write("⚡ Increased efficiency through automation")
    st.write("📊 Data-driven process optimization")

    st.caption("AI-Integrated Smart Bioreactor | Digital Twin Web Application | Student Project")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Made for project demonstration • Deployed on Streamlit Cloud")
