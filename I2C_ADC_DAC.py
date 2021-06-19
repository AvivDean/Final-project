import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial as sr
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter as xls
from PIL import ImageTk, Image
import adafruit_mcp4725
import math



#---I2C configuration---#

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
ads.gain = 1

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)


#print("{:>5}\t{:>5.5f}".format(chan0.value, chan0.voltage))
time.sleep(0.5)

#---Export data file---
#create xls file
outWorkbook = xls.Workbook("VoltageValues.xlsx")
outSheet = outWorkbook.add_worksheet()

header = "Voltage"

outSheet.write(0,0,header)


#---np variables---#

#---global  variables---#
data = np.array([])
cond = False
numOfSamples = 1
isGenerate = False
i = 1

#---plotting functions---#

def plot_data():
    global cond, data, numOfSamples, status, isGenerate, i, freq_val
    dac = adafruit_mcp4725.MCP4725(i2c)
    freq = int(freq_val)
    x = np.linspace(0,100,freq)
    y = 2.5 + 2.5*np.sin(2*math.pi*x)
    
    if (cond==True):
        status.pack_forget()
        status = Label(root,text='Sampling input signal - in progress...', bd=1, relief=SUNKEN, anchor=E)

        status.pack(side=BOTTOM, fill=X)
        V0 = chan0.voltage
        V1 = chan1.voltage
        V2 = chan2.voltage
        V3 = chan3.voltage
        
        V_SUM = V0+V1+V2+V3
        V_SUB = V0-V1-V2-V3
        V_MUL = V0*V1*V2*V3
        
        #A0_input_plt(V0)      
        #V_SUM_plt(V_SUM)
        #V_SUB_plt(V_SUB)
        #V_MUL_plt(V_MUL)
        
        #print("{:>5}\t{:>5.5f}".format(chan0.value, V))       ///print voltage and raw values of ADC
        numOfSamples= numOfSamples + 1
        outSheet.write(numOfSamples, 0, V0)
    
    if(isGenerate==True):

#       sin(freq_val)
        #new_y = 2.5 + 2.5*np.sin(2*math.pi*x-0.5*i)
        dac.raw_value = 2048 - int((2046)*(np.sin((2*math.pi*i)/4095)))        
        #lines1.set_xdata(np.arange(0,len(x)))
        #lines1.set_ydata(new_y)
        #print(dac.raw_value)
        i = i+1
        #canvas1.draw()    
    else:
        pass
    

    root.after(1,plot_data)


def A0_input_plt(V):
    global data, lines
    if(len(data) <100):
        data=np.append(data,V)
    else:
        data[0:99] = data[1:100]
        data[99] = V
    lines.set_xdata(np.arange(0,len(data)))
    lines.set_ydata(data)

    canvas.draw()
    

def V_SUM_plt(SUM):
    global data, lines2
    if(len(data) <100):
        data=np.append(data,SUM)
    else:
        data[0:99] = data[1:100]
        data[99] = SUM
    lines2.set_xdata(np.arange(0,len(data)))
    lines2.set_ydata(data)

    canvas.draw() 


def V_SUB_plt(SUB):
    global data, lines3
    if(len(data) <100):
        data=np.append(data,SUB)
    else:
        data[0:99] = data[1:100]
        data[99] = SUB
    lines3.set_xdata(np.arange(0,len(data)))
    lines3.set_ydata(data)
    print(SUB)

    canvas.draw()
    
    
def V_MUL_plt(MUL):
    global data, lines4
    if(len(data) <100):
        data=np.append(data,MUL)
    else:
        data[0:99] = data[1:100]
        data[99] = MUL
    lines4.set_xdata(np.arange(0,len(data)))
    lines4.set_ydata(data)
    print(MUL)

    canvas.draw() 



def plot_start():
    global cond
    cond = True

        
def plot_stop():
    global cond, status
    cond = False
    status.pack_forget()
    status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)

def generate_signal_start():
    global isGenerate, status
    status.pack_forget()
    status = Label(root,text='Generating random sine signal - in progress...', bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)
    isGenerate = True


