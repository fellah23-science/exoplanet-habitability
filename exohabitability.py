import streamlit as st
import math

# Constants
G = 6.67430e-11       # Gravitational constant (m^3 kg^-1 s^-2)
sigma = 5.670374419e-8 # Stefan-Boltzmann constant (W/m^2 K^4)
M_sun = 1.989e30       # Mass of Sun (kg)
L_sun = 3.828e26       # Luminosity of Sun (W)

st.title("🌌 ExoHabit: Exoplanet Habitability Calculator")

st.header("Star Properties")
M_star = st.number_input("Star Mass (in Solar Masses)", value=1.0)
L_star = st.number_input("Star Luminosity (in Solar Luminosities)", value=1.0)

st.header("Planet / Orbit Properties")
K = st.number_input("Radial Velocity Amplitude (m/s)", value=10.0)
P_days = st.number_input("Orbital Period (days)", value=365.0)
e = st.number_input("Orbital Eccentricity (0 = circle)", value=0.0, min_value=0.0, max_value=0.99)
i_deg = st.number_input("Inclination (degrees, default 90)", value=90.0)
A = st.number_input("Albedo (reflectivity, default 0.3)", value=0.3)

# Calculations
P = P_days * 24 * 3600
i = math.radians(i_deg)
M_star_kg = M_star * M_sun
L_star_W = L_star * L_sun

M_p = (K * math.sqrt(1 - e**2) * (M_star_kg)**(2/3) * (P/(2*math.pi*G))**(1/3)) / math.sin(i)
a = ((G * M_star_kg * P**2) / (4 * math.pi**2))**(1/3)
F = L_star_W / (4 * math.pi * a**2)
T_eq = ((F * (1-A)) / (4*sigma))**0.25

HZ_inner = 0.95 * 1.496e11
HZ_outer = 1.67 * 1.496e11
if HZ_inner <= a <= HZ_outer:
    habitability = "✅ Likely Habitable"
else:
    habitability = "❌ Not in Habitable Zone"

st.header("Results")
st.write(f"**Planet Mass:** {M_p/5.972e24:.2f} Earth masses")
st.write(f"**Orbital Radius:** {a/1.496e11:.2f} AU")
st.write(f"**Equilibrium Temperature:** {T_eq:.1f} K")
st.write(f"**Habitability:** {habitability}")
