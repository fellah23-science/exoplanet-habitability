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

# ----------------- TAB 7: SOLAR SYSTEM SIMULATION -----------------
with tab7:
    st.header("🌞 Solar System Simulation")
    
    planet_facts = {
        "Mercury": "Mercury is the closest planet to the Sun.",
        "Venus": "Venus is the hottest planet in the solar system.",
        "Earth": "Earth is the only known planet that supports life.",
        "Mars": "Mars is called the Red Planet.",
        "Jupiter": "Jupiter is the largest planet.",
        "Saturn": "Saturn has beautiful rings.",
        "Uranus": "Uranus rotates sideways.",
        "Neptune": "Neptune has the strongest winds."
    }

    solar_html = """
    <style>
    .solar-system {
        background-color: #0b0c1a;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        position: relative;
    }
    .sun {
        width: 50px;
        height: 50px;
        background: yellow;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 30px 10px yellow;
        z-index: 100;
    }
    .orbit {
        position: absolute;
        top: 50%;
        left: 50%;
        border-radius: 50%;
        transform-origin: center center;
    }
    .planet {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 0 10px #fff;
    }
    .Mercury { background: gray; animation: rotateMerc 5s linear infinite; }
    .Venus { background: yellow; animation: rotateVen 8s linear infinite; }
    .Earth { background: blue; animation: rotateEar 10s linear infinite; }
    .Mars { background: red; animation: rotateMar 12s linear infinite; }
    .Jupiter { background: orange; animation: rotateJup 14s linear infinite; }
    .Saturn { background: #f5deb3; animation: rotateSat 16s linear infinite; }
    .Uranus { background: #00ffff; animation: rotateUra 18s linear infinite; }
    .Neptune { background: #0000ff; animation: rotateNep 20s linear infinite; }

    @keyframes rotateMerc { from { transform: rotate(0deg) translateX(60px) rotate(0deg);} to { transform: rotate(360deg) translateX(60px) rotate(-360deg);}}
    @keyframes rotateVen { from { transform: rotate(0deg) translateX(80px) rotate(0deg);} to { transform: rotate(360deg) translateX(80px) rotate(-360deg);}}
    @keyframes rotateEar { from { transform: rotate(0deg) translateX(100px) rotate(0deg);} to { transform: rotate(360deg) translateX(100px) rotate(-360deg);}}
    @keyframes rotateMar { from { transform: rotate(0deg) translateX(120px) rotate(0deg);} to { transform: rotate(360deg) translateX(120px) rotate(-360deg);}}
    @keyframes rotateJup { from { transform: rotate(0deg) translateX(160px) rotate(0deg);} to { transform: rotate(360deg) translateX(160px) rotate(-360deg);}}
    @keyframes rotateSat { from { transform: rotate(0deg) translateX(190px) rotate(0deg);} to { transform: rotate(360deg) translateX(190px) rotate(-360deg);}}
    @keyframes rotateUra { from { transform: rotate(0deg) translateX(220px) rotate(0deg);} to { transform: rotate(360deg) translateX(220px) rotate(-360deg);}}
    @keyframes rotateNep { from { transform: rotate(0deg) translateX(250px) rotate(0deg);} to { transform: rotate(360deg) translateX(250px) rotate(-360deg);}}
    </style>

    <div class="solar-system" style="height:600px;">
        <div class="sun"></div>
        <div class="orbit Mercury"><div class="planet Mercury" title="Mercury"></div></div>
        <div class="orbit Venus"><div class="planet Venus" title="Venus"></div></div>
        <div class="orbit Earth"><div class="planet Earth" title="Earth"></div></div>
        <div class="orbit Mars"><div class="planet Mars" title="Mars"></div></div>
        <div class="orbit Jupiter"><div class="planet Jupiter" title="Jupiter"></div></div>
        <div class="orbit Saturn"><div class="planet Saturn" title="Saturn"></div></div>
        <div class="orbit Uranus"><div class="planet Uranus" title="Uranus"></div></div>
        <div class="orbit Neptune"><div class="planet Neptune" title="Neptune"></div></div>
    </div>
    """
    components.html(solar_html, height=620)

    selected = st.selectbox("🪐 Choose a planet", list(planet_facts.keys()))
    st.write(planet_facts[selected])
 