def generate_signal_stop():
    global isGenerate, status
    isGenerate = False
    status.pack_forget()
    status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)


# def sin(freq_val):
#     global isGenerate
#     freq = int(freq_val)
#     x = np.linspace(0,100,freq)
#     y = 2.5 + 2.5*np.sin(x)
#     dac = adafruit_mcp4725.MCP4725(i2c)
# 
#     plt.ion()
#     figure, ax = plt.subplots(figsize=(18,10))
#     line1, = ax.plot(x,y)
# 
#     if isGenerate==True:
#         for _ in range (0, 9000, 1):
#             new_y = 2.5 + 2.5*np.sin(2*math.pi*x-0.5*_)
#             dac.raw_value = 2048 - int(2046*(math.sin((2*math.pi*_)/4095)))
#             line1.set_xdata(x)
#             line1.set_ydata(new_y)
#         
#             figure.canvas.draw()
#             figure.canvas.flush_events()
        
    
#-----main GUI code-----
root = Tk()
root.title('CEMOP')
root.geometry('1250x720')
#root.wm_iconbitmap("home/pi/pycharm/Project/settings_icon.png")
my_pic = ImageTk.PhotoImage(Image.open("download.jpeg"))
my_bg = Label(root, image=my_pic)
my_bg.place(x=0,y=0,relwidth=1,relheight=1)


fig = Figure();
fig1 = Figure()
ax1 = fig1.add_subplot(111)
ax = fig.add_subplot(111)

ax1.set_title('Analog output')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Voltage')
ax1.set_xlim(0,100)
ax1.set_ylim(-0.5,5)
lines1 = ax1.plot([],[])[0]

ax.set_title('Digital Input From ADS1115')
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,5)
lines = ax.plot([],[])[0]

ax.set_title('Sum of all analog inputs')
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,5)
lines2 = ax.plot([],[])[0]

ax.set_title('Sub of all analog inputs')
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,5)
lines3 = ax.plot([],[])[0]

ax.set_title('Mul of all analog inputs')
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,5)
lines4 = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().place(x = 640, y = 10, width = 600, height = 400)
canvas1.draw()


root.update()
start_bt = Button(root, text="Start", font= ('calbiri',12), padx = 40, command = plot_start)
stop_bt = Button(root, text="Stop", font= ('calbiri',12), padx = 40, command = plot_stop)
export_data_bt = Button(root, text="Export to Excel", font= ('calbiri',12),padx=66, command = lambda: outWorkbook.close())
#creat_signal_label = Label(root,text = "Generate Signal", bg="black", fg="white", font=('calbiri', 14))
exit_bt = Button(root, text="Exit Program", command=lambda: exit())
freq_var = IntVar(root)
freq_entry = Entry(root, textvariable = freq_var, width = 10)
freq_val = freq_entry.get()
freq_entry_label= Label(root, text= "Enter Frequancy Here:", font=('calbiri', 12), bg='gray', fg='black')
generate_signal_bt = Button(root, text= 'Start Signal', font=('calbiri',12), padx=10, pady=0, command=generate_signal_start)
stop_generate_signal_bt = Button(root, text = 'Stop Signal', font=('calbiri',12), padx=10, pady=0, command=generate_signal_stop)
status = Label(root,text='waiting for action...', bd=1, relief=SUNKEN, anchor=E)


start_bt.place(x=10,y=430)
stop_bt.place(x=start_bt.winfo_x()+start_bt.winfo_reqwidth()+20, y=430)
export_data_bt.place(x=10, y=470)
#creat_signal_label.place(x=620, y=430)
exit_bt.place(x=10,y=660)
freq_entry.place(x=830, y=430)
freq_entry_label.place(x=640,y=430)
generate_signal_bt.place(x=640, y=470)
stop_generate_signal_bt.place(x=765, y=470)
status.pack(side=BOTTOM, fill=X)


root.after(1, plot_data)
root.mainloop()

