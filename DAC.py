import time
import board
import busio
import adafruit_mcp4725
import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation

    
# root = Tk()
# root.title('CEMOP')
# root.geometry('960x720')
#root.wm_iconbitmap("home/pi/pycharm/Project/settings_icon.png")
#my_pic = ImageTk.PhotoImage(Image.open("download.jpeg"))
#my_bg = Label(root, image=my_pic)
#my_bg.place(x=0,y=0,relwidth=1,relheight=1)


# fig = Figure();
# ax = fig.add_subplot(111)
# 
# ax.set_title('Digital Input From ADS1115')
# ax.set_xlabel('Sample')
# ax.set_ylabel('Voltage')
# ax.set_xlim(0,100)
# ax.set_ylim(-0.5,5000)
# lines = ax.plot([],[])[0]
# 
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().place(x = 10, y = 10, width = 500, height = 400)
# canvas.draw()


i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)
V = dac.raw_value
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xs=[]
ys=[]



def animate(i, xs, ys):
#    data = np.array([])
    xs = xs[-4095:]
    ys = ys[-4095:]
    xs.append(dt.datetime.now())
    ys.append(dac.raw_value)
    for i in range(4095, 0, -1):
        dac.raw_value = 2048 + int(2047*(math.sin(2*math.pi*i/4095)))
        print(dac.raw_value)
        #ax.clear()
        ax.plot(xs,ys)
        #plt.show()
    for i in range(0, 4095, 1):
        dac.raw_value = 2047 - int(2046*(math.sin(2*math.pi*i/4095)))
        print(dac.raw_value)
        #ax.clear()
        ax.plot(xs,ys) 
        #plt.show()
    


    
ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys))
plt.show()
         
         
         
        #time.sleep(0.0001)
#         if(len(data) <100):
#             data=np.append(data,dac.raw_value)
#             
#         else:
#             data[0:99] = data[1:100]
#             data[99] = dac.raw_value


#while True:
    
    
    

#             
        #lines.set_xdata(np.arange(0,len(data)))
        #lines.set_ydata(data)
        
#     plt.plot(np.arange(0,len(data)),data)
#     plt.show()
        #canvas.draw()
        

        #time.sleep(0.0001)
      