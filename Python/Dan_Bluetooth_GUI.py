"""

Control Panel>Hardware>Printers>Other Devices>MaximusRoboticus
Bluetooth>Unique identifier
98:d3:32:21:40:d1
Services: Serial Port
COM5

Baud rate
38400

Windows 10 Bluetooth Serial Terminal (Microsoft App store)
https://www.microsoft.com/en-gb/p/bluetooth-serial-terminal/9wzdncrdfst8?activetab=pivot%3Aoverviewtab
"""

import serial # pip install pySerial
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
#import filedialog
#from tkinter import messagebox

port = 'COM5' # Device>Services>Serial Port
baud = 38400 # Get from TBot.ino
bluetooth = serial.Serial(port,baud)

def blueread():
	try:
		line = bluetooth.readline().decode().strip().split()
		print(line)
	except:
		print('read didnt''t work')
        bluetooth.close()
        #sys.exit()
        line = []
	return line

def bluewrite(sendstr):
	try:
		bluetooth.write(sendstr.encode(encoding='utf-8'))
	except:
		print('send didn''t work')
        bluetooth.close()
        #sys.exit()

def bluejoystick(jx,jy):
	print('x '+str(jx)+' y '+str(jy))
	sendstring = chr(0X02)+str(jx)+str(jy)+chr(0X03)
	print(sendstring)
	bluewrite(sendstring)

# Fonts
TF= ["Times", 10]
BF= ["Times", 14]
SF= ["Times New Roman", 14]
LF= ["Times", 14]
HF= ['Courier',12]


class TbotGui:
    """
    Simple graphical user interface to send commands to the T-Bot
    """
    def __init__(self,xtl=None):
        "Initialise"
        
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('T-Bot Controller by D G Porter')
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=1920, height=1200)
        
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT,anchor=tk.N)
        
        # Filename (variable)
        f_file = tk.Frame(frame)
        f_file.pack(side=tk.TOP,expand=tk.YES,fill=tk.X)
        self.file = tk.StringVar(frame,self.xtl.filename)
        var = tk.Label(f_file, text='CIF file:',font=SF,width=10)
        var.pack(side=tk.LEFT,expand=tk.NO)
        var = tk.Label(f_file, textvariable=self.file,font=TF,width=50)
        var.pack(side=tk.LEFT,expand=tk.YES)
        var = tk.Button(f_file, text='Load CIF',font=BF, command=self.fun_loadcif)
        var.pack(side=tk.LEFT,expand=tk.NO,padx=5)
        
        # Name (variable)
        f_name = tk.Frame(frame)
        f_name.pack(side=tk.TOP,expand=tk.YES,fill=tk.X)
        self.name = tk.StringVar(frame,self.xtl.name)
        var = tk.Label(f_name, text='Name:',font=SF,width=10)
        var.pack(side=tk.LEFT)
        var = tk.Entry(f_name, textvariable=self.name,font=TF, width=40)
        var.pack(side=tk.LEFT)
        var.bind('<Return>',self.update_name)
        var.bind('<KP_Enter>',self.update_name)
        
        # Buttons 1
        f_but = tk.Frame(frame)
        f_but.pack(side=tk.TOP)
        var = tk.Button(f_but, text='Lattice\nParameters', font=BF, command=self.fun_latpar)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Symmetric\nPositions', font=BF, command=self.fun_atoms)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Symmetry\nOperations', font=BF, command=self.fun_symmetry)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='General\nPositions', font=BF, command=self.fun_structure)
        var.pack(side=tk.LEFT)
        
        # Buttons 2
        f_but = tk.Frame(frame)
        f_but.pack(side=tk.TOP)
        var = tk.Button(f_but, text='Plot\nCrystal', font=BF, command=self.fun_plotxtl)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Simulate\nStructure Factors', font=BF, command=self.fun_simulate)
        var.pack(side=tk.LEFT)
    
    ###################################################################################
    ############################## FUNCTIONS ##########################################
    ###################################################################################
    def fun_set(self):
        self.file.set(self.xtl.filename)
        self.name.set(self.xtl.name)
    
    def fun_get(self):
        self.xtl.name = self.name.get()
    
    def fun_loadcif(self):
        #root = Tk().withdraw() # from Tkinter
        filename = filedialog.askopenfilename(initialdir=os.path.expanduser('~'),\
        filetypes=[('cif file','.cif'),('magnetic cif','.mcif'),('All files','.*')]) # from tkFileDialog
        if filename:
            self.xtl = Crystal(filename)
            self.fun_set()
    
    def update_name(self):
        newname = self.name.get()
        self.xtl.name = newname
    
    def fun_latpar(self):
        self.fun_set()
        Latpargui(self.xtl)
    
    def fun_atoms(self):
        self.fun_set()
        if np.any(self.xtl.Atoms.mxmymz()):
            Atomsgui(self.xtl,True,True)
        else:
            Atomsgui(self.xtl,True,False)
    
    def fun_structure(self):
        self.fun_set()
        if np.any(self.xtl.Structure.mxmymz()):
            Atomsgui(self.xtl,False,True)
        else:
            Atomsgui(self.xtl,False,False)
    
    def fun_symmetry(self):
        self.fun_set()
        Symmetrygui(self.xtl)
    
    def fun_plotxtl(self):
        self.fun_set()
        self.xtl.Plot.plot_crystal()
    
    def fun_simulate(self):
        self.fun_set()
        Scatteringgui(self.xtl)