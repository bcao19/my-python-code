"""
Plot power spectrum density of signals in EAST
chunan@ipp.ac.cn 2018.07.11
"""
import Tkinter as tk
import ttk
import numpy
import matplotlib as plt
import pylab
import sys
import os

# import Fgiure toolbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

plt.use('TkAgg')
pi = numpy.pi


# load user function modules
# sys.path.append(os.path.abspath('../../'))
from function_lib import plot_lib
from function_lib import readdata_lib
from function_lib import signal_lib
# from function_lib import math_lib
from function_lib import diagnostics_lib as diag_lib
font_size = 16



class PSD_App(tk.Frame) :
    """
    Plot Power Spectrum Density of a signal in EAST
    """
    def __init__(self, master) :
        # initialize window
        tk.Frame.__init__(self, master, width = 1060, height = 670)
        # set title
        self.master.title('PSD for EAST signals by N. Chu')
        # set the relative resolution
        self.tk.call('tk', 'scaling', 1.2)
        # set ttk styles
        self.style = ttk.Style()
        #('clam', 'alt', 'default', 'classic')
        self.style.theme_use("alt")
        # This allows the size specification to take effect
        self.pack_propagate(0)
        # We'll use the flexible pack layout manager
        self.pack()


        # Label for EAST shot
        Label_shot = tk.Label(self, text = 'shot', font = ("Arial", font_size))
        Label_shot.place(relx = 0.005, rely = 0)

        
        # Text input for shot number
        self.recipient1_shot = tk.IntVar()
        self.recipient1 = tk.Entry(self,textvariable=self.recipient1_shot,
        font=("Arial", font_size))
        self.recipient1_shot.set('78620')
        self.recipient1.place(relx = 0.08, rely = 0, relwidth = 0.08)        


        # Label for MDS tree
        Label_tree = tk.Label(self, text = 'tree', font = ("Arial", font_size))
        Label_tree.place(relx = 0.005, rely = 0.05)

        
        # Text input for MDS tree
        self.recipient2_tree = tk.StringVar()
        self.recipient2 = tk.Entry(self,textvariable=self.recipient2_tree,
        font=("Arial", font_size))
        self.recipient2_tree.set('EAST')
        self.recipient2.place(relx = 0.08, rely = 0.05, relwidth = 0.08) 


        # Label for EAST signal name
        Label_name = tk.Label(self, text = 'name', font = ("Arial", font_size))
        Label_name.place(relx = 0.005, rely = 0.1)

        
        # Text input for signal name
        self.recipient3_name = tk.StringVar()
        self.recipient3 = tk.Entry(self,textvariable=self.recipient3_name,
        font=("Arial", font_size))
        self.recipient3_name.set('CMP1T')
        self.recipient3.place(relx = 0.08, rely = 0.1, relwidth = 0.08)  
        
        
        # Label for start time
        Label_t_start = tk.Label(self, text = 't start (s)', font = ("Arial", font_size))
        Label_t_start.place(relx = 0.005, rely = 0.15)


        # Text input for start time
        self.recipient_tstart = tk.StringVar()
        self.recipient_start = tk.Entry(self,textvariable=self.recipient_tstart,
        font=("Arial", font_size))
        self.recipient_tstart.set('2')
        self.recipient_start.place(relx = 0.08, rely = 0.15, relwidth = 0.08)   
        
        
        # Label for end time
        Label_t_end = tk.Label(self, text = 't end (s)', font = ("Arial", font_size))
        Label_t_end.place(relx = 0.005, rely = 0.2)
        
        
        # Text input for end time
        self.recipient_tend = tk.StringVar()
        self.recipient_end = tk.Entry(self,textvariable=self.recipient_tend,
        font=("Arial", font_size))
        self.recipient_tend.set('7')
        self.recipient_end.place( relx = 0.08, rely = 0.2, relwidth = 0.08) 


        # Label for NFFT
        Label_nfft = tk.Label(self, text = 'NFFT', font = ("Arial", font_size))
        Label_nfft.place(relx = 0.005, rely = 0.25)
        
        
        # Text input for NFFT
        self.recipient_nfft = tk.IntVar()
        self.recipient_NFFT = tk.Entry(self,textvariable=self.recipient_nfft,
        font=("Arial", font_size))
        self.recipient_nfft.set(1024)
        self.recipient_NFFT.place( relx = 0.08, rely = 0.25, relwidth = 0.08) 
        

        # Label for sampling points
        Label_dn = tk.Label(self, text = 'dn', font = ("Arial", font_size))
        Label_dn.place(relx = 0.005, rely = 0.30)
        
        
        # Text input for sampling points
        self.recipient_dn = tk.IntVar()
        self.recipient_DN = tk.Entry(self,textvariable=self.recipient_dn,
        font=("Arial", font_size))
        self.recipient_dn.set(1)
        self.recipient_DN.place( relx = 0.08, rely = 0.30, relwidth = 0.08) 
        
        
        # read EAST data
        shot = self.recipient1_shot.get()
        tree = self.recipient2_tree.get()
        sig_name = self.recipient3_name.get()
        t_start = numpy.float(self.recipient_tstart.get())
        t_end = numpy.float(self.recipient_tend.get())
        nfft = self.recipient_nfft.get()
        sig, t, _ = readdata_lib.read_signal_fast(tree = tree, shot = shot,
                    sig_name = sig_name, t_in = [t_start, t_end])
        # calculate PSD for the signal
        # PSD_raw, f, t_fix = signal_lib.psdplot(sig = sig, t = t, nfft = nfft)
        # PSD_raw_real = numpy.log10(numpy.abs(PSD_raw))
        Fs = 1.0/((t[2]-t[0])/2.0)
        
        # Initiate figure        
        f = pylab.figure(figsize = (11, 8))
        a = f.add_subplot(111)
        # a.pcolormesh(t_fix, f/1000.0, PSD_raw_real)
        # a.contourf(t_fix, f/1000.0, PSD_raw_real, cmap = 'jet')
        # a.plot(t, sig)
        a.set_xlim([t_start, t_end])
        a.set_ylim([0, Fs/2.0/1000])
        # a.set_ylim([0, 500])
        
        a.set_xlabel('t (s)')
        a.set_ylabel('f (kHz)')
        a.set_title('EAST PSD #' + str(000) + ', ' + sig_name)
        plot_lib.single_axis_paras(a)
        a.grid('off')
        f.tight_layout()
        
        
        # Design tk Drawing Area
        canvas = FigureCanvasTkAgg(f, master = self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        # Control plot area
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)        
        canvas._tkcanvas.place(relx = 0.17, rely = 0.0)
        # canvas._tkcanvas.grid(row = 2, column = 1)
        
        
        
        
        # design plot button
        self.go_button = tk.Button(self,text='Plot',
        command=lambda: self.replot(canvas,a),font=("Arial", font_size))     
        self.go_button.place(relx = 0.01, rely = 0.35) 




    def replot(self, canvas, ax) :
        """Refresh the plot of PSD figure"""
        dn = self.recipient_dn.get()
        shot = self.recipient1_shot.get()
        tree = self.recipient2_tree.get()
        sig_name = self.recipient3_name.get()
        t_start = numpy.float(self.recipient_tstart.get())
        t_end = numpy.float(self.recipient_tend.get())
        nfft = self.recipient_nfft.get()
        sig, t, _ = readdata_lib.read_signal_fast(tree = tree, shot = shot,
        sig_name = sig_name, t_in = [t_start, t_end], dn = dn)
        # calculate PSD for the signal
        PSD_raw, f, t_fix = signal_lib.psdplot(sig = sig, t = t, nfft = nfft)
        PSD_raw_real = numpy.log10(numpy.abs(PSD_raw))
        Fs = 1.0/((t[2]-t[0])/2.0)
        # plot figure out
        ax.clear()
        ax.pcolormesh(t_fix, f/1000, PSD_raw_real) 
        # ax.contourf(t_fix, f/1000.0, PSD_raw_real, 10, cmap = 'jet')     
        ax.set_xlim((t_fix[0],t_fix[len(t_fix)-1])) 
        ax.set_ylim([0, Fs/2.0/1000])
        ax.set_xlabel('t (s)')
        ax.set_ylabel('f (kHz)')
        ax.set_title('EAST PSD #' + str(shot) + ', ' + sig_name)
        plot_lib.single_axis_paras(ax)
        ax.grid('off')
        canvas.draw()




    def run(self) :
        """run this GUI"""
        self.mainloop()
        



app = PSD_App(tk.Tk())
app.run()

















