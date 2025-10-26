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
tab1, tab2, tab3 = st.tabs(["🪐 Calculator", "📊 Exoplanet Data", "💫 Learn & Discover"])

# --- TAB 1: Habitability Calculator ---
with tab1:
    st.header("🪐 Habitability Calculator")
    st.write("Input the parameters of any exoplanet or star to calculate results:")

    # --- Star Properties ---
    st.subheader("⭐ Star Properties")
    col1, col2 = st.columns(2)
    with col1:
        M_star = st.number_input(
            "Star Mass (M☉)",
            value=1.0,
            min_value=0.01,
            help="Mass of the star compared to the Sun (1 = Sun)."
        )
        L_star_log = st.number_input(
            "Star Luminosity (log10 L/L☉)",
            value=0.0,
            help="Brightness of the star compared to the Sun in log scale."
        )
    with col2:
        # Moved Albedo to Planet Properties as requested
        pass

    # --- Planet Properties ---
    st.subheader("🪐 Planet Properties")
    col1, col2 = st.columns(2)
    with col1:
        Planet_mass = st.number_input(
            "Planet Mass (M⊕)",
            value=1.0,
            min_value=0.0,
            help="Mass of the planet in Earth masses."
        )
        e = st.number_input(
            "Eccentricity (0=circle)",
            value=0.0,
            min_value=0.0,
            max_value=0.99,
            help="How stretched out the orbit is (0 = circular, 1 = very elongated)."
        )
        A = st.number_input(
            "Albedo (reflectivity)",
            value=0.3,
            min_value=0.0,
            max_value=1.0,
            help="Fraction of starlight reflected by the planet (0 = none, 1 = all)."
        )
    with col2:
        P_days = st.number_input(
            "Orbital Period (days)",
            value=365.0,
            min_value=0.1,
            help="Time it takes for the planet to complete one orbit around its star."
        )
        i_deg = st.number_input(
            "Inclination (degrees)",
            value=90.0,
            min_value=0.0,
            max_value=180.0,
            help="Tilt of the planet's orbit relative to the line of sight from Earth."
        )

    # --- Calculations ---
    P_sec = P_days * DAY
    i_rad = math.radians(i_deg)
    M_star_kg = M_star * M_sun
    M_p_kg = Planet_mass * M_earth

    # Radial velocity amplitude K
    K = ( (2*np.pi*G/P_sec)**(1/3) * (M_p_kg * np.sin(i_rad)) /
          (M_star_kg + M_p_kg)**(2/3) * 1/np.sqrt(1 - e**2) )

    # Orbital radius
    a = ((G * M_star_kg * P_sec**2) / (4 * math.pi**2))**(1/3)

    # Equilibrium temperature
    L_star = 10**L_star_log
    L_star_W = L_star * L_sun
    F = L_star_W / (4 * math.pi * a**2)
    T_eq = ((F * (1-A)) / (4*sigma))**0.25

    # Habitable Zone
    HZ_inner = 0.95 * math.sqrt(L_star) * AU
    HZ_outer = 1.67 * math.sqrt(L_star) * AU
    if HZ_inner <= a <= HZ_outer:
        habitability = "✅ Likely Habitable"
    else:
        habitability = "❌ Not in Habitable Zone"

    # --- Results with definitions ---
    st.header("Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Radial Velocity (m/s)",
            value=f"{K:.2f}",
            help="The change in the star's velocity caused by the planet's gravitational pull."
        )
    with col2:
        st.metric(
            label="Orbital Distance (AU)",
            value=f"{a/AU:.3f}",
            help="The average distance between the planet and its star (1 AU = distance from Earth to Sun)."
        )
    with col3:
        st.metric(
            label="Equilibrium Temperature (K)",
            value=f"{T_eq:.1f}",
            help="The planet's temperature assuming it is a perfect blackbody, based on star luminosity and albedo."
        )

    st.markdown(f"**Habitability:** {habitability}")

# --- TAB 2: Exoplanet Data Table ---
with tab2:
    st.header("📊 Exoplanet Data")
    st.dataframe(df_planets, use_container_width=True)

# --- TAB 3: Fun Facts ---
with tab3:
    st.header("💫 Learn & Discover")
    facts = [
        "🌠 The first exoplanet was discovered in 1992 around a pulsar called PSR B1257+12.",
        "🌞 Stars are mostly made of hydrogen and helium — the same elements that power our Sun.",
        "🌍 Over 5,000 exoplanets have been discovered so far!",
        "💧 A planet’s ‘habitable zone’ is the distance where liquid water could exist.",
        "🌌 Eccentric orbits can make seasons on exoplanets extremely long or short.",
        "🧬 Studying exoplanets helps scientists understand how life might form on other worlds."
    ]
    if st.button("🌟 Show a Space Fact"):
        st.info(random.choice(facts))



   
  

    
 





