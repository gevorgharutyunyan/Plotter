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
