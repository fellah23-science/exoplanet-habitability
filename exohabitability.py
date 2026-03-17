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
st.set_page_config(page_title="ExoHabit", layout="wide")
st.title("🌌 ExoHabit – Exoplanet Explorer")

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🪐 Calculator", 
    "📊 Exoplanet Data", 
    "💫 Learn & Discover", 
    "🌌 Galaxy Notes", 
    "📝 Assessment Zone", 
    "🤖 SpaceBot AI", 
    "🌞 Solar System Simulation"
])

# ----------------- TAB 1: Habitability Calculator -----------------
with tab1:
    st.header("🪐 Habitability Calculator")
    st.write("Input parameters of a star or planet to calculate habitability.")

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
        i_deg = st.number_input("Inclination (°)", value=90.0, min_value=0.0, max_value=180.0)

    # Calculations
    P_sec = P_days * DAY
    i_rad = math.radians(i_deg)
    M_star_kg = M_star * M_sun
    M_p_kg = Planet_mass * M_earth
    K = ((2 * np.pi * G / P_sec)**(1/3) * (M_p_kg * np.sin(i_rad)) /
         (M_star_kg + M_p_kg)**(2/3) / np.sqrt(1 - e**2))
    a = ((G * M_star_kg * P_sec**2) / (4 * math.pi**2))**(1/3)
    L_star = 10**L_star_log
    L_star_W = L_star * L_sun
    F = L_star_W / (4 * math.pi * a**2)
    T_eq = ((F * (1 - A)) / (4 * sigma))**0.25
    HZ_inner = 0.95 * math.sqrt(L_star) * AU
    HZ_outer = 1.67 * math.sqrt(L_star) * AU
    habitability = "✅ Likely Habitable" if HZ_inner <= a <= HZ_outer else "❌ Not in Habitable Zone"

    col1, col2, col3 = st.columns(3)
    col1.metric("Radial Velocity (m/s)", f"{K:.2f}")
    col2.metric("Orbital Distance (AU)", f"{a/AU:.3f}")
    col3.metric("Equilibrium Temperature (K)", f"{T_eq:.1f}")
    st.markdown(f"**Habitability:** {habitability}")

# ----------------- TAB 2: Exoplanet Data -----------------
with tab2:
    st.header("📊 Exoplanet Data")
    st.dataframe(df_planets, use_container_width=True, height=400)

# ----------------- TAB 3: Learn & Discover -----------------
with tab3:
    st.header("💫 Learn & Discover")
    facts = [
        "🌠 First exoplanet discovered: PSR B1257+12.",
        "🌞 Stars are mostly hydrogen and helium.",
        "🌍 Over 5,000 exoplanets discovered so far!",
        "💧 Habitable zone = where liquid water can exist.",
        "🌌 Eccentric orbits change exoplanet seasons.",
        "🧬 Studying exoplanets helps us understand life elsewhere."
    ]
    if st.button("🌟 Show a Space Fact"):
        st.info(random.choice(facts))

# ----------------- TAB 4: Galaxy Notes -----------------
with tab4:
    st.header("🌌 Galaxy Notes")
    st.markdown("""
    <table style="width:100%; border-collapse:collapse;">
        <tr><th>Cosmic Phenomenon</th><th>Description</th></tr>
        <tr><td>Black Hole</td><td>Gravity so strong even light can't escape.</td></tr>
        <tr><td>Supernova</td><td>Explosion of a dying star creating heavy elements.</td></tr>
        <tr><td>Nebula</td><td>Clouds of gas and dust; birthplace of stars.</td></tr>
        <tr><td>Star</td><td>Glowing gas sphere shining due to nuclear fusion.</td></tr>
        <tr><td>Exoplanet</td><td>Planets outside our Solar System.</td></tr>
        <tr><td>Galaxy</td><td>Vast system of stars, dust, gas & dark matter.</td></tr>
        <tr><td>Dark Matter</td><td>Invisible matter felt via gravity.</td></tr>
        <tr><td>Neutron Star</td><td>Tiny, dense remnants of massive stars.</td></tr>
        <tr><td>Solar System</td><td>Our Sun, planets, asteroids, and comets.</td></tr>
    </table>
    """, unsafe_allow_html=True)

