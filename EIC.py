from Synchrotron import*
from SSC import *
from Constants import*


def cmb_eng_density(photon_eng):
    cmb_temp = 2.72
    return (((np.pi**2)*((h*c)**3))**-1)*(photon_eng**2)*(np.exp(photon_eng/(k*cmb_temp))-1)**-1

def cmb_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return quad(lambda i:(10**i)*np.log(10)*(law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10**i,gamma_cutOff,gamma_break)/10**(2*i))*if_statement(10**i,photon_eng,synch_photon),np.log10(low_limit_ssc(photon_eng/restenergy,synch_photon/restenergy)),np.log10(gamma_max))[0]