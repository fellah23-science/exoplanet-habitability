import streamlit as st
import math
import pandas as pd
import random

# --- Constants ---
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
sigma = 5.670374419e-8 # Stefan-Boltzmann constant (W/m^2 K^4)
M_sun = 1.989e30       # Mass of Sun (kg)
L_sun = 3.828e26       # Luminosity of Sun (W)

st.set_page_config(page_title="ExoHabit: Exoplanet Habitability", layout="wide")

# --- Main Title ---
st.title("🌌 ExoHabit: Exoplanet Habitability Explorer")

# --- Tabs for organization ---
tab1, tab2, tab3 = st.tabs(["🪐 Calculator", "📊 Exoplanet Data", "💫 Learn & Discover"])

# --- TAB 1: Habitability Calculator ---
with tab1:
    st.header("🪐 Habitability Calculator")

    # --- STAR PROPERTIES ---
    st.subheader("⭐ Star Properties")
    M_star = st.number_input(
        "Star Mass (M☉)", value=1.0,
        help="Mass of the star compared to the Sun (1 = Sun)."
    )

    L_star = st.number_input(
        "Star Luminosity (L☉)", value=1.0,
        help="Brightness of the star compared to the Sun (1 = same as Sun)."
    )

    # --- PLANET PROPERTIES ---
    st.subheader("🪐 Planet Properties")
    K = st.number_input(
        "Radial Velocity Amplitude (m/s)", value=10.0,
        help="Change in the star's velocity caused by the planet's gravitational pull."
    )

    P_days = st.number_input(
        "Orbital Period (days)", value=365.0,
        help="Time it takes for the planet to complete one orbit around the star."
    )

    e = st.number_input(
        "Orbital Eccentricity (0=circle)", value=0.0, min_value=0.0, max_value=0.99,
        help="How stretched out the orbit is (0 = circular, 1 = highly elongated)."
    )

    i_deg = st.number_input(
        "Inclination (degrees)", value=90.0, min_value=0.0, max_value=180.0,
        help="Tilt of the planet's orbit relative to the line of sight from Earth."
    )

    A = st.number_input(
        "Albedo (reflectivity)", value=0.3, min_value=0.0, max_value=1.0,
        help="Fraction of starlight reflected by the planet (0 = none, 1 = all)."
    )

    # --- Calculations ---
    P = P_days * 24 * 3600  # seconds
    i = math.radians(i_deg)
    M_star_kg = M_star * M_sun
    L_star_W = L_star * L_sun

    # Planet mass
    M_p = (K * math.sqrt(1 - e**2) * (M_star_kg)**(2/3) * (P/(2*math.pi*G))**(1/3)) / math.sin(i)

    # Orbital radius
    a = ((G * M_star_kg * P**2) / (4 * math.pi**2))**(1/3)

    # Equilibrium temperature
    F = L_star_W / (4 * math.pi * a**2)
    T_eq = ((F * (1-A)) / (4*sigma))**0.25

    # Habitable Zone (scaled with luminosity)
    HZ_inner = 0.95 * math.sqrt(L_star) * 1.496e11
    HZ_outer = 1.67 * math.sqrt(L_star) * 1.496e11
    if HZ_inner <= a <= HZ_outer:
        habitability = "✅ Likely Habitable"
    else:
        habitability = "❌ Not in Habitable Zone"

    # --- Results ---
    st.header("Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Planet Mass (Earth masses)", f"{M_p/5.972e24:.2f}")
        st.metric("Orbital Radius (AU)", f"{a/1.496e11:.2f}")
    with col2:
        st.metric("Equilibrium Temperature (K)", f"{T_eq:.1f}")
        st.markdown(f"**Habitability:** {habitability}")

# --- TAB 2: Exoplanet Data Table (plain, no highlight) ---
with tab2:
    st.header("📊 Explore Exoplanet Data")

    data = {
        "Planet Name": ["Kepler-22b", "Kepler-452b", "Proxima Centauri b", "TRAPPIST-1e", "Kepler-186f", "Gliese 667 Cc"],
        "Distance (ly)": [620, 1400, 4.24, 39.6, 490, 23.6],
        "Orbital Distance (AU)": [0.85, 1.05, 0.05, 0.029, 0.36, 0.125],
        "Stellar Flux (Earth=1)": [1.11, 1.04, 0.65, 0.66, 0.26, 0.9],
        "Eccentricity": [0.02, 0.05, 0.15, 0.005, 0.02, 0.1],
        "Planet Mass (Earth=1)": [2.4, 5.0, 1.3, 0.77, 1.4, 4.5]
    }

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Exoplanet Data", csv, "exoplanet_data.csv", "text/csv")

    selected_planet = st.selectbox("🔹 Choose a planet to analyze:", df["Planet Name"])
    planet_info = df[df["Planet Name"] == selected_planet]
    st.success(f"✅ Selected: {selected_planet}")
    st.dataframe(planet_info)  # Show as dataframe

# --- TAB 3: Fun Facts Section ---
with tab3:
    st.header("💫 Learn & Discover")

    st.write("Curious about exoplanets and stars? Tap the button below for random space facts! 🌠")

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