# ----------------- TAB 5: Assessment Zone -----------------
with tab5:
    st.header("📝 Assessment Zone")
    quiz_choice = st.radio("Select a Quiz:", ["Space Geek Quiz", "Exoplanet Knowledge Quiz"])

    quizzes = {
        "Space Geek Quiz": [
            {"q":"Which planet is closest to the Sun?","options":["Mercury","Venus","Earth","Mars"],"a":"Mercury"},
            {"q":"Largest planet in the solar system?","options":["Jupiter","Saturn","Earth","Mars"],"a":"Jupiter"},
            {"q":"Planet known as Red Planet?","options":["Venus","Mars","Mercury","Jupiter"],"a":"Mars"},
            {"q":"Which planet rotates sideways?","options":["Uranus","Earth","Venus","Neptune"],"a":"Uranus"},
            {"q":"Hottest planet?","options":["Earth","Venus","Mercury","Mars"],"a":"Venus"}
        ],
        "Exoplanet Knowledge Quiz": [
            {"q":"First exoplanet discovered in 1992?","options":["PSR B1257+12","Kepler-22b","Proxima Centauri b","TRAPPIST-1e"],"a":"PSR B1257+12"},
            {"q":"Planet with 384 days orbital period?","options":["Kepler-22b","Kepler-452b","TRAPPIST-1e","Gliese 12b"],"a":"Kepler-452b"},
            {"q":"Closest exoplanet to Earth?","options":["Kepler-22b","Proxima Centauri b","TRAPPIST-1e","Gliese 12b"],"a":"Proxima Centauri b"},
            {"q":"TRAPPIST-1e mass (M⊕)?","options":["0.62","2","36","10"],"a":"0.62"},
            {"q":"Gliese 12b eccentricity?","options":["0.5","0.02","0.085","0.0"],"a":"0.5"}
        ]
    }

    if st.button("Start Quiz"):
        score = 0
        wrong_answers = []
        for idx, q in enumerate(quizzes[quiz_choice]):
            ans = st.radio(f"Q{idx+1}: {q['q']}", q['options'], key=f"{quiz_choice}_{idx}")
            if ans == q['a']:
                score += 1
            else:
                wrong_answers.append(f"Q{idx+1}: Correct answer: {q['a']}")
        st.success(f"You scored {score}/{len(quizzes[quiz_choice])}")
        if score >= 3:
            st.balloons()
            st.info("🌟 Space Geek / Astronomer Level Unlocked!")
        if wrong_answers:
            st.warning("You missed the following:")
            for w in wrong_answers:
                st.write(w)

# ----------------- TAB 6: SpaceBot AI -----------------
with tab6:
    st.header("🤖 SpaceBot AI")
    user_q = st.text_input("Ask me anything about space or exoplanets:")
    if st.button("Ask SpaceBot"):
        if user_q:
            ans = "Sorry, I don't know the answer. Try asking something else."
            keywords = {
                "planet":"Planets are celestial bodies orbiting stars.",
                "star":"Stars are glowing balls of gas undergoing nuclear fusion.",
                "exoplanet":"Exoplanets are planets outside our Solar System.",
                "galaxy":"Galaxies are vast collections of stars, gas, dust, and dark matter.",
                "black hole":"Black holes are collapsed massive stars with gravity so strong even light cannot escape."
            }
            for k,v in keywords.items():
                if k.lower() in user_q.lower():
                    ans = v
                    break
            st.info(ans)

# ----------------- TAB 7: Solar System Simulation -----------------
with tab7:
    st.header("🌞 Solar System Simulation")
    st.markdown('<div class="solar-box">Solar System</div>', unsafe_allow_html=True)
    solar_html = """
    <div style="position: relative; width:700px; height:700px; margin:auto;">
        <div style="width:140px;height:140px;background:radial-gradient(circle at 30% 30%, #fff59d,#ffd700,#ff8c00);border-radius:50%;position:absolute;top:280px;left:280px;box-shadow:0 0 70px yellow;"></div>
    """
    colors = ["gray","orange","blue","red","tan","gold","lightblue","darkblue"]
    names = ["Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]
    facts = ["Closest planet to the Sun.","Hottest planet.","Supports life.","Red Planet.","Largest planet.","Beautiful rings.","Rotates sideways.","Strongest winds."]
    for i, (c, n, f) in enumerate(zip(colors, names, facts)):
        size = 48
        orbit = 180 + i*70
        solar_html += f"""
        <div style="position:absolute; width:{orbit}px; height:{orbit}px; border:1px solid rgba(255,255,255,0.12); border-radius:50%; top:{350-orbit//2}px; left:{350-orbit//2}px; animation:spin {8+i*4}s linear infinite;">
            <div title="{f}" style="width:{size}px; height:{size}px; background:{c}; border-radius:50%; position:absolute; top:-{size//2}px; left:50%; transform:translateX(-50%); box-shadow:0 0 20px #00bfff;"></div>
            <div style="position:absolute; top:-45px; left:50%; transform:translateX(-50%); color:black; font-size:12px;">{n}</div>
        </div>
        """
    solar_html += """
    </div>
    <style>
    @keyframes spin {from {transform: rotate(0deg);} to {transform: rotate(360deg);}}
    </style>
    """
    st.markdown(solar_html, unsafe_allow_html=True)
      
       
       
    
   

   
  

    
 








