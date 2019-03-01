"""
Bluetooth controller for T-Bot, using Tkinter
***Currently under development!

Python 3.7 required!

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

# Set TkAgg environment
import matplotlib
matplotlib.use('TkAgg')
#import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
import serial # pip install pySerial, only available in python 3.x+

#####################################################################
#######################  Bluetooth Functions  #######################
#####################################################################

port = 'COM5' # Device>Services>Serial Port
baud = 38400 # Get from TBot.ino
try:
    bluetooth = serial.Serial(port,baud)
    print('Bluetooth Module started')
except serial.serialutil.SerialException:
    print('Bluetooth not available')
    bluetooth = open('Dan_Bluetooth_test.txt', 'w')

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

#####################################################################
#######################  Interface Functions  #######################
#####################################################################

# Fonts
TF= ["Times", 20, 'bold'] # title font
BF= ["Times", 14] # button font
SF= ["Times New Roman", 14] # Small font
LF= ["Times", 14] # large font
HF= ['Courier',12] # 
# Colours - background
bkg = 'snow'
ety = 'white'
btn = 'light slate blue'
opt = 'light slate blue'
# Colours - active
btn_active = 'grey'
opt_active = 'grey'
# Colours - Fonts
txtcol = 'black'
btn_txt = 'black'
ety_txt = 'black'
opt_txt = 'black'


class TbotGui:
    """
    Simple graphical user interface to send commands to the T-Bot
    """
    def __init__(self,xtl=None):
        """Initialise"""
        
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('T-Bot Controller by D G Porter')
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)

        self.joybox_size = 100
        self.joystick_size = 60
        self.pixel_x = self.joybox_size//2
        self.pixel_y = self.joybox_size//2
        self.joystick_x = 0.0
        self.joystick_y = 0.0
        
        w = tk.Label(self.root, text='T-Bot Controller', bg='red', font=TF)
        w.pack(expand=tk.YES, fill=tk.X)

        # Line 1
        frame = tk.Frame(self.root)
        frame.pack()

        w = tk.Label(frame, text='Port:', font=SF, width=10)
        w.pack(side=tk.LEFT)

        self.port = tk.StringVar(frame, 'COM5')
        w = tk.Entry(frame, textvariable=self.port, font=SF, width=20, bg=ety, fg=ety_txt)
        w.pack(side=tk.LEFT)

        w = tk.Button(frame, text='Connect', font=BF, width=10, bg=btn, fg=btn_txt)
        w.pack(side=tk.RIGHT)

        # Line 2
        frame = tk.Frame(self.root)
        frame.pack()

        w = tk.Label(frame, text='Baud rate:', font=SF, width=10)
        w.pack(side=tk.LEFT)

        self.baud = tk.IntVar(frame, 38400)
        w = tk.Entry(frame, textvariable=self.baud, font=SF, width=20, bg=ety, fg=ety_txt)
        w.pack(side=tk.LEFT)

        w = tk.Button(frame, text='Disconnect', font=BF, width=10, bg=btn, fg=btn_txt)
        w.pack(side=tk.RIGHT)

        # Joystick
        frame = tk.Frame(self.root, bg='black')
        frame.pack(expand=tk.YES, fill=tk.BOTH)

        self.joybox = tk.Canvas(frame, 
            bg='white', 
            height=self.joybox_size, 
            width=self.joybox_size)
        self.joybox.bind('<B1-Motion>', self.onLeftDrag) 
        self.joybox.bind('<ButtonPress-1>', self.onLeftClick)
        self.joybox.bind('<ButtonRelease-1>', self.onLeftRelease)
        self.joybox.pack(padx=20, pady=20)

        self.joybox.create_oval(
            self.pixel_x-5, 
            self.pixel_y-5, 
            self.pixel_x+5, 
            self.pixel_y+5, 
            fill='black')
        self.stk = self.joybox.create_line(
            self.pixel_x,
            self.pixel_y,
            self.pixel_x,
            self.pixel_y,
            fill='black', width=10)
        """
        self.joy = self.joybox.create_oval(
            self.pixel_x-self.joystick_size//2, 
            self.pixel_y-self.joystick_size//2, 
            self.pixel_x+self.joystick_size//2, 
            self.pixel_y+self.joystick_size//2, 
            fill='slateblue')
        """
        pos = self.circle(
            xpos=self.pixel_x, 
            ypos=self.pixel_y, 
            size=self.joystick_size//2)
        self.joy = self.joybox.create_polygon(pos, fill='slateblue')

        """
        w = tk.Label(frame, text='Click\'n Drag Here!', bg='white', font=HF)
        w.config(height=5, width=20)
        w.bind('<B1-Motion>', self.onLeftDrag) 
        w.bind('<ButtonPress-1>', self.onLeftClick)
        w.bind('<ButtonRelease-1>', self.onLeftRelease)
        w.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx=50, pady=50)
        """
        # Start GUI
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    ###################################################################################
    ############################## FUNCTIONS ##########################################
    ###################################################################################
    def circle(self, xpos=0, ypos=0, size=1.0, flat=1.0, rot=0.0):
        """
        Create coordinates of rotated oval 
        """
        ang_deg = range(361)
        ang_rad = [math.radians(ang) for ang in ang_deg]
        x = [flat*math.sin(ang) for ang in ang_rad]
        y = [math.cos(ang) for ang in ang_rad]
        xx = [x[n]*math.cos(rot)-y[n]*math.sin(rot) for n in ang_deg]
        yy = [x[n]*math.sin(rot)+y[n]*math.cos(rot) for n in ang_deg]
        out = []
        for n in ang_deg:
            out += [xpos+size*xx[n], ypos+size*yy[n]]
        return out

    def getJoyStick(self, event):
        w = event.widget
        xpos = event.x
        ypos = event.y
        xmax = w.winfo_width()
        ymax = w.winfo_height()

        xrat = float(xpos)/xmax - 0.5
        yrat = float(ypos)/ymax - 0.5
        dist = (xrat**2 + yrat**2)**0.5
        angle = math.atan2(yrat, xrat)
        if dist > 0.25: dist=0.25
        x = dist*math.cos(angle)
        y = dist*math.sin(angle)

        self.joystick_x = x*4
        self.joystick_y = y*4
        self.pixel_x = int((0.5 + x)*self.joybox_size)
        self.pixel_y = int((0.5 + y)*self.joybox_size)
        """
        if xpos > self.joystick_size//2 and xpos < xmax-self.joystick_size//2:
            self.pixel_x = xpos
            self.joystick_x = xrat
        if ypos > self.joystick_size//2 and ypos < xmax-self.joystick_size//2:
            self.pixel_y = ypos
            self.joystick_y = yrat
        """

    def returnJoyStick(self):
        self.pixel_x = self.joybox_size//2
        self.pixel_y = self.joybox_size//2
        self.joystick_x = 0
        self.joystick_y = 0

    def joyStickMove(self):
        joyx = self.joystick_x
        joyy = self.joystick_y
        print('Joystick: X=%5.2f Y=%5.2f'%(joyx, joyy))

        dist = 1-0.5*(joyx**2 + joyy**2)**0.5
        angle = math.atan2(joyy, joyx)
        pos = self.circle(
            xpos=self.pixel_x, 
            ypos=self.pixel_y, 
            size=self.joystick_size//2, 
            flat=dist, 
            rot=angle)

        self.joybox.coords(self.stk,
            self.joybox_size//2,
            self.joybox_size//2,
            self.pixel_x,
            self.pixel_y)
        self.joybox.coords(self.joy, pos)

    def onLeftDrag(self, event):
        self.getJoyStick(event)
        self.joyStickMove()
        
    def onLeftClick(self, event):
        self.getJoyStick(event)
        self.joyStickMove()

    def onLeftRelease(self, event):
        self.returnJoyStick()
        self.joyStickMove()

    def on_closing(self):
        """close window"""
        print('GoodByee!')
        self.root.destroy()
        bluetooth.close()


if __name__ == '__main__':
    tbot = TbotGui()