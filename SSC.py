from Synchrotron import*

#####################################################################################
# fixme                        Cross-Section
#####################################################################################

def low_limit_ssc(photon_eng,synch_photon):
    return 0.5*synch_photon*(1+np.sqrt(1+1/(synch_photon*photon_eng)))

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

# for SSC is taking account photons produced by synchrotron emission and
# energy density defines as blob luminosity divided to blob volume
def ssc_eng_density(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    return (3*luminosity(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break, cutOff_bool,broken_bool))\
           /(evtoerg*4*np.pi*c*(blob_radius**2))


# for SSC mechanisms spectrum from many electrons is calculated by this formula
def ssc_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return quad(lambda i:(10**i)*np.log(10)*(law_selection(cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,10**i,gamma_cutOff,gamma_break)/10**(2*i))*if_statement(10**i,photon_eng,synch_photon),np.log10(low_limit_ssc(photon_eng/restenergy,synch_photon/restenergy)),np.log10(gamma_max))[0]



def ssc_luminosity(synch_photon,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return  quad(lambda photon_eng: 0.75*c*sigma* (synch_photon**2)*(ssc_eng_density(B, alpha,alpha_1,alpha_2,photon_eng, gamma_cutOff,gamma_break,cutOff_bool,broken_bool)/photon_eng**3)*ssc_el_dist(photon_eng,synch_photon,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break),0,np.inf)[0]



def ssc_flux(synch_photon,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break):
    return ((doppler_factor**4)*ssc_luminosity((synch_photon*(1+red_shift))/doppler_factor,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break))/distance_surf

def ssc_plotter(B, alpha,alpha_1,alpha_2, gamma_cutOff,gamma_break, cutOff_bool,broken_bool):
    energy_axis_ssc = np.logspace(-1, 9, num=100)
    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    self_synchrotron_flux = np.array([ssc_flux(j,B,cutOff_bool,broken_bool,alpha,alpha_1,alpha_2,gamma_cutOff,gamma_break) for j in energy_axis_ssc])
    plt.figure(1,figsize=(16,4))
    plt.loglog(energy_axis_ssc,self_synchrotron_flux,color="red")

    plt.show()





ssc_plotter(0.07, None,2.4,3.9, None,2200, 0,1)




