import adafruit_mcp4725
import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725,MCP4725(i2c, address=0x60)

while True:
    for i in range(0,4095):
        dac.raw_value = i
        print(i)
        time.sleep(0.002)
    
    for i in range (4095,0,-1):
        dac.raw_value=i
        print(i)
        time.sleep(0.002) 