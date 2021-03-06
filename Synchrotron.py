from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np
import math

# Constants
e  =  4.8032*10**(-10)        # Electron charge
h  =  6.5821* 10**(-16)       # Plank's constant with line in Ev
hev  =  4.135667662*10**-15   # Plank's constant  in Ev
m  = 9.1095 *10**(-28)        # Mass of an electron
c  = 2.9979 *10**(10)         # Speed of light
sigma  =  6.6524*10**(-25)    # Cross-section
restenergy  =  0.511*10**(6)  # E = mc^2
k  =  8.6173303 *10**(-5)     # Boltzman's constant
ergtoev  =  6.24*10**(11)     # eV
evtoerg  =  0.16 * 10**(-11)  # erg
N0 =  1.48453*10**(51)        # number of electrons
#gamma_cutOff = 2*10**(3)     # Cutoff energy
doppler_factor  = 18          # Bulk gamman is equal to doppler factor
source_distance = 1.88274*10**(28)
distance_surf   =  4*math.pi*math.pow(source_distance,2) # Luminosity should be divided to suface
gamma_min = 69   # minimum energy of radiated photon
gamma_max = 4*10**6 # maximum energy of radiated photon

# Power law with exponential cutoff
def PowerLawExpCutOff(alpha, gamma_cutOff, gamma):
    return N0 * (gamma ** (-alpha)) * np.exp(-(gamma / gamma_cutOff))


# This function shows the energy which have many emitted photons(characteristic energy  )
def char_energy(B, gamma):
    return (3 * e * h * B * (gamma ** 2)) / (2 * m * c)


# Bessel's function
def bessel_function(x):
    return (2.15 * (x) ** (1 / 3)) * (
                ((1 + 3.06 * (x)) ** (1 / 6)) * (1 + (0.884 * (x) ** (2 / 3)) + (0.471 * (x) ** (4 / 3)))) / (
                       1 + (1.64 * (x) ** (2 / 3)) + (0.974 * (x) ** (4 / 3))) * np.exp((-x))


# Quantity of emitted photons in per second with E energy(Differential sepctrum dN/dE*dt)
def diff_spectrum(photon_eng, B, gamma):
    return ((np.sqrt(3) * (e ** 3) * B) / (2 * np.pi * restenergy * h * photon_eng)) * bessel_function(
       photon_eng / char_energy(B, gamma))



def emission_spectrum(B, alpha, E, gamma_cutOff):
    return \
    quad(lambda j: (10 ** j) * (math.log(10)) * diff_spectrum(E, B, 10 ** j) * PowerLawExpCutOff(alpha, gamma_cutOff, 10 ** j),
         np.log10(gamma_min), np.log10(gamma_max))[0]



def luminosity(B, alpha, E, gamma_cutOff):
    return E**2*emission_spectrum(B, alpha, E, gamma_cutOff)

def flux_our_system(B, alpha, E, gamma_cutOff):
    return (doppler_factor**4)*1/(evtoerg*distance_surf)*luminosity(B, alpha, E/doppler_factor, gamma_cutOff)

# x axis


#for  each point of energy_axis should be calcilated flux_our_system(as a Y axis)


def synchrotron_plotter(B, alpha, CutOff_eng):
    energy_axis = np.logspace(-5, 9, num=100)
    synchrotron_flux = np.array([flux_our_system(B, alpha, i, CutOff_eng) for i in energy_axis])
    plt.figure(1,figsize=(16,4))
    plt.loglog(energy_axis,synchrotron_flux,color="red")
    plt.xlim(10**-1,10**8)
    plt.ylim(10**-14,10**-11)
    plt.show()
