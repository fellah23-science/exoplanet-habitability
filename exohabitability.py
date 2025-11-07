import streamlit as st
import math
import numpy as np
import pandas as pd
import random

# --- Constants ---
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
sigma = 5.670374419e-8 # Stefan-Boltzmann constant (W/m^2 K^4)
M_sun = 1.989e30       # Mass of Sun (kg)
L_sun = 3.828e26       # Luminosity of Sun (W)
M_earth = 5.972e24     # Earth mass in kg
DAY = 86400.0          # seconds in a day
AU = 1.496e11          # meters

# --- Page setup ---
st.set_page_config(page_title="ExoHabit - Exoplanet Habitability Calculator", layout="wide")
st.title("🌌 ExoHabit – Exoplanet Habitability Calculator")

# --- Planet data ---
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

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🪐 Calculator", "📊 Exoplanet Data", "💫 Learn & Discover", "🌌 Galaxy Notes"])

# --- TAB 1: Habitability Calculator ---
with tab1:
    st.header("🪐 Habitability Calculator")
    st.write("Input the parameters of any exoplanet or star to calculate its habitability details.")

    # --- Star Properties ---
    st.subheader("⭐ Star Properties")
    col1, col2 = st.columns(2)
    with col1:
        M_star = st.number_input(
            "Star Mass (M☉)",
            value=1.0,
            min_value=0.01,
            help="Mass of the star in solar masses (1 M☉ = mass of our Sun)."
        )
        L_star_log = st.number_input(
            "Star Luminosity (log10 L/L☉)",
            value=0.0,
            help="Luminosity of the star in log10 units relative to Sun. 0 means same as Sun."
        )
    with col2:
        st.markdown("")

    # --- Planet Properties ---
    st.subheader("🌍 Planet Properties")
    col1, col2 = st.columns(2)
    with col1:
        Planet_mass = st.number_input(
            "Planet Mass (M⊕)",
            value=1.0,
            min_value=0.0,
            help="Mass of the planet in Earth masses (1 M⊕ = mass of Earth)."
        )
        e = st.number_input(
            "Eccentricity (0=circle)",
            value=0.0,
            min_value=0.0,
            max_value=0.99,
            help="Orbital shape of the planet; 0 is circular, closer to 1 is elongated."
        )
        A = st.number_input(
            "Albedo (reflectivity)",
            value=0.3,
            min_value=0.0,
            max_value=1.0,
            help="Fraction of starlight reflected by the planet; 0 = absorbs all, 1 = reflects all."
        )
    with col2:
        P_days = st.number_input(
            "Orbital Period (days)",
            value=365.0,
            min_value=0.1,
            help="Time the planet takes to orbit its star once, in Earth days."
        )
        i_deg = st.number_input(
            "Inclination (degrees)",
            value=90.0,
            min_value=0.0,
            max_value=180.0,
            help="Angle between orbital plane and line of sight; 90° = edge-on."
        )

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
    st.header("📊 Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Radial Velocity (m/s)",
            f"{K:.2f}",
            delta=None,
            help="Radial velocity induced on the star by the planet, measured in meters/second."
        )
    with col2:
        st.metric(
            "Orbital Distance (AU)",
            f"{a/AU:.3f}",
            delta=None,
            help="Average distance from the star in Astronomical Units (1 AU = Earth-Sun distance)."
        )
    with col3:
        st.metric(
            "Equilibrium Temperature (K)",
            f"{T_eq:.1f}",
            delta=None,
            help="Temperature the planet would have if it were a perfect blackbody, ignoring atmosphere."
        )

    st.markdown(f"**Habitability:** {habitability}  ⓘ Hover over each metric for details.")

# --- TAB 2: Exoplanet Data ---
with tab2:
    st.header("📊 Exoplanet Data")
    st.dataframe(
        df_planets,
        use_container_width=True,
        height=400
    )
    st.caption("Data includes orbital and physical parameters of select exoplanets. ")

# --- TAB 3: Learn & Discover ---
with tab3:
    st.header("💫 Learn & Discover")
    facts = [
        "🌠 The first exoplanet was discovered in 1992 around a pulsar called PSR B1257+12.",
        "🌞 Stars are mostly made of hydrogen and helium — just like our Sun.",
        "🌍 Over 5,000 exoplanets have been discovered so far!",
        "💧 The 'habitable zone' is where liquid water might exist.",
        "🌌 Eccentric orbits can make seasons on exoplanets very long or short.",
        "🧬 Studying exoplanets helps us understand how life forms elsewhere."
    ]
    if st.button("🌟 Show a Space Fact"):
        st.info(random.choice(facts))

# --- TAB 4: Galaxy Notes ---
with tab4:
    st.markdown(
        """
        <style>
        .galaxy-bg {
            background: radial-gradient(circle at top left, #e0e7ff, #f3e8ff, #e0f2fe);
            color: #2e1065;
            padding: 30px;
            border-radius: 25px;
            box-shadow: 0 0 25px rgba(173, 123, 255, 0.4);
            font-family: 'Trebuchet MS', sans-serif;
        }
        h1 {
            color: #2e1065;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }
        th {
            background-color: #c7d2fe;
            color: #1e1e1e;
            padding: 12px;
            text-align: left;
            font-size: 18px;
        }
        td {
            background-color: #faf5ff;
            color: #3b0764;
            padding: 12px;
            border-bottom: 2px solid #e0e7ff;
        }
        tr:hover td {
            background-color: #ede9fe;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<div class='galaxy-bg'>", unsafe_allow_html=True)
    st.markdown("<h1>🌌 Galaxy Notes </h1>", unsafe_allow_html=True)
    st.markdown("""
    <table>
        <tr><th>🌠 Cosmic Phenomenon</th><th>✨ Description</th></tr>
        <tr><td>🕳️ Black Hole</td><td>Formed when a massive star collapses under its own gravity. Its pull is so strong that even light cannot escape!</td></tr>
        <tr><td>💥 Supernova</td><td>A powerful explosion of a dying star that creates heavy elements like gold and iron.</td></tr>
        <tr><td>🌠 Nebula</td><td>Beautiful clouds of gas and dust in space — the birthplace of new stars.</td></tr>
        <tr><td>🌞 Star</td><td>A glowing sphere of hot gas that shines because of nuclear fusion in its core.</td></tr>
        <tr><td>🪐 Exoplanet</td><td>Planets orbiting stars outside our Solar System. Some could support life!</td></tr>
        <tr><td>🌌 Galaxy</td><td>Vast systems of stars, gas, dust, and dark matter held together by gravity. We live in the Milky Way Galaxy.</td></tr>
        <tr><td>🌑 Dark Matter</td><td>Invisible matter that makes up most of the universe’s mass — we can’t see it, but we feel its gravity.</td></tr>
        <tr><td>⚡ Neutron Star</td><td>What remains after a massive star explodes — tiny but incredibly dense!</td></tr>
        <tr><td>☀️ Solar System</td><td>Our cosmic neighborhood — one Sun, eight planets, and countless asteroids and comets.</td></tr>
    </table>
    """, unsafe_allow_html=True)



   
      
       
       
        
      
       
       
    
   

   
  

    
 







