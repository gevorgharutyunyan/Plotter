from tkinter import*
import numpy as np
from Synchrotron import synchrotron_plotter

class Plotter_GUI:
    def __init__(self,master):
        self.master = master
        master.title("Plotter")
        master.geometry('{}x{}'.format(master.winfo_screenwidth(), master.winfo_screenmmheight()))
        self.synchrotron_btn = Button(master, text="Synchrotron", height=10, width=10, bg="blue",command = self.param_winwow).place(relx=0.1, rely=0.3, anchor='e')
        #self.self_synchrotron_btn = Button(master, text="SSC", height=10, width=10, bg="red",command=self.param_winwow).place(relx=0.5, rely=0.3, anchor='e')

        #self.inverse_compton_btn = Button(master, text="IC", height=10, width=10, bg="green",command=self.param_winwow).place(relx=0.9, rely=0.3, anchor='e')


    def param_winwow(self):

        self.window = Toplevel()
        self.window.title("Synchrotron parameters")
        self.CutOff_Law = IntVar()
        self.Broken_Law = IntVar()
        self.CutOff_PL = Checkbutton(self.window, text='CutOff_PL', variable=self.CutOff_Law, onvalue=1, offvalue=0,command=self.open_cutoff_param)
        self.CutOff_PL.grid(row=5, column=0)
        self.Broken_PL = Checkbutton(self.window, text='Broken_PL', variable=self.Broken_Law, onvalue=1, offvalue=0,command=self.open_broken_param)
        self.Broken_PL.grid(row=5, column=1)

    def open_cutoff_param(self):

        # magnetic field
        label_magField = Label(self.window,text='Magnetic field :',relief = RIDGE,width = 20)
        label_magField.grid(row=0,column=0)
        self.entry_magField = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_magField.grid(row=0, column=1)

        #alpha
        label_alpha = Label(self.window,text='alpha :',relief = RIDGE,width = 20)
        label_alpha.grid(row=1,column=0)
        self. entry_alpha = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_alpha.grid(row=1, column=1)

        # gamma_cutOff
        label_cutOff = Label(self.window, text='Cut_OFF energy :', relief=RIDGE, width=20)
        label_cutOff.grid(row=2, column=0)
        self.entry_cutOff = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_cutOff.grid(row=2, column=1)
        plt_btn = Button(self.window,text = "Plot",bg = "red",command = self.ploting_func)
        plt_btn.grid(row = 20,column = 20)



    def open_broken_param(self):

        # magnetic field
        label_magField = Label(self.window,text='Magnetic field :',relief = RIDGE,width = 20)
        label_magField.grid(row=0,column=0)
        self.entry_magField = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_magField.grid(row=0, column=1)
        # alpha_1
        label_alpha_1 = Label(self.window, text='alpha_1 :', relief=RIDGE, width=20)
        label_alpha_1.grid(row=1, column=0)
        self.entry_alpha_1 = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_alpha_1.grid(row=1, column=1)
        # alpha_2
        label_alpha_2 = Label(self.window, text='alpha_2 :', relief=RIDGE, width=20)
        label_alpha_2.grid(row=2, column=0)
        self.entry_alpha_2 = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_alpha_2.grid(row=2, column=1)
        #break_eng
        label_break = Label(self.window, text='Break energy :', relief=RIDGE, width=20)
        label_break.grid(row=3, column=0)
        self.entry_break = Entry(self.window, width=20, relief=SUNKEN)
        self.entry_break.grid(row=3, column=1)
        plt_btn = Button(self.window,text = "Plot",bg = "red",command = self.ploting_func)
        plt_btn.grid(row = 20,column = 20)


    def ploting_func(self):
        if  (self.CutOff_Law.get() == 1) and(self.Broken_Law.get()==0):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha  = np.float(self.entry_alpha.get())
            self.cutOff = np.float(self.entry_cutOff.get())
            self.alpha1   = None
            self.alpha2   = None
            self.broken   = None
        elif (self.CutOff_Law.get() == 0) and(self.Broken_Law.get()==1):
            self.magfield = np.float(self.entry_magField.get())
            self.alpha1   = np.float(self.entry_alpha_1.get())
            self.alpha2   = np.float(self.entry_alpha_2.get())
            self.broken   = np.float(self.entry_break.get())
            self.alpha = None
            self.cutOff = None
        else:
            return "Choose something"
        synchrotron_plotter(self.magfield, self.alpha,self.alpha1,self.alpha2, self.cutOff,self.broken,self.CutOff_Law.get(),self.Broken_Law.get())
        self.master.destroy()


root = Tk()
Plotter_GUI(root)
root.mainloop()
