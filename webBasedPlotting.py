from EIC import *
from Constants import *


########################################################################################################
########################################################################################################
#fixme                                Plotting Synchrotron
########################################################################################################
########################################################################################################

def synchrotron_plotter(B, alpha, alpha_1, alpha_2, gamma_cutOff, gamma_break, cutOff_bool, broken_bool,kwargs = {"N0" : 1.5 * 10 ** (56)}):
    energy_axis = np.logspace(-9, 4, num=25)
    # for  each point of energy_axis should be calculated flux_our_system(as a Y axis)
    synchrotron_flux = np.array(
        [flux_our_system(B, alpha, alpha_1, alpha_2, i, gamma_cutOff, gamma_break, cutOff_bool, broken_bool) for i in
         energy_axis])
    plt.figure(1, figsize=(16, 4))
    plt.loglog(energy_axis, synchrotron_flux, color=v)
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
# fixme                              Plotting SSC
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

