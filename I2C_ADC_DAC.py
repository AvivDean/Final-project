import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial as sr
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import xlsxwriter as xls
from PIL import ImageTk, Image
import adafruit_mcp4725
import math



#---I2C configuration---#

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
ads.gain = 1

chan = AnalogIn(ads, ADS.P0)
print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
time.sleep(0.5)

#---Export data file---
#create xls file
outWorkbook = xls.Workbook("VoltageValues.xlsx")
outSheet = outWorkbook.add_worksheet()

header = "Voltage"

outSheet.write(0,0,header)



#---global  variables---#
data = np.array([])
cond = False
numOfSamples = 1
isGenerate = False

#---plotting functions---#

def plot_data():
    global cond, data, numOfSamples, status
    
    
    
    if (cond==True):
        status.pack_forget()
        status = Label(root,text='Sampling input signal - in progress...', bd=1, relief=SUNKEN, anchor=E)
        status.pack(side=BOTTOM, fill=X)
        a=chan.voltage
        
        
        if(len(data) <100):
            data=np.append(data,a)
        else:
            data[0:99] = data[1:100]
            data[99] = a
        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)
        
        canvas.draw()   

        print("{:>5}\t{:>5.5f}".format(chan.value, a))
        numOfSamples= numOfSamples + 1
        outSheet.write(numOfSamples, 0, a)

    root.after(1,generate_signal)


def plot_start():
    global cond
    cond = True

        
def plot_stop():
    global cond, status
    cond = False
    isGenerate = False
    status.pack_forget()
    status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)

def generate_signal_start():
    global isGenerate
    isGenerate = True


def generate_signal_stop():
    global isGenerate, status
    isGenerate = False
    status.pack_forget()
    status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)
    
    
def generate_signal():
    global isGenerate, status
    
    
    if (isGenerate==True):
        status.pack_forget()
        status = Label(root,text='Generating random sine signal - in progress...', bd=1, relief=SUNKEN, anchor=E)
        generate_signal_bt = Button(root, text= 'Generate Signal', font=('calbiri',12), padx=10, pady=0, command=generate_signal_stop)
        
        generate_signal_bt.place(x=550, y=120)
        status.pack(side=BOTTOM, fill=X)
        dac = adafruit_mcp4725.MCP4725(i2c, address=0x48)
        for i in range(4095, 0, -50):
            dac.raw_value = 1400 + int(1240*(math.sin(2*math.pi*i/4095)))
            print(dac.raw_value)
    else:
        dac.raw_value = 0
    
    
#-----main GUI code-----
root = Tk()
root.title('CEMOP')
root.geometry('960x720')
#root.wm_iconbitmap("home/pi/pycharm/Project/settings_icon.png")
my_pic = ImageTk.PhotoImage(Image.open("download.jpeg"))
my_bg = Label(root, image=my_pic)
my_bg.place(x=0,y=0,relwidth=1,relheight=1)


fig = Figure();
ax = fig.add_subplot(111)

ax.set_title('Digital Input From ADS1115')
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,5)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 500, height = 400)
canvas.draw()


root.update()
start_bt = Button(root, text="Start", font= ('calbiri',12), padx = 40, command = plot_start)
stop_bt = Button(root, text="Stop", font= ('calbiri',12), padx = 40, command = plot_stop)
export_data_bt = Button(root, text="Export to Excel", font= ('calbiri',12),padx=66, command = lambda: outWorkbook.close())
creat_signal_label = Label(root,text = "Generate Signal", bg="black", fg="white", font=('calbiri', 14))
exit_bt = Button(root, text="Exit Program", command=lambda: exit())
freq_entry = Entry(root, width = 10)
freq_entry_label= Label(root, text= "Enter Frequancy Here:", font=('calbiri', 12), bg='gray', fg='black')
generate_signal_bt = Button(root, text= 'Generate Signal', font=('calbiri',12), padx=10, pady=0, command=generate_signal_start)
status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)


start_bt.place(x=10,y=430)
stop_bt.place(x=start_bt.winfo_x()+start_bt.winfo_reqwidth()+20, y=430)
export_data_bt.place(x=10, y=470)
creat_signal_label.place(x=620, y=30)
exit_bt.place(x=10,y=660)
freq_entry.place(x=738, y=90)
freq_entry_label.place(x=550,y=90)
generate_signal_bt.place(x=550, y=120)
status.pack(side=BOTTOM, fill=X)


root.after(1, plot_data)
root.mainloop()

