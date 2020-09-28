from scipy.integrate import quad,trapz
import matplotlib.pyplot as plt
import numpy as np
import math
import  streamlit as st
import time
import streamlit.components.v1 as components


electron_num       = st.sidebar.number_input("Number of electrons", value=float(1.5 * 10 ** (56)),step=float(1))
dopplerFactor      = st.sidebar.number_input("Doppler factor", value=float(20), step=0.1)
distance_of_source = st.sidebar.number_input("Distance from a source", value=float(1.7896929972 * 10 ** (28)))
redShift           = st.sidebar.number_input("Red shift", value=float(0.9))
gammaMin           = st.sidebar.number_input("Minimum energy of an electron", value=float(1))
gammaMax           = st.sidebar.number_input("Maximum energy of an electron", value=float(2.4*10**4))
thettaBLR          = st.sidebar.number_input("Reflection coefficient for broad line region", value=float(0.6))
thettaTorus        = st.sidebar.number_input("Reflection coefficient for Torus", value=float(0.6))
discLuminosity     = st.sidebar.number_input("Luminosity of the accretion disc", value=float(1.4*10**43))
blrTemp            = st.sidebar.number_input("Temperature of BLR", value=float(116045))
blrRadius          = st.sidebar.number_input("Radius of BLR", value=float(10**17*(discLuminosity/10**45)**0.5))
torusTemp          = st.sidebar.number_input("Temperature of Torus", value=float(1000))
blobRadius         = st.sidebar.number_input("Radus of an emission region", value= float(1.6*10**17))
torusRadius        = st.sidebar.number_input("Radius of Torus", value=float(0.4*((discLuminosity/10**45)**0.5)*((1500/torusTemp)**2.6)*(3.086*10**18)))

x = st.slider('Select a value',float(10 ** -8),float(10 ** 8),float(10**3))
print(x[0])
# Constants
e = 4.8032 * 10 ** (-10)  # Electron charge
h = 6.5821 * 10 ** (-16)  # Plank's constant with line in Ev
hev = 4.135667662 * 10 ** -15  # Plank's constant  in Ev
m = 9.1095 * 10 ** (-28)  # Mass of an electron
c = 2.9979 * 10 ** (10)  # Speed of light
sigma = 6.6524 * 10 ** (-25)  # Cross-section
restenergy = 0.511 * 10 ** (6)  # E = mc^2
k = 8.6173303 * 10 ** (-5)  # Boltzman's constant
ergtoev = 6.24 * 10 ** (11)  # eV
evtoerg = 0.16 * 10 ** (-11)  # erg
parsec = 3.086*10**18 # One parsec is a 3.086*10**18 cm
inverse_restEng = 1/restenergy # for simplicity
N0 = electron_num  # number of electrons
doppler_factor = dopplerFactor  # Bulk gamma is equal to doppler factor
source_distance = distance_of_source
distance_surf = 4 * math.pi * math.pow(source_distance, 2)  # Luminosity should be divided to suface
gamma_min = gammaMin  # minimum energy of radiated photon
gamma_max = gammaMax  # maximum energy of a radiated photon
red_shift = redShift
cmb_temp = 2.72 # cosmic microwave background temperature
thetta_blr   = thettaBLR # reflection coefficient for broad line region
thetta_torus = thettaTorus # reflection coefficient for Torus
disc_luminosity = discLuminosity # Luminosity produced by accretion disc
blr_temp = blrTemp# temperature of broad line region
blr_radius = blrRadius
torus_temp = torusTemp# temperature of torus
blob_radius = blobRadius # radius of emission region
torus_radius = torusRadius


