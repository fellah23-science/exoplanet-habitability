import streamlit as st
import math
import numpy as np
import pandas as pd
import random
import streamlit.components.v1 as components

# --- CONSTANTS ---
G = 6.67430e-11
sigma = 5.670374419e-8
M_sun = 1.989e30
L_sun = 3.828e26
M_earth = 5.972e24
DAY = 86400.0
AU = 1.496e11

# --- PAGE SETUP ---
st.set_page_config(page_title="ExoHabit App", layout="wide")
st.title("🌌 ExoHabit – Exoplanet Habitability Calculator")

# --- PLANET DATA ---
planet_data = [
    {"Planet":"Kepler-22b","Eccentricity":0.72,"Orbital Period (days)":289.86,"Inclination (°)":89.764,
     "Planet Mass (M⊕)":36,"Star Mass (M☉)":0.97,"Star Luminosity (log10 L/L☉)":-0.19},
    {"Planet":"Kepler-452b","Eccentricity":0.0,"Orbital Period (days)":384.84,"Inclination (°)":89.99,
     "Planet Mass (M⊕)":2.0,"Star Mass (M☉)":0.892,"Star Luminosity (log10 L/L☉)":0.084},
    {"Planet":"Proxima Centauri b","Eccentricity":0.02,"Orbital Period (days)":11.1,"Inclination (°)":90.0,
     "Planet Mass (M⊕)":1.07,"Star Mass (M☉)":0.12,"Star Luminosity (log10 L/L☉)":-2.8},
    {"Planet":"TRAPPIST-1e","Eccentricity":0.085,"Orbital Period (days)":6.09,"Inclination (°)":89.86,
     "Planet Mass (M⊕)":0.62,"Star Mass (M☉)":0.08,"Star Luminosity (log10 L/L☉)":-2.13},
    {"Planet":"Gliese 12b","Eccentricity":0.5,"Orbital Period (days)":12.76,"Inclination (°)":89.2,
     "Planet Mass (M⊕)":10,"Star Mass (M☉)":0.241,"Star Luminosity (log10 L/L☉)":-2.13}
]
df_planets = pd.DataFrame(planet_data)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🪐 Calculator", "📊 Exoplanet Data", "💫 Learn & Discover", "🌌 Galaxy Notes",
    "📝 Assessment Zone", "🤖 SpaceBot AI", "🌞 Solar System Simulation"
])

# ----------------- TAB 1: HABITABILITY CALCULATOR -----------------
with tab1:
    st.header("🪐 Habitability Calculator")
    st.write("Input the parameters of any exoplanet or star to calculate its habitability details.")
    
    st.subheader("⭐ Star Properties")
    col1, col2 = st.columns(2)
    with col1:
        M_star = st.number_input("Star Mass (M☉)", value=1.0, min_value=0.01)
        L_star_log = st.number_input("Star Luminosity (log10 L/L☉)", value=0.0)
    with col2:
        st.markdown("")
    
    st.subheader("🌍 Planet Properties")
    col1, col2 = st.columns(2)
    with col1:
        Planet_mass = st.number_input("Planet Mass (M⊕)", value=1.0, min_value=0.0)
        e = st.number_input("Eccentricity (0=circle)", value=0.0, min_value=0.0, max_value=0.99)
        A = st.number_input("Albedo (reflectivity)", value=0.3, min_value=0.0, max_value=1.0)
    with col2:
        P_days = st.number_input("Orbital Period (days)", value=365.0, min_value=0.1)
        i_deg = st.number_input("Inclination (degrees)", value=90.0, min_value=0.0, max_value=180.0)

    # --- Calculations ---
    P_sec = P_days * DAY
    i_rad = math.radians(i_deg)
    M_star_kg = M_star * M_sun
    M_p_kg = Planet_mass * M_earth

    K = ((2 * np.pi * G / P_sec)**(1/3) * (M_p_kg * np.sin(i_rad)) /
         (M_star_kg + M_p_kg)**(2/3) * 1 / np.sqrt(1 - e**2))

    a = ((G * M_star_kg * P_sec**2) / (4 * math.pi**2))**(1/3)
    L_star = 10**L_star_log
    L_star_W = L_star * L_sun
    F = L_star_W / (4 * math.pi * a**2)
    T_eq = ((F * (1 - A)) / (4 * sigma))**0.25

    HZ_inner = 0.95 * math.sqrt(L_star) * AU
    HZ_outer = 1.67 * math.sqrt(L_star) * AU
    habitability = "✅ Likely Habitable" if HZ_inner <= a <= HZ_outer else "❌ Not in Habitable Zone"

    # --- Results ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Radial Velocity (m/s)", f"{K:.2f}")
    with col2:
        st.metric("Orbital Distance (AU)", f"{a/AU:.3f}")
    with col3:
        st.metric("Equilibrium Temperature (K)", f"{T_eq:.1f}")

    st.markdown(f"**Habitability:** {habitability}")
