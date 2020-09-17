from Constants import*

# Power law functions
def PowerLawExpCutOff(alpha, gamma_cutOff, gamma):

    return N0 * (gamma ** (-alpha)) * np.exp(-(gamma / gamma_cutOff))


def BrokenPowerLaw(alpha_1,alpha_2,gamma_break,gamma):
    if gamma < gamma_break:
        return N0*gamma**(-alpha_1)
    else:
        return gamma_break**(alpha_2-alpha_1)*N0*gamma**(-alpha_2)


def law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma,gamma_cutOff,gamma_break):
    if (cutOff_bool ==1) and (broken_bool == 0):
        return PowerLawExpCutOff(alpha, gamma_cutOff, gamma)
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



def emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return \
    quad(lambda j: (10 ** j) * (math.log(10)) * diff_spectrum(photon_eng, B, 10 ** j) * law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10 ** j,gamma_cutOff,gamma_break),
         np.log10(gamma_min), np.log10(gamma_max))[0]




def luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return photon_eng**2*emission_spectrum(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool)




def flux_our_system(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return (doppler_factor**4)*1/(evtoerg*distance_surf)*luminosity(B, alpha,alpha_1,alpha_2,photon_eng*(1+red_shift)/doppler_factor, gamma_cutOff,gamma_break, cutOff_bool,broken_bool)


def synchrotron_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis = np.logspace(-9, 4, num=25)
    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array([flux_our_system(B, alpha,alpha_1,alpha_2, i, gamma_cutOff,gamma_break, cutOff_bool,broken_bool) for i in energy_axis])
    plt.figure(1,figsize=(16,4))
    plt.loglog(energy_axis,synchrotron_flux,color="red")
    plt.xlim(10**-8,10**8)
    plt.ylim(10**-13,10**-8)
    plt.show()
    return  synchrotron_flux

