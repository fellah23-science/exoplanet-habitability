import streamlit as st
import math
import pandas as pd
import numpy as np
import random
import base64

st.set_page_config(page_title="ExoGalaxy Explorer", layout="wide")

# ------------------- Solar System Background -------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #000000, #0b0c1a, #1a0033, #000022);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------- Tabs -------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🪐 Habitability Calculator", 
    "📊 Exoplanet Data", 
    "💫 Learn & Discover", 
    "📝 Assessment Zone", 
    "🤖 Space Encyclopedia AI",
    "🌌 Solar System Simulation"
])

# ------------------- TAB 1: Habitability Calculator -------------------
with tab1:
    st.header("🪐 Habitability Calculator")
    st.write("Input parameters to calculate habitability...")
    # ---- Put your habitability calculator code here ----
    st.info("Habitability calculator goes here...")

# ------------------- TAB 2: Exoplanet Data -------------------
with tab2:
    st.header("📊 Exoplanet Data")
    # ---- Put your planet data table code here ----
    st.info("Exoplanet data table goes here...")

# ------------------- TAB 3: Learn & Discover -------------------
with tab3:
    st.header("💫 Learn & Discover")
    # ---- Put your random space facts code here ----
    if st.button("🌟 Show a Space Fact"):
        facts = [
            "🌠 The first exoplanet was discovered in 1992.",
            "🌍 Over 5,000 exoplanets discovered!",
            "💧 Habitable zone is where liquid water can exist."
        ]
        st.info(random.choice(facts))

# ------------------- TAB 4: Assessment Zone -------------------
with tab4:
    st.header("📝 Assessment Zone")

    # Quiz questions (MCQ)
    quiz1 = [
        {"question":"Which planet is known as the Red Planet?", "options":["Earth","Mars","Venus","Jupiter"], "answer":"Mars"},
        {"question":"What is the largest planet?", "options":["Jupiter","Saturn","Neptune","Mars"], "answer":"Jupiter"},
        {"question":"Black holes are formed from?", "options":["Stars","Planets","Comets","Asteroids"], "answer":"Stars"},
        {"question":"What is the habitable zone?", "options":["Ice zone","Liquid water zone","Gas zone","Dark zone"], "answer":"Liquid water zone"},
        {"question":"Nearest star to Earth?", "options":["Sirius","Proxima Centauri","Sun","Alpha Centauri"], "answer":"Proxima Centauri"}
    ]

    st.subheader("🚀 Space Geek Quiz")
    user_answers = []
    wrong = []
    score = 0
    for i,q in enumerate(quiz1):
        ans = st.radio(f"{i+1}. {q['question']}", q['options'], key=f"q1_{i}")
        user_answers.append(ans)
        if ans == q['answer']:
            score += 1
        else:
            wrong.append(f"{q['question']} -> Correct: {q['answer']}")

    if st.button("Submit Space Geek Quiz"):
        st.markdown(f"**You scored {score}/5**")
        if score > 2:
            st.success("You're a true Space Geek! 🌌")
        else:
            st.info("Keep learning, Astronomer in training! 🌠")
        if wrong:
            st.warning("Questions you got wrong:")
            for w in wrong:
                st.write(w)

# ------------------- TAB 5: Space Encyclopedia AI -------------------
with tab5:
    st.header("🤖 Space Encyclopedia AI")
    space_facts = {
        "black hole": "A black hole is a region of space where gravity is so strong that nothing can escape.",
        "supernova": "A supernova is a powerful explosion of a dying star.",
        "nebula": "A nebula is a cloud of gas and dust where stars are born.",
        "exoplanet": "Exoplanets orbit stars outside our Solar System.",
        "galaxy": "A galaxy is a system of stars, gas, and dark matter.",
        "star": "A star shines due to nuclear fusion in its core.",
        "solar system": "Our Solar System has the Sun, planets, moons, and asteroids."
    }

    question = st.text_input("Ask a space question:")
    if st.button("Get Answer"):
        found = False
        for key,val in space_facts.items():
            if key in question.lower():
                st.info(val)
                found = True
                break
        if not found:
            st.warning("Sorry! I don't know the answer yet. Try another question!")

# ------------------- TAB 6: Solar System Simulation -------------------
with tab6:
    st.header("🌌 Solar System Simulation")

    # ----- Solar System HTML/CSS -----
    solar_html = """
    <style>
    .solar-container {
        position: relative;
        width: 700px;
        height: 700px;
        margin: auto;
        margin-top: 30px;
    }
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
    .orbit {
        position: absolute;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 50%;
        animation: spin linear infinite;
    }
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
    </style>

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
    
   
           



   
      
       
       
        
      
       
       
    
   

   
  

    
 








