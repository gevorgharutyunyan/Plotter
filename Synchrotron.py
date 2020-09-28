from Constants import*

# Power law functions

#Electron energy distribution can be power law with exponential cut off or broken power law.

def PowerLawExpCutOff(alpha, gamma_cutOff, gamma,**kwargs):

    return kwargs["N0"] * (gamma ** (-alpha)) * np.exp(-(gamma / gamma_cutOff))

def BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma,**kwargs):
    if gamma < gamma_break:
        return N0*gamma**(-alpha_1)
    else:
        return gamma_break**(alpha_2-alpha_1)*kwargs["N0"]*gamma**(-alpha_2)

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



