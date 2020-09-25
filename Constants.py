from scipy.integrate import quad,trapz
import matplotlib.pyplot as plt
import numpy as np
import math
import  streamlit as st
import time

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
N0 = 1.5 * 10 ** (56)  # number of electrons
doppler_factor = 20  # Bulk gamma is equal to doppler factor
source_distance = 1.7896929972 * 10 ** (28)
distance_surf = 4 * math.pi * math.pow(source_distance, 2)  # Luminosity should be divided to suface
gamma_min = 1  # minimum energy of radiated photon
gamma_max = 2.4*10**4  # maximum energy of a radiated photon
red_shift = 0.9
parsec = 3.086*10**18 # One parsec is a 3.086*10**18 cm
blob_radius = 1.6*10**17 # radius of emission region
inverse_restEng = 1/restenergy # for simplicity
cmb_temp = 2.72 # cosmic microwave background temperature
thetta_blr   = 0.6 # reflection coefficient for broad line region
thetta_torus = 0.6 # reflection coefficient for Torus
disc_luminosity = 1.4*10**43 # Luminosity produced by accretion disc
blr_temp = 116045 # temperature of broad line region
blr_radius = 10**17*(disc_luminosity/10**45)**0.5
torus_temp = 1000 # temperature of torus

torus_radius = 0.4*((disc_luminosity/10**45)**0.5)*((1500/torus_temp)**2.6)*parsec