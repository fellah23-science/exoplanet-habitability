import streamlit as st
import math
import numpy as np
import pandas as pd
import random

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
tab1, tab2, tab3, tab4, tab5, tab6,tab7 = st.tabs([
    "🪐 Calculator", "📊 Exoplanet Data", "💫 Learn & Discover",
    "🌌 Galaxy Notes", "📝 Assessment Zone", "🤖 SpaceBot AI","planetarium view"
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

# ----------------- TAB 2: EXOPLANET DATA -----------------
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
    st.dataframe(planet_info)

# ----------------- TAB 3: LEARN & DISCOVER -----------------
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

# ----------------- TAB 4: GALAXY NOTES -----------------
with tab4:
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

# ----------------- TAB 5: ASSESSMENT ZONE -----------------
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

    user_answers = []
    for idx, q in enumerate(quizzes[quiz_choice]):
        ans = st.radio(f"Q{idx+1}: {q['q']}", q['options'], key=f"{quiz_choice}_{idx}")
        user_answers.append(ans)

    if st.button("Submit Quiz"):
        score = 0
        wrong_answers = []
        for idx, q in enumerate(quizzes[quiz_choice]):
            if user_answers[idx] == q['a']:
                score += 1
            else:
                wrong_answers.append(f"Q{idx+1}: Correct answer: {q['a']}")
        st.success(f"You scored {score}/{len(quizzes[quiz_choice])}")
        if score >= 3:
            st.balloons()
            st.info("🌟 You are a Space Geek / Astronomer!")
        if wrong_answers:
            st.warning("You missed the following:")
            for w in wrong_answers:
                st.write(w)

# ----------------- TAB 6: SPACEBOT AI -----------------
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
                "black hole":"Black holes are collapsed massive stars with gravity so strong even light cannot escape.",
                "supernova":"A supernova is an explosion of a dying star.",
                "nebula":"Nebulae are clouds of gas and dust, birthplace of stars.",
                "habitable zone":"The habitable zone is where liquid water may exist.",
                "asteroid":"Asteroids are rocky objects orbiting stars.",
                "comet":"Comets are icy objects with tails when near a star.",
                "pulsar":"Pulsars are rapidly spinning neutron stars that emit beams of radiation.",
                "telescope":"Telescopes allow astronomers to observe distant objects in space."
            }
            for k,v in keywords.items():
                if k.lower() in user_q.lower():
                    ans = v
                    break
            st.info(ans)
with tab7:
    import streamlit.components.v1 as components

    st.markdown("""
        <style>
        iframe {
            background-color: black !important;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("🌌 Planetarium View")
    solar_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        margin:0;
        background:black;
        overflow:hidden;
    }

    .space {
        position:relative;
        width:1250px;
        height:950px;
        margin:auto;
        background:black;
        overflow:hidden;
    }

    .star {
        position:absolute;
        border-radius:50%;
        background:white;
        animation: twinkle 3s infinite alternate;
    }

    @keyframes twinkle {
        from { opacity:0.2; }
        to { opacity:1; }
    }

    .sun {
        position:absolute;
        top:50%;
        left:50%;
        width:60px;
        height:60px;
        margin-left:-30px;
        margin-top:-30px;
        background:radial-gradient(circle, yellow, orange, darkorange);
        border-radius:50%;
        box-shadow:0 0 90px yellow;
    }

    .orbit {
        position:absolute;
        border:1px solid rgba(255,255,255,0.25);
        border-radius:50%;
        top:50%;
        left:50%;
        transform:translate(-50%,-50%);
    }

    .planet {
        position:absolute;
        border-radius:50%;
        transition: transform 0.3s;
        box-shadow: inset -3px -3px 5px rgba(0,0,0,0.4);
    }

    .planet:hover {
        transform:scale(1.4);
        box-shadow:0 0 20px white;
    }

    .label {
        position:absolute;
        color:white;
        font-size:12px;
        left:24px;
        top:-2px;
        white-space:nowrap;
    }

    .mercury-orbit { width:130px; height:130px; animation:spin 5s linear infinite; }
    .venus-orbit { width:200px; height:200px; animation:spin 8s linear infinite; }
    .earth-orbit { width:270px; height:270px; animation:spin 12s linear infinite; }
    .mars-orbit { width:340px; height:340px; animation:spin 16s linear infinite; }
    .jupiter-orbit { width:470px; height:470px; animation:spin 24s linear infinite; }
    .saturn-orbit { width:610px; height:610px; animation:spin 32s linear infinite; }
    .uranus-orbit { width:760px; height:760px; animation:spin 42s linear infinite; }
    .neptune-orbit { width:900px; height:900px; animation:spin 54s linear infinite; }

    .mercury { width:10px; height:10px; top:50%; left:-5px; background:radial-gradient(circle, lightgray, gray); }
    .venus { width:14px; height:14px; top:50%; left:-7px; background:radial-gradient(circle, #ffd27f, orange); }
    .earth { width:17px; height:17px; top:50%; left:-8px; background:radial-gradient(circle, #66ccff, blue); }
    .mars { width:13px; height:13px; top:50%; left:-6px; background:radial-gradient(circle, #ff9999, red); }
    .jupiter { width:30px; height:30px; top:50%; left:-15px; background:radial-gradient(circle, #d2b48c, brown); }
    .saturn { width:26px; height:26px; top:50%; left:-13px; background:radial-gradient(circle, #ffe680, gold); }
    .uranus { width:21px; height:21px; top:50%; left:-10px; background:radial-gradient(circle, #ccffff, lightblue); }
    .neptune { width:21px; height:21px; top:50%; left:-10px; background:radial-gradient(circle, #6699ff, darkblue); }

    .ring {
        position:absolute;
        width:38px;
        height:12px;
        border:2px solid rgba(255,255,255,0.45);
        border-radius:50%;
        top:7px;
        left:-6px;
        transform:rotate(20deg);
    }

    .moon-orbit {
        position:absolute;
        width:34px;
        height:34px;
        border:1px dashed rgba(255,255,255,0.18);
        border-radius:50%;
        top:-8px;
        left:-8px;
        animation:spin 2s linear infinite;
    }

    .moon {
        position:absolute;
        width:5px;
        height:5px;
        background:white;
        border-radius:50%;
        top:50%;
        left:-2px;
    }

    .moon-label {
        position:absolute;
        color:white;
        font-size:10px;
        left:8px;
        top:-8px;
    }

    .comet {
        position:absolute;
        width:12px;
        height:12px;
        background:red;
        border-radius:50%;
        box-shadow:0 0 30px red;
        animation: cometmove 4s linear infinite;
    }

    .comet-tail {
        position:absolute;
        width:90px;
        height:3px;
        background:linear-gradient(to left, red, transparent);
        top:4px;
        left:-85px;
    }

    @keyframes cometmove {
        0% { left:-100px; top:100px; }
        100% { left:1300px; top:850px; }
    }

    @keyframes spin {
        from { transform:translate(-50%,-50%) rotate(0deg); }
        to { transform:translate(-50%,-50%) rotate(360deg); }
    }
    </style>
    </head>

    <body>
    <div class="space">

    <div class="star" style="width:2px;height:2px;top:70px;left:100px;"></div>
    <div class="star" style="width:3px;height:3px;top:140px;left:400px;"></div>
    <div class="star" style="width:2px;height:2px;top:250px;left:900px;"></div>
    <div class="star" style="width:3px;height:3px;top:700px;left:250px;"></div>

    <div class="sun"></div>

    <div class="orbit mercury-orbit"><div class="planet mercury"><div class="label">Mercury</div></div></div>
    <div class="orbit venus-orbit"><div class="planet venus"><div class="label">Venus</div></div></div>

    <div class="orbit earth-orbit">
        <div class="planet earth">
            <div class="label">Earth</div>
            <div class="moon-orbit">
                <div class="moon"><div class="moon-label">Moon</div></div>
            </div>
        </div>
    </div>

    <div class="orbit mars-orbit"><div class="planet mars"><div class="label">Mars</div></div></div>
    <div class="orbit jupiter-orbit"><div class="planet jupiter"><div class="label">Jupiter</div></div></div>

    <div class="orbit saturn-orbit">
        <div class="planet saturn">
            <div class="ring"></div>
            <div class="label">Saturn</div>
        </div>
    </div>

    <div class="orbit uranus-orbit"><div class="planet uranus"><div class="label">Uranus</div></div></div>
    <div class="orbit neptune-orbit"><div class="planet neptune"><div class="label">Neptune</div></div></div>

    <div class="comet"><div class="comet-tail"></div></div>

    </div>
    </body>
    </html>
    """

    components.html(solar_html, height=980)

    planet_facts = {
        "Mercury": "Mercury is the closest planet to the Sun.",
        "Venus": "Venus is the hottest planet.",
        "Earth": "Earth supports life and has one moon.",
        "Mars": "Mars contains Olympus Mons.",
        "Jupiter": "Jupiter is the largest planet.",
        "Saturn": "Saturn has icy rings.",
        "Uranus": "Uranus rotates sideways.",
        "Neptune": "Neptune has extreme winds."
    }

    selected = st.selectbox("Choose a planet", list(planet_facts.keys()))
    st.info(planet_facts[selected])
