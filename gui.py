from tkinter import*
from Synchrotron import synchrotron_plotter
import numpy as np

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

        # magnetic field
        label_magField = Label(self.window,text='Magnetic field :',relief = RIDGE,width = 20)
        label_magField.grid(row=0,column=0)
        self.entry_magField = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_magField.grid(row=0, column=1)

        #slope
        label_index = Label(self.window,text='Index :',relief = RIDGE,width = 20)
        label_index.grid(row=1,column=0)
        self. entry_index = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_index.grid(row=1, column=1)


        #gamma_cutOff
        label_cutOff = Label(self.window,text='Cut_OFF energy :',relief = RIDGE,width = 20)
        label_cutOff.grid(row=2, column=0)
        self.entry_cutOff = Entry(self.window,width=20,relief=SUNKEN)
        self.entry_cutOff.grid(row=2, column=1)

        plt_btn = Button(self.window,text = "Plot",bg = "red",command = self.ploting_func)
        plt_btn.grid(row = 20,column = 20)

    def ploting_func(self):
       self.magfield = np.float(self.entry_magField.get())
       self.index    = np.float(self.entry_index.get())
       self.cutOff   = np.float(self.entry_cutOff.get())
       synchrotron_plotter(self.magfield, self.index, self.cutOff)
       self.master.destroy()

root = Tk()
Plotter_GUI(root)
root.mainloop()
