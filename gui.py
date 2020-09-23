from tkinter import *
import numpy as np
from Synchrotron import *
from SSC import *
from EIC import *


class Plotter_GUI:
    """
    Plotter_GUI class
    """

    def __init__(self, master):
        """
        There are 3 main radiation mechanisms in jets- Synchrotron radiation, Synchrotron Self-Compton and Inverse Compton.
        For each one there is a checkbutton
        :param master:
        """

        self.master = master
        master.title("Plotter")
        master.geometry('{}x{}'.format(master.winfo_screenwidth(), master.winfo_screenmmheight()))

        self.synch_bool = IntVar()
        self.ssc_bool = IntVar()
        self.ic_bool = IntVar()
        self.synchrotron_btn = Checkbutton(master, text="Synchrotron", height=10, width=10,state="normal", variable=self.synch_bool,
                                           onvalue=1, offvalue=0, command= self.param_winwow).place(relx=0.1, rely=0.3,
                                                                                                   anchor='e')
        self.self_synchrotron_btn = Checkbutton(master, text="SSC", height=10, width=10,state="normal", variable=self.ssc_bool,
                                                onvalue=1, offvalue=0, command=self.param_winwow).place(relx=0.5,
                                                                                                        rely=0.3,
                                                                                                        anchor='e')
        self.inverse_compton_btn = Checkbutton(master, text="IC", height=10, width=10,state="normal", variable=self.ic_bool, onvalue=1,
                                               offvalue=0, command= self.param_winwow).place(relx=0.9, rely=0.3,
                                                                                            anchor='e')

        """     
        def disable_synchrotron_and_ssc(self):
            self.synchrotron_btn.config(state=DISABLED)
            self.self_synchrotron_btn.config(state=DISABLED)

        def disable_ssc_and_eic(self):
            self.self_synchrotron_btn.config(state=DISABLED)
            self.inverse_compton_btn.config(state=DISABLED)
    
        def disable_eic_and_synchrotron(self):
            self.synchrotron_btn.config(state=DISABLED)
            self.inverse_compton_btn.config(state=DISABLED)
        """

    # Only can choose one spectrum law by choosing one of this law second one will be disabled.
    def disable_broken(self):
        self.Broken_PL.config(state=DISABLED)

    def disable_cutOff(self):
        self.CutOff_PL.config(state=DISABLED)

    def param_winwow(self):
        """
        This function is responsible for selecting from two power laws cutOff and broken.
        Calling this function in the window will apear two checkboxes with CutOff_PL and Broken_PL names.
        After clicking one of them open_cutoff_param(open_broken_param) function will be called and
        opened labels should be filled otherwise code won't work.
        """
        self.window = Toplevel()
        self.window.title("SED parameters")
        self.CutOff_Law = IntVar()
        self.Broken_Law = IntVar()
        self.CutOff_PL = Checkbutton(self.window, text='CutOff_PL', state="normal", variable=self.CutOff_Law, onvalue=1,
                                     offvalue=0, command=lambda: [self.open_cutoff_param(), self.disable_broken()])
        self.CutOff_PL.grid(row=5, column=0)
        self.Broken_PL = Checkbutton(self.window, text='Broken_PL', state="normal", variable=self.Broken_Law, onvalue=1,
                                     offvalue=0, command=lambda: [self.open_broken_param(), self.disable_cutOff()])
        self.Broken_PL.grid(row=5, column=1)
        if self.ic_bool.get() == 1:
            self.cmb = Checkbutton(self.window, text='cmb', state="normal",
                                         onvalue=1,
                                         offvalue=0)
            self.cmb.grid(row=6, column=0)
            self.blr = Checkbutton(self.window, text='blr', state="normal",
                                         onvalue=1,
                                         offvalue=0)
            self.blr.grid(row=7, column=0)
            self.torus = Checkbutton(self.window, text='torus', state="normal",
                                         onvalue=1,
                                         offvalue=0)
            self.torus.grid(row=8, column=0)


    def open_cutoff_param(self):
        """
         For cutOff law there are three basic parameters.
         magnetic field(B)
         photon index (alpha)
         cutOff energy (gamma_cutOff)
         This  function will make labels for parameters listed above.
        """
        # fixme magnetic field
        label_magField = Label(self.window, text='Magnetic field :', relief=RIDGE, width=20)
        label_magField.grid(row=0, column=0)
        self.entry_magField = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_magField.grid(row=0, column=1)

        # fixme  alpha
        label_alpha = Label(self.window, text='alpha :', relief=RIDGE, width=20)
        label_alpha.grid(row=1, column=0)
        self.entry_alpha = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_alpha.grid(row=1, column=1)

        # fixme gamma_cutOff
        label_cutOff = Label(self.window, text='Cut_OFF energy :', relief=RIDGE, width=20)
        label_cutOff.grid(row=2, column=0)
        self.entry_cutOff = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_cutOff.grid(row=2, column=1)
        if self.synch_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.synchrotron_plotFunc)
            plt_btn.grid(row=20, column=20)
        elif self.ssc_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.ssc_plotFunc)
            plt_btn.grid(row=20, column=20)
        elif self.ic_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.eic_plotFunc)
            plt_btn.grid(row=20, column=20)

    def open_broken_param(self):
        """
        In the broken law case need four parameters
        magnetic field(B)
        broken index1 (alpha1)
        broken index2 (alpha2)
        broken energy (gamma_broken)
        This  function will make labels for  parameters listed above.
        """
        # fixme   magnetic field
        label_magField = Label(self.window, text='Magnetic field :', relief=RIDGE, width=20)
        label_magField.grid(row=0, column=2)
        self.entry_magField = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_magField.grid(row=0, column=3)
        # fixme   alpha_1
        label_alpha_1 = Label(self.window, text='alpha_1 :', relief=RIDGE, width=20)
        label_alpha_1.grid(row=1, column=2)
        self.entry_alpha_1 = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_alpha_1.grid(row=1, column=3)
        # fixme alpha_2
        label_alpha_2 = Label(self.window, text='alpha_2 :', relief=RIDGE, width=20)
        label_alpha_2.grid(row=2, column=2)
        self.entry_alpha_2 = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_alpha_2.grid(row=2, column=3)
        # fixme  break_eng
        label_break = Label(self.window, text='Break energy :', relief=RIDGE, width=20)
        label_break.grid(row=3, column=2)
        self.entry_break = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_break.grid(row=3, column=3)
        if self.synch_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.synchrotron_plotFunc)
            plt_btn.grid(row=20, column=20)
        elif self.ssc_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.ssc_plotFunc)
            plt_btn.grid(row=20, column=20)
        elif self.ic_bool.get() == 1:
            plt_btn = Button(self.window, text="Plot", bg="red", command=self.eic_plotFunc)
            plt_btn.grid(row=20, column=20)

    def synchrotron_plotFunc(self):
        """
        After choosing a law(using checkboxes) correspondig  values of parameters will be  taken from labels.
        Below of the function synchrotron_plotter is called  from SYnchrotron.py module
        which plots low energy component of SED of blazar.
        """
        if (self.CutOff_Law.get() == 1) and (self.Broken_Law.get() == 0):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha = np.float(self.entry_alpha.get())
            self.cutOff = np.float(self.entry_cutOff.get())
            self.alpha1 = None  # if click CutOff_PL all broken param. values will be none
            self.alpha2 = None
            self.broken = None

        elif (self.CutOff_Law.get() == 0) and (self.Broken_Law.get() == 1):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha1 = np.float(self.entry_alpha_1.get())
            self.alpha2 = np.float(self.entry_alpha_2.get())
            self.broken = np.float(self.entry_break.get())
            self.alpha = None  # if click Broken_PL all cutOff param. values will be none
            self.cutOff = None
        else:
            return "Choose something"
        synchrotron_plotter(self.magfield, self.alpha, self.alpha1, self.alpha2, self.cutOff, self.broken,
                            self.CutOff_Law.get(), self.Broken_Law.get())
        self.master.destroy()

    def ssc_plotFunc(self):
        """
        After choosing one of laws(using checkboxes) correspondig  values of parameters will be  taken from labels
        below of the function ssc_plotter is called  from SSC.py module
        which plots high energy component of SED of blazar.
        """
        if (self.CutOff_Law.get() == 1) and (self.Broken_Law.get() == 0):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha = np.float(self.entry_alpha.get())
            self.cutOff = np.float(self.entry_cutOff.get())
            self.alpha1 = None  # if click CutOff_PL all broken param. values will be none
            self.alpha2 = None
            self.broken = None

        elif (self.CutOff_Law.get() == 0) and (self.Broken_Law.get() == 1):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha1 = np.float(self.entry_alpha_1.get())
            self.alpha2 = np.float(self.entry_alpha_2.get())
            self.broken = np.float(self.entry_break.get())
            self.alpha = None  # if click Broken_PL all cutOff param. values will be none
            self.cutOff = None
        else:
            return "Choose something"
        ssc_plotter(self.magfield, self.alpha, self.alpha1, self.alpha2, self.cutOff, self.broken,
                    self.CutOff_Law.get(), self.Broken_Law.get())
        self.master.destroy()

    def eic_plotFunc(self):
        """
        After choosing a law(using checkboxes) correspondig  values of parameters will be  taken from labels
        below of the function eic_plotter is called  from EIC.py module
        which plots high energy component of SED of blazar.
        """
        if (self.CutOff_Law.get() == 1) and (self.Broken_Law.get() == 0):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha = np.float(self.entry_alpha.get())
            self.cutOff = np.float(self.entry_cutOff.get())
            self.alpha1 = None  # if click CutOff_PL all broken param. values will be none
            self.alpha2 = None
            self.broken = None

        elif (self.CutOff_Law.get() == 0) and (self.Broken_Law.get() == 1):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha1 = np.float(self.entry_alpha_1.get())
            self.alpha2 = np.float(self.entry_alpha_2.get())
            self.broken = np.float(self.entry_break.get())
            self.alpha = None  # if click Broken_PL all cutOff param. values will be none
            self.cutOff = None
        else:
            return "Choose something"
        cmb_plotter(self.magfield, self.alpha, self.alpha1, self.alpha2, self.cutOff, self.broken,
                    self.CutOff_Law.get(), self.Broken_Law.get())
        self.master.destroy()


root = Tk()
Plotter_GUI(root)
root.mainloop()
