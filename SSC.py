from Synchrotron import*

#####################################################################################
# fixme                        Cross-Section
#####################################################################################

def CS_bulk_gamma (gamma,photon_eng):
    return 4 *(photon_eng/restenergy)*gamma


def CS_q (gamma,photon_eng,synch_photon_eng):
    return (synch_photon_eng/restenergy*gamma)/(4*gamma*(photon_eng/restenergy)*(1-(synch_photon_eng/(gamma*restenergy))))

def cross_section(gamma,photon_eng,synch_photon_eng):
    return 2*CS_q(gamma,photon_eng,synch_photon_eng)*math.log(CS_q(gamma,photon_eng,synch_photon_eng))+(1+2*CS_q(gamma,photon_eng,synch_photon_eng))*(1-CS_q(gamma,photon_eng,synch_photon_eng))+(0.5*(1-CS_q(gamma,photon_eng,synch_photon_eng))
           *((CS_q(gamma,photon_eng,synch_photon_eng)*CS_bulk_gamma(gamma,photon_eng)**2))/(1+(CS_bulk_gamma(gamma,photon_eng)*(CS_q(gamma,photon_eng,synch_photon_eng)))))



def if_statment(gamma,photon_eng,synch_photon_eng):
    if CS_q (gamma,photon_eng,synch_photon_eng) >= 1/(4*(gamma**2)) and CS_q (gamma,photon_eng,synch_photon_eng)<=1:
        return cross_section(gamma,photon_eng,synch_photon_eng)
    else:
        return 0


def SSC_eng_densiy(B,alpha,alpha_1,alpha_2,photon_eng,gumma_cutOff,gamma_break,cutOff_bool,broken_bool):
    return 3*(luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gumma_cutOff,gamma_break, cutOff_bool,broken_bool)/(evtoerg*4*np.pi*c*(blob_radius**2)))


def SSC_low_limit(synch_photon_eng,photon_eng):
    return 0.5*synch_photon_eng*(1+np.sqrt(1+(1/synch_photon_eng*photon_eng)))


def SSC_electron_dist(synch_photon_eng,photon_eng,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gumma_cutOff,gamma_break):
    return quad(lambda k:(10**k)*(np.log(10))*if_statment(10**k,photon_eng,synch_photon_eng)
           *(law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10**k,gumma_cutOff,gamma_break)/10**(2*k))/10**(2*k),np.log10(SSC_low_limit(synch_photon_eng/restenergy,photon_eng/restenergy)),np.log10(gamma_max))[0]





def SSC_lumnosity(synch_photon_eng,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gumma_cutOff,gamma_break):
    return quad(lambda photon_eng:0.75*c*sigma*(synch_photon_eng**2)*(SSC_eng_densiy(B,alpha,alpha_1,alpha_2,photon_eng,gumma_cutOff,gamma_break,cutOff_bool,broken_bool)/(distance_surf*(photon_eng**3)))
           *SSC_electron_dist(synch_photon_eng,photon_eng,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gumma_cutOff,gamma_break),0,np.Infinity)[0]


def SSC_flux(synch_photon_eng,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gumma_cutOff,gamma_break):
    return (doppler_factor**4)*SSC_lumnosity((synch_photon_eng*(1+red_shift))/doppler_factor,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gumma_cutOff,gamma_break)


energy_axis = np.logspace(0, 9, num=100)
# for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
self_synchrotron_flux = np.array([SSC_flux(m,0.07,0,1,None,2.4,3.9,None,2200) for m in energy_axis])
plt.figure(1,figsize=(16,4))
plt.loglog(energy_axis,self_synchrotron_flux,color="red")
plt.xlim(10**-16,10**12                                                                                                                                                                                                                                                                 )
plt.ylim(10**-18,10**-11)
plt.show()


