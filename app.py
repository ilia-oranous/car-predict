import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="SuperCar Price AI",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    /* === Hide default Streamlit elements === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* === Space background === */
    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0, 150, 255, 0.15), transparent),
            radial-gradient(ellipse 80% 50% at 50% 120%, rgba(120, 40, 255, 0.15), transparent),
            linear-gradient(180deg, #050d1a 0%, #0a1929 50%, #000814 100%);
        background-attachment: fixed;
        color: #e0f7ff;
    }

    /* === Animated glowing particles === */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            radial-gradient(2px 2px at 20% 30%, rgba(0, 200, 255, 0.4), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(120, 80, 255, 0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(0, 220, 255, 0.5), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(0, 180, 255, 0.4), transparent),
            radial-gradient(2px 2px at 90% 80%, rgba(150, 100, 255, 0.3), transparent);
        background-size: 200% 200%;
        animation: twinkle 8s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.5; transform: translateY(0); }
        50% { opacity: 1; transform: translateY(-10px); }
    }

    /* === Hero title with animated gradient === */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2fff, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 3s linear infinite;
        margin-bottom: 0.3rem;
        letter-spacing: 2px;
        filter: drop-shadow(0 0 20px rgba(0, 200, 255, 0.5));
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .hero-subtitle {
        text-align: center;
        color: #7dd3fc;
        font-size: 1.05rem;
        margin-bottom: 2.5rem;
        letter-spacing: 1px;
        opacity: 0.85;
    }

    /* === Glassmorphism card === */
    .glass-card {
        background: rgba(10, 25, 50, 0.55);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 200, 255, 0.2);
        border-radius: 20px;
        padding: 24px 28px;
        box-shadow:
            0 8px 32px rgba(0, 150, 255, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .glass-card:hover {
        border-color: rgba(0, 220, 255, 0.4);
        box-shadow:
            0 12px 40px rgba(0, 180, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    .section-title {
        color: #00d4ff;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
        text-shadow: 0 0 15px rgba(0, 200, 255, 0.5);
    }

    /* === Neon button === */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 16px 32px;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 2px;
        box-shadow:
            0 0 25px rgba(0, 180, 255, 0.5),
            0 4px 15px rgba(0, 100, 255, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        box-shadow:
            0 0 40px rgba(0, 220, 255, 0.9),
            0 6px 25px rgba(0, 150, 255, 0.5);
        transform: translateY(-3px);
        background: linear-gradient(135deg, #0080ff 0%, #00e5ff 100%);
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* === Price result card === */
    .price-result {
        background: linear-gradient(135deg,
            rgba(0, 100, 255, 0.18) 0%,
            rgba(120, 40, 255, 0.18) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(0, 220, 255, 0.5);
        border-radius: 24px;
        padding: 40px 30px;
        text-align: center;
        box-shadow:
            0 0 60px rgba(0, 180, 255, 0.35),
            inset 0 0 40px rgba(0, 150, 255, 0.1);
        animation: pulse-glow 2.5s ease-in-out infinite;
        margin: 1.5rem 0;
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 60px rgba(0, 180, 255, 0.35), inset 0 0 40px rgba(0, 150, 255, 0.1); }
        50% { box-shadow: 0 0 90px rgba(0, 220, 255, 0.6), inset 0 0 60px rgba(0, 180, 255, 0.18); }
    }

    .price-label {
        color: #7dd3fc;
        font-size: 0.95rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .price-value {
        font-size: 3.6rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #ffffff, #7b2fff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 3s linear infinite;
        filter: drop-shadow(0 0 25px rgba(0, 200, 255, 0.6));
        line-height: 1.1;
    }

    .price-currency {
        color: #4dd0e1;
        font-size: 1rem;
        margin-top: 8px;
        letter-spacing: 2px;
    }

    /* === Small stat card === */
    .stat-card {
        background: rgba(10, 25, 50, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 200, 255, 0.18);
        border-radius: 16px;
        padding: 18px 20px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        border-color: rgba(0, 220, 255, 0.4);
        transform: translateY(-3px);
    }

    .stat-label {
        color: #64b5f6;
        font-size: 0.78rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .stat-value {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 800;
        text-shadow: 0 0 12px rgba(0, 200, 255, 0.6);
    }

    /* === Input improvements === */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(5, 15, 30, 0.7) !important;
        border: 1px solid rgba(0, 200, 255, 0.25) !important;
        border-radius: 10px !important;
        color: #e0f7ff !important;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(0, 220, 255, 0.5) !important;
    }

    /* === Sliders === */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #0066ff, #00d4ff) !important;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 220, 255, 0.9) !important;
    }

    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 25, 50, 0.5);
        border-radius: 14px;
        padding: 6px;
        gap: 4px;
        border: 1px solid rgba(0, 200, 255, 0.15);
    }

    .stTabs [data-baseweb="tab"] {
        color: #7dd3fc;
        border-radius: 10px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0066ff, #00d4ff) !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(0, 180, 255, 0.5);
    }

    /* === Text === */
    label, .stMarkdown p, .stSelectbox label {
        color: #b3e5fc !important;
        font-weight: 500;
    }

    /* === Spinner === */
    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Load model and dataset
@st.cache_resource
def load_model():
    return joblib.load("best_ridge_pipeline.pkl")

@st.cache_data
def load_dataset():
    return pd.read_csv("car_price_engineered.csv")

try:
    model = load_model()
    df = load_dataset()
except Exception as e:
    st.error(f"❌ Failed to load resources: {e}")
    st.stop()

# Extract unique options
MAKES = sorted(df["Car Make"].unique().tolist())
POWERTRAINS = sorted(df["Powertrain Type"].unique().tolist())

# Hero header
st.markdown('<div class="hero-title">🏎️ SUPERCAR PRICE AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">'
    '◆ AI-Powered Price Prediction for Supercars ◆'
    '</div>',
    unsafe_allow_html=True
)

# Model stats bar
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">R² Score</div>
        <div class="stat-value">0.9295</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">MAE (Avg)</div>
        <div class="stat-value">$48.5K</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Brands</div>
        <div class="stat-value">38</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Models</div>
        <div class="stat-value">176</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#Input form
st.markdown('<div class="section-title">⚙️ VEHICLE SPECIFICATIONS</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        car_make = st.selectbox(
            "🏭 Car Make",
            MAKES,
            index=MAKES.index("Ferrari") if "Ferrari" in MAKES else 0
        )

        # Filter models based on selected make
        models_for_make = sorted(
            df[df["Car Make"] == car_make]["Car Model"].unique().tolist()
        )
        car_model = st.selectbox("🚗 Car Model", models_for_make)

        powertrain = st.selectbox(
            "⚡ Powertrain Type",
            POWERTRAINS,
            index=POWERTRAINS.index("ICE") if "ICE" in POWERTRAINS else 0
        )

    with col2:
        engine_size = st.slider("🔧 Engine Size (L)", 0.0, 8.4, 4.0, step=0.1)
        horsepower = st.slider("🐎 Horsepower (HP)", 181, 2000, 700, step=1)

    col3, col4, col5 = st.columns(3)
    with col3:
        torque = st.slider("💪 Torque (lb-ft)", 0, 2000, 550, step=1)
    with col4:
        zero_sixty = st.slider("⏱️ 0-60 MPH (seconds)", 1.8, 6.5, 3.0, step=0.1)
    with col5:
        car_age = st.slider("📅 Car Age (years)", 3, 61, 5, step=1)

    st.markdown('</div>', unsafe_allow_html=True)

# Predict buttom
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🚀  PREDICT PRICE  🚀", use_container_width=True)

# Result
if predict_btn:
    input_data = pd.DataFrame([{
        "Car Make": car_make,
        "Car Model": car_model,
        "Engine Size (L)": engine_size,
        "Horsepower": horsepower,
        "Torque (lb-ft)": torque,
        "0-60 MPH Time (seconds)": zero_sixty,
        "Powertrain Type": powertrain,
        "Car Age": car_age,
    }])

    with st.spinner("✨ Calculating..."):
        try:
            prediction = float(model.predict(input_data)[0])
            prediction = max(prediction, 0)
        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.stop()

    # Price result card
    st.markdown(f"""
    <div class="price-result">
        <div class="price-label">💰 PREDICTED PRICE</div>
        <div class="price-value">${prediction:,.0f}</div>
        <div class="price-currency">US DOLLARS</div>
    </div>
    """, unsafe_allow_html=True)

    # Charts
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Market Comparison", "📉 Feature Radar"])

    with tab1:
        # Compare with brand average
        brand_data = df[df["Car Make"] == car_make]["Price (in USD)"]
        global_avg = df["Price (in USD)"].mean()
        brand_avg = brand_data.mean()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Your Prediction", f"{car_make} Avg", "Market Avg"],
            y=[prediction, brand_avg, global_avg],
            marker=dict(
                color=["#00d4ff", "#7b2fff", "#4a5568"],
                line=dict(color="rgba(0, 200, 255, 0.5)", width=2)
            ),
            text=[f"${v:,.0f}" for v in [prediction, brand_avg, global_avg]],
            textposition="outside",
            textfont=dict(color="#e0f7ff", size=13),
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,25,50,0.3)",
            font=dict(color="#b3e5fc", family="Arial"),
            yaxis=dict(gridcolor="rgba(0,200,255,0.1)", title="Price (USD)"),
            xaxis=dict(gridcolor="rgba(0,200,255,0.1)"),
            height=400,
            margin=dict(t=30, b=30),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Radar chart normalized to dataset ranges
        features = {
            "Horsepower": (horsepower, df["Horsepower"].min(), df["Horsepower"].max()),
            "Torque": (torque, df["Torque (lb-ft)"].min(), df["Torque (lb-ft)"].max()),
            "Engine": (engine_size, df["Engine Size (L)"].min(), df["Engine Size (L)"].max()),
            "Acceleration": (
                7.0 - zero_sixty,
                7.0 - df["0-60 MPH Time (seconds)"].max(),
                7.0 - df["0-60 MPH Time (seconds)"].min()
            ),
            "Newness": (
                61 - car_age,
                61 - df["Car Age"].max(),
                61 - df["Car Age"].min()
            ),
        }

        labels, values = [], []
        for name, (val, mn, mx) in features.items():
            norm = (val - mn) / (mx - mn + 1e-9)
            norm = max(0, min(1, norm))
            labels.append(name)
            values.append(round(norm * 100, 1))

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(0, 200, 255, 0.25)",
            line=dict(color="#00d4ff", width=3),
            name="Vehicle Specs",
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b3e5fc"),
            polar=dict(
                bgcolor="rgba(10,25,50,0.4)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    gridcolor="rgba(0,200,255,0.15)",
                    tickfont=dict(color="#7dd3fc", size=10),
                ),
                angularaxis=dict(
                    gridcolor="rgba(0,200,255,0.15)",
                    tickfont=dict(color="#b3e5fc", size=12),
                ),
            ),
            height=450,
            showlegend=False,
            margin=dict(t=30, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Summary
    st.markdown('<div class="section-title">📋 SPECIFICATIONS SUMMARY</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(f"**🏭 Make:** {car_make}")
        st.markdown(f"**🚗 Model:** {car_model}")
        st.markdown(f"**⚡ Powertrain:** {powertrain}")
    with d2:
        st.markdown(f"**🔧 Engine Size:** {engine_size} L")
        st.markdown(f"**🐎 Horsepower:** {horsepower} HP")
        st.markdown(f"**💪 Torque:** {torque} lb-ft")
    with d3:
        st.markdown(f"**⏱️ 0-60 MPH:** {zero_sixty} sec")
        st.markdown(f"**📅 Car Age:** {car_age} years")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 50px 20px; opacity: 0.7;">
        <div style="font-size: 3rem; margin-bottom: 15px;">🏁</div>
        <div style="color: #7dd3fc; font-size: 1.1rem; letter-spacing: 2px;">
            Configure your vehicle and hit PREDICT
        </div>
    </div>
    """, unsafe_allow_html=True)