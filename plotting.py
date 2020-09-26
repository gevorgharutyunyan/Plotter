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



########################################################################################################
#fixme                                Synchrotron
########################################################################################################

# Power law functions

#Electron energy distribution can be power law with exponential cut off or broken power law.

def PowerLawExpCutOff(alpha, gamma_cutOff, gamma,**kwargs):

    return N0 * (gamma ** (-alpha)) * np.exp(-(gamma / gamma_cutOff))

def BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma,**kwargs):
    if gamma < gamma_break:
        return N0*gamma**(-alpha_1)
    else:
        return gamma_break**(alpha_2-alpha_1)*N0*gamma**(-alpha_2)

# Choose from two laws with booleans
def law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma,gamma_cutOff,gamma_break):
    if (cutOff_bool ==1) and (broken_bool == 0):
        return PowerLawExpCutOff(alpha, gamma_cutOff, gamma)
    elif (cutOff_bool ==0) and (broken_bool == 1):
        return  BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma)

# This function shows the energy which have many emitted photons(characteristic energy)
def char_energy(B, gamma):
    return (3 * e * h * B * (gamma ** 2)) / (2 * m * c)


# Bessel's function
def bessel_function(x):
    return (2.15 * (x) ** (1 / 3)) * (
                ((1 + 3.06 * (x)) ** (1 / 6)) * (1 + (0.884 * (x) ** (2 / 3)) + (0.471 * (x) ** (4 / 3)))) / (
                       1 + (1.64 * (x) ** (2 / 3)) + (0.974 * (x) ** (4 / 3))) * np.exp((-x))


# Quantity of emitted photons in per second with E energy(Differential spectrum dN/dE*dt)
def diff_spectrum(photon_eng, B, gamma):
    return ((np.sqrt(3) * (e ** 3) * B) / (2 * np.pi * restenergy * h * photon_eng)) * bessel_function(
       photon_eng / char_energy(B, gamma))


# spectrum for a group of electrons
def emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return \
    quad(lambda j: (10 ** j) * (math.log(10)) * diff_spectrum(photon_eng, B, 10 ** j) * law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10 ** j,gamma_cutOff,gamma_break),
         np.log10(gamma_min), np.log10(gamma_max))[0]



# Bolometric Synchrotron luminosity wich we get multiplying emission spectrum by square of photon energy(erg s^-1)
def luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return photon_eng**2*emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool)



# Energy on a per square in a per second will be luminosity divided to surface F = L/4*pi*R^2.
# Considering Lorentz transformation formulas F should be multiplied by doppler factor ^4. F = delta^4*F'
# As an energy unit are being used erg(for converting use ev to erg ratio).
def flux_our_system(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool,):
    return (doppler_factor**4)*1/(evtoerg*distance_surf)*luminosity(B, alpha,alpha_1,alpha_2,photon_eng*(1+red_shift)/doppler_factor, gamma_cutOff,gamma_break, cutOff_bool,broken_bool)


########################################################################################################
#fixme                              Synchrotron Self-Compton
########################################################################################################


#Lower limit of an integral for HE component on SED
def low_limit_ssc(photon_eng,synch_photon):
    return 0.5*synch_photon*(1+np.sqrt(1+1/(synch_photon*photon_eng)))


#####################################################################################
# fixme                        Cross-Section
#####################################################################################
"""
Cross section defines probability of an interaction between photon and electron.
Photons can be produced after synchrotron radiation(SSC), come from dusty Torus,
BLR and CMB.
"""
def bulk_gamma(gamma, photon_eng):
    return 4 * gamma * (photon_eng / restenergy)

def cross_q(gamma,photon_eng,synch_photon):
    return (synch_photon*inverse_restEng/gamma)/(4*photon_eng*inverse_restEng*gamma*(1-inverse_restEng*synch_photon/gamma))
def cross_section(gamma,photon_eng,synch_photon):
    bulk = bulk_gamma(gamma, photon_eng)
    q = (cross_q(gamma,photon_eng,synch_photon))
    return (2*q*np.log(q)+(1+2*q)*(1-q)+0.5*(1-q)*((bulk*q)**2/(1+bulk*q)))

def if_statement(gamma,photon_eng,synch_photon):
    if(cross_q(gamma,photon_eng,synch_photon) >= 1/(4*(gamma**2)) and cross_q(gamma,photon_eng,synch_photon)<=1):
        return cross_section(gamma,photon_eng,synch_photon)
    else:
        return 0

#####################################################################################
# fixme             EnergyDensity-Distribution-Luminosity-Flux
#####################################################################################
# for SSC it is taking account photons produced by synchrotron emission and
# energy density defines as blob luminosity divided to blob volume
def ssc_eng_density(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return (3*luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool))\
           /(evtoerg*4*np.pi*c*(blob_radius**2))


# for SSC mechanisms spectrum from many electrons is calculated by this formula
def ic_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return quad(lambda i:(10**i)*np.log(10)*(law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10**i,gamma_cutOff,gamma_break)/10**(2*i))*if_statement(10**i,photon_eng,synch_photon),np.log10(low_limit_ssc(photon_eng/restenergy,synch_photon/restenergy)),np.log10(gamma_max))[0]


def ssc_luminosity(synch_photon,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return  quad(lambda photon_eng: 0.75*c*sigma* (synch_photon**2)*(ssc_eng_density(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break,cutOff_bool,broken_bool)/photon_eng**3)*ic_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break),0,np.inf)[0]

# Luminosity = Flux*(4*pi*R^2)
def ssc_flux(synch_photon,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return ((doppler_factor**4)*ssc_luminosity((synch_photon*(1+red_shift))/doppler_factor,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break))/distance_surf





########################################################################################################
#fixme                                External Inverse Compton
########################################################################################################


#####################################################################################
# fixme               energy density-luminosity-flux for CMB
#####################################################################################

# Functions for electron energy distribution and cross section have been already written(see SSC.py module)
def cmb_eng_density(photon_eng):
    return (((np.pi**2)*((h*c)**3))**-1)*(photon_eng**2)*(np.exp(photon_eng/(k*cmb_temp))-1)**-1

def cmb_luminosity(synch_photon,cutOff_bool, broken_bool, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break):
    return quad(lambda photon_eng: 0.75 * c * sigma * (synch_photon ** 2) * (
                cmb_eng_density(photon_eng/doppler_factor) / photon_eng) * ic_el_dist(photon_eng, synch_photon, cutOff_bool,
                                                                             broken_bool, alpha, alpha_1, alpha_2,
                                                                             gamma_cutOff, gamma_break), 0, np.inf)[0]

def cmb_flux(synch_photon,cutOff_bool, broken_bool, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break):
    return (doppler_factor**4*evtoerg*cmb_luminosity(synch_photon/doppler_factor,cutOff_bool, broken_bool, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break))/distance_surf



#####################################################################################
# fixme           energy density-luminosity-flux for BLR
#####################################################################################
"""
BLR stands for Broad Line Region. Emission line profiles in this region are broad.It is far from central black hole but 
accretion disc emission(photons) can rich and be reflected from BLR clouds.Reflected photons interact with emission region
and produce HE component. 
"""

def luminosity_from_disc_blr(photon_eng):
    fraction = photon_eng/(k*blr_temp)
    return ((15*fraction**4)*thetta_blr*disc_luminosity)/(np.pi**4*(np.exp(fraction)-1))


def blr_eng_density(photon_eng):
    return luminosity_from_disc_blr(photon_eng)/(4*np.pi*c*(blr_radius**2))

def blr_luminosity(synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return  quad(lambda photon_eng: 0.75*c*sigma* (synch_photon**2)*(blr_eng_density(photon_eng/doppler_factor)/photon_eng**3)*ic_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break),0,np.inf)[0]



def blr_flux(synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return (doppler_factor**6*blr_luminosity((synch_photon*(1+red_shift))/doppler_factor,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break))/distance_surf



#####################################################################################
# fixme           energy density-luminosity-flux for TORUS
#####################################################################################
"""
Torus produces infrared photons and fills huge volume with them. Out of BLR are torus photons which have low energy and
after scattering energy increases up to GeV.
"""
def luminosity_from_disc_torus(photon_eng):
    fraction = photon_eng/(k*torus_temp)
    return ((15*fraction**4)*thetta_torus*disc_luminosity)/(np.pi**4*(np.exp(fraction)-1))

def torus_eng_density(photon_eng):
    return luminosity_from_disc_torus(photon_eng)/(4*np.pi*c*(torus_radius**2))


def torus_luminosity(synch_photon, cutOff_bool, broken_bool, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break):
    return quad(lambda photon_eng: 0.75 * c * sigma * (synch_photon ** 2) * (
                torus_eng_density(photon_eng / doppler_factor) / photon_eng ** 3) * ic_el_dist(photon_eng,synch_photon, cutOff_bool,
                broken_bool, alpha,alpha_1, alpha_2,gamma_cutOff, gamma_break), 0,np.inf)[0]


def torus_flux(synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return (doppler_factor**6*torus_luminosity((synch_photon*(1+red_shift))/doppler_factor,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break))/distance_surf



########################################################################################################
########################################################################################################
#fixme                              Synchrotron Plotting
########################################################################################################
########################################################################################################

def synchrotron_plotter(B, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break, cutOff_bool, broken_bool,kwargs = {"N0" : 1.5 * 10 ** (56)}):
    energy_axis = np.logspace(-9, 4, num=25)
    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array(
        [flux_our_system(B, alpha, alpha_1, alpha_2, i, gamma_cutOff, gamma_break, cutOff_bool, broken_bool) for i in
         energy_axis])
    plt.figure(1, figsize=(16, 4))
    plt.loglog(energy_axis, synchrotron_flux, color="red")
    plot = st.pyplot(plt)
    plt.xlim(10 ** -8, 10 ** 8)
    plt.ylim(10 ** -13, 10 ** -8)
    st.title('Synchrotron')
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(len(energy_axis) + 1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {4 * i}')
        bar.progress(4 * i)
        time.sleep(0.1)

    plot.pyplot(plt)



#####################################################################################
# fixme                            SSC Plotting
#####################################################################################
def ssc_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis_ssc = np.logspace(2, 9, num=25)
    # for  each point of energy_axis_ssc should be calculated flux_our_system(as an Y axis)
    self_synchrotron_flux = np.array([ssc_flux(j,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break) for j in energy_axis_ssc])
    plt.figure(1,figsize=(16,4))

    energy_axis_synch = np.logspace(-5,2, num=25)

    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gamma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis_synch])

    fig, ax1 = plt.subplots(figsize=(16, 4))
    color = 'tab:red'
    ax1.set_xlabel('E [eV]')
    ax1.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)
    ax1.plot(energy_axis_synch, synchrotron_flux, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    #Needs second y axis because low and high energy component scales do not coincide.
    color = 'tab:blue'
    ax2.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)
    ax2.plot(energy_axis_ssc, self_synchrotron_flux, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plot= st.pyplot(plt)
    st.title('Synchrotron Self-Compton')
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(len(energy_axis_ssc)+1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {4*i}')
        bar.progress(4*i)
        time.sleep(0.1)

    plot.pyplot(plt)


#####################################################################################
# fixme                           CMB   Plotting
#####################################################################################
def cmb_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis_cmb = np.logspace(2, 11, num=25)
    # for  each point of energy_axis_cmb should be calculated flux_our_system(as an Y axis)
    cosmic_background = np.array([cmb_flux(j,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break) for j in energy_axis_cmb])
    plt.figure(1,figsize=(16,4))

    energy_axis_synch = np.logspace(-5,2, num=25)

    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gamma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis_synch])

    fig, ax1 = plt.subplots(figsize=(16, 4))
    color = 'tab:red'
    ax1.set_xlabel('E [eV]')
    ax1.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)
    ax1.plot(energy_axis_synch, synchrotron_flux, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)  # we already handled the x-label with ax1
    ax2.plot(energy_axis_cmb, cosmic_background, color=color)
    plot1 = st.pyplot(plt)
    st.title('External Inverse Compton CMB')
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(len(energy_axis_cmb)+1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {4*i}')
        bar.progress(4*i)
        time.sleep(0.1)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plot1.pyplot(plt)


#####################################################################################
# fixme                           BLR   Plotting
#####################################################################################

def blr_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis_blr = np.logspace(2, 11, num=25)
    # for  each point of energy_axis_cmb should be calculated flux_our_system(as an Y axis)
    broad_line_flux = np.array([blr_flux(j,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break) for j in energy_axis_blr])
    plt.figure(1,figsize=(16,4))

    energy_axis_synch = np.logspace(-5,2, num=25)

    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gamma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis_synch])

    fig, ax1 = plt.subplots(figsize=(16, 4))
    color = 'tab:red'
    ax1.set_xlabel('E [eV]')
    ax1.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)
    ax1.plot(energy_axis_synch, synchrotron_flux, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)  # we already handled the x-label with ax1
    ax2.plot(energy_axis_blr, broad_line_flux, color=color)
    plot2 = st.pyplot(plt)
    st.title('External Inverse Compton BLR')
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(len(energy_axis_blr)+1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {4*i}')
        bar.progress(4*i)
        time.sleep(0.1)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plot2.pyplot(plt)


#####################################################################################
# fixme                           Torus   Plotting
#####################################################################################
def torus_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis_torus = np.logspace(2, 11, num=25)
    # for  each point of energy_axis_cmb should be calculated flux_our_system(as an Y axis)
    dusty_torus_flux = np.array([torus_flux(j,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break) for j in energy_axis_torus])
    plt.figure(1,figsize=(16,4))

    energy_axis_synch = np.logspace(-5,2, num=25)

    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gamma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis_synch])

    fig, ax1 = plt.subplots(figsize=(16, 4))
    color = 'tab:red'
    ax1.set_xlabel('E [eV]')
    ax1.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)
    ax1.plot(energy_axis_synch, synchrotron_flux, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color ='tab:blue'
    ax2.set_ylabel(r"$\nu F(\nu)\/ (erg\/cm^{-2} s^{-1})$", color=color)  # we already handled the x-label with ax1
    st.title('External Inverse Compton Torus')
    ax2.plot(energy_axis_torus, dusty_torus_flux, color=color)
    plot3 = st.pyplot(plt)
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(len(energy_axis_torus)+1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {4*i}')
        bar.progress(4*i)
        time.sleep(0.1)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plot3.pyplot(plt)




########################################################################################################
#fixme                               Web based plot
########################################################################################################

select_mechanism = st.selectbox('Choose from mehcanisms ', ('Select','Synchrotron', 'SSC', 'EIC'),index= 0)
if select_mechanism=="Synchrotron":
    select_power_law = st.selectbox('Choose from power laws ', ('Select', 'Exp. Cut-Off', 'Broken Law'), index=0)
    if select_power_law=='Exp. Cut-Off':
        mag_filed   = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha       = st.number_input('Cut-Off alpha',  min_value=float(0), max_value=float(5), step=0.01)
        cut_off_eng = st.number_input('Cut-Off energy', min_value=float(0), max_value=float(10**5), step=float(100))
        plot_btn = st.button("Plot")
        if plot_btn:
            synchrotron_plotter(mag_filed, alpha, None, None, cut_off_eng, None, 1, 0)
    if select_power_law == 'Broken Law':
        mag_filed = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha1 = st.number_input('Broken alpha1', min_value=float(0), max_value=float(5), step=0.01)
        alpha2 = st.number_input('Broken alpha2', min_value=float(0), max_value=float(5), step=0.01)
        broken_eng = st.number_input('Broken energy', min_value=float(0), max_value=float(100000), step=float(100))
        if st.button("Plot"):
            synchrotron_plotter(mag_filed, None, alpha1, alpha2, None, broken_eng, 0, 1)
elif select_mechanism=='SSC':
    select_power_law = st.selectbox('Choose from power laws ', ('Select', 'Exp. Cut-Off', 'Broken Law'), index=0)
    if select_power_law=='Exp. Cut-Off':
        mag_filed   = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha       = st.number_input('Cut-Off alpha',  min_value=float(0), max_value=float(5), step=0.01)
        cut_off_eng = st.number_input('Cut-Off energy', min_value=float(0), max_value=float(10**5), step=float(100))
        plot_btn = st.button("Plot")
        if plot_btn:
            ssc_plotter(mag_filed, alpha, None, None, cut_off_eng, None, 1, 0)
    if select_power_law == 'Broken Law':
        mag_filed = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha1 = st.number_input('Broken alpha1', min_value=float(0), max_value=float(5), step=0.01)
        alpha2 = st.number_input('Broken alpha2', min_value=float(0), max_value=float(5), step=0.01)
        broken_eng = st.number_input('Broken energy', min_value=float(0), max_value=float(100000), step=float(100))
        plot_btn = st.button("Plot")
        if plot_btn:
            ssc_plotter(mag_filed, None, alpha1, alpha2, None, broken_eng, 0, 1)
elif select_mechanism == 'EIC':
    select_power_law = st.selectbox('Choose from power laws ', ('Select', 'Exp. Cut-Off', 'Broken Law'), index=0)
    if select_power_law=='Exp. Cut-Off':
        mag_filed   = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha       = st.number_input('Cut-Off alpha',  min_value=float(0), max_value=float(5), step=0.01)
        cut_off_eng = st.number_input('Cut-Off energy', min_value=float(0), max_value=float(10**5), step=float(100))
        select_photon_filed = st.selectbox('Choose from photon fileds ', ('Select', 'CMB', 'BLR','Torus'), index=0)
        if select_photon_filed=='CMB':
            plot_btn = st.button("Plot")
            if plot_btn:
                cmb_plotter(mag_filed, alpha, None, None, cut_off_eng, None, 1, 0)
        elif select_photon_filed=='BLR':
            plot_btn = st.button("Plot")
            if plot_btn:
                blr_plotter(mag_filed, alpha, None, None, cut_off_eng, None, 1, 0)
        elif select_photon_filed=='Torus':
            plot_btn = st.button("Plot")
            if plot_btn:
                torus_plotter(mag_filed, alpha, None, None, cut_off_eng, None, 1, 0)
    elif select_power_law=='Broken Law':
        mag_filed = st.number_input('Magnetic Filed', min_value=float(0), max_value=float(5), step=0.01)
        alpha1 = st.number_input('Broken alpha1', min_value=float(0), max_value=float(5), step=0.01)
        alpha2 = st.number_input('Broken alpha2', min_value=float(0), max_value=float(5), step=0.01)
        broken_eng = st.number_input('Broken energy', min_value=float(0), max_value=float(100000), step=float(100))
        select_photon_filed = st.selectbox('Choose from photon fileds ', ('Select', 'CMB', 'BLR', 'Torus'), index=0)
        if select_photon_filed == 'CMB':
            plot_btn = st.button("Plot")
            if plot_btn:
                cmb_plotter(mag_filed, None, alpha1, alpha2, None, broken_eng, 0, 1)
        elif select_photon_filed == 'BLR':
            plot_btn = st.button("Plot")
            if plot_btn:
                blr_plotter(mag_filed, None, alpha1, alpha2, None, broken_eng, 0, 1)
        elif select_photon_filed == 'Torus':
            plot_btn = st.button("Plot")
            if plot_btn:
                torus_plotter(mag_filed, None, alpha1, alpha2, None, broken_eng, 0, 1)

