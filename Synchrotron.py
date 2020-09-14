from scipy.integrate import quad,odeint
import matplotlib.pyplot as plt
import numpy as np
import math


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
doppler_factor = 20  # Bulk gamman is equal to doppler factor
source_distance = 1.7896929972 * 10 ** (28)
distance_surf = 4 * math.pi * math.pow(source_distance, 2)  # Luminosity should be divided to suface
gamma_min = 1  # minimum energy of radiated photon
gamma_max = 2.4*10**4  # maximum energy of radiated photon
red_shift = 0.9
blob_radius = 1.6*10**17 # radius of emission region
# Power law functions
def PowerLawExpCutOff(alpha, gumma_cutOff, gamma):

    return N0 * (gamma ** (-alpha)) * np.exp(-(gamma / gumma_cutOff))


def BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma):
    if gamma < gamma_break:
        return N0*gamma**(-alpha_1)
    else:
        return gamma_break**(alpha_2-alpha_1)*N0*gamma**(-alpha_2)


def law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma,gumma_cutOff,gamma_break):
    if (cutOff_bool ==1) and (broken_bool == 0):
        return PowerLawExpCutOff(alpha, gumma_cutOff, gamma)
    elif (cutOff_bool ==0) and (broken_bool == 1):
        return  BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma)

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



def emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gumma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return \
    quad(lambda j: (10 ** j) * (math.log(10)) * diff_spectrum(photon_eng, B, 10 ** j) * law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10 ** j,gumma_cutOff,gamma_break),
         np.log10(gamma_min), np.log10(gamma_max))[0]




def luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gumma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return photon_eng**2*emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gumma_cutOff,gamma_break, cutOff_bool,broken_bool)




def flux_our_system(B, alpha,alpha_1,alpha_2,photon_eng, gumma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return (doppler_factor**4)*1/(evtoerg*distance_surf)*luminosity(B, alpha,alpha_1,alpha_2,photon_eng*(1+red_shift)/doppler_factor, gumma_cutOff,gamma_break, cutOff_bool,broken_bool)


def synchrotron_plotter(B, alpha,alpha_1,alpha_2, gumma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis = np.logspace(-5, 9, num=100)
    # for  each point of energy_axis should be calcilated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gumma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis])
    plt.figure(1,figsize=(16,4))
    plt.loglog(energy_axis,synchrotron_flux,color="red")
    plt.xlim(10**-8,10**8)
    plt.ylim(10**-17,10**-11)
    plt.show()



