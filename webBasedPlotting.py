from tkinter import ttk
import numpy as np
from Synchrotron import *
from SSC import *
from EIC import *



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

selected = st.text_input("", "Search...")


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



# color = st.beta_color_picker('Pick A Color', '#00f900')
# st.write('The current color is', color)

