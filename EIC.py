from Synchrotron import*
from SSC import *
from Constants import*

"""
Beside SSC there are three main mechanisms which responsible for HE component.Electrons of emission region can interact 
with CMB , BLR and IR Torus photon fields.For all cases principle are the same,changeable only energy density and 
particular parameters which depend on photon filed.It means we can use all functions from SSC module. For more details
see Ghizelini(Radiative processes),Dermer(article),Nenkova(article).
"""


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
    #plt.show()


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
    #plt.show()




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

    color = 'tab:blue'
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
    #plt.show()