# ---------------- TAB 7: SOLAR SYSTEM SIMULATION ----------------
with tab7:
    st.markdown('<div class="title-box">🌌 Welcome to Exoplanet Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="solar-box">Solar System</div>', unsafe_allow_html=True)

    # ---------------- CSS ONLY FOR TAB 7 ----------------
    st.markdown("""
    <style>
    /* Solar area only */
    .solar-container {
        position: relative;
        width: 700px;
        height: 700px;
        margin: auto;
        margin-top: 30px;
        background-color: #0b0c1a;  /* Dark only for simulation */
        border-radius: 20px;
    }

    /* Sun */
    .sun {
        width: 140px;
        height: 140px;
        background: radial-gradient(circle at 30% 30%, #fff59d, #ffd700, #ff8c00);
        border-radius: 50%;
        position: absolute;
        top: 280px;
        left: 280px;
        box-shadow: 0 0 70px yellow;
    }

    /* Orbits */
    .orbit {
        position: absolute;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 50%;
        animation: spin linear infinite;
    }

    /* Planets */
    .planet {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        position: absolute;
        top: -24px;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 0 20px #00bfff;
    }

    @keyframes spin {
        from {transform: rotate(0deg);}
        to {transform: rotate(360deg);}
    }

    /* Title */
    .title-box {
        text-align: center;
        font-size: 46px;
        font-weight: bold;
        margin-top: 20px;
        color: white;
    }

    /* Solar system title box */
    .solar-box {
        width: 280px;
        margin: auto;
        margin-top: 20px;
        text-align: center;
        padding: 15px;
        border-radius: 18px;
        background-color: rgba(20,40,90,0.85);
        box-shadow: 0 0 25px #00bfff;
        font-size: 30px;
        font-weight: bold;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- SOLAR SYSTEM HTML ----------------
    solar_html = """
    <div class="solar-container">
        <div class="sun"></div>

        <div class="orbit" style="width:180px;height:180px;top:260px;left:260px;animation-duration:8s;">
            <div class="planet" style="background:gray;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Mercury</div>
        </div>

        <div class="orbit" style="width:250px;height:250px;top:225px;left:225px;animation-duration:12s;">
            <div class="planet" style="background:orange;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Venus</div>
        </div>

        <div class="orbit" style="width:320px;height:320px;top:190px;left:190px;animation-duration:16s;">
            <div class="planet" style="background:blue;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Earth</div>
        </div>

        <div class="orbit" style="width:390px;height:390px;top:155px;left:155px;animation-duration:20s;">
            <div class="planet" style="background:red;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Mars</div>
        </div>

        <div class="orbit" style="width:470px;height:470px;top:115px;left:115px;animation-duration:24s;">
            <div class="planet" style="background:tan;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Jupiter</div>
        </div>

        <div class="orbit" style="width:550px;height:550px;top:75px;left:75px;animation-duration:28s;">
            <div class="planet" style="background:gold;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Saturn</div>
        </div>

        <div class="orbit" style="width:620px;height:620px;top:40px;left:40px;animation-duration:32s;">
            <div class="planet" style="background:lightblue;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Uranus</div>
        </div>

        <div class="orbit" style="width:680px;height:680px;top:10px;left:10px;animation-duration:36s;">
            <div class="planet" style="background:darkblue;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:white; font-size:12px;">Neptune</div>
        </div>
    </div>
    """
    st.markdown(solar_html, unsafe_allow_html=True)

    # ---------------- FACTS DROPDOWN ----------------
    st.markdown("## 🪐 Planet Facts")
    selected = st.selectbox("Choose a planet", list(planet_facts.keys()))
    st.write(planet_facts[selected])
