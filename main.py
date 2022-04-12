'''
MicroPython - matrix clock which shows the time and temperature when approaching
https://github.com/wolli112/matrix_clock-temperature_proximity

MIT License

Copyright (c) 2022 wolli112

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
__version__ = '0.1'
__author__ = 'wolli112'

# Import the required modules
from machine import Pin, SPI
import network
import utime
import ntptime
import max7219
from hcsr04 import HCSR04
import time
import onewire
import ds18x20
from wlan import * # Import the data of the WLAN connection

# Timezone offset 2= Summertime; 1= Wintertime
timezone_hour = 2  # (hours)

# DS18B20 definition
ds = 4 
ds_pin = Pin(ds)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin)) 

# SR04 definition
trig = 5
echo = 16
sensor = HCSR04(trigger_pin=trig, echo_pin=echo, echo_timeout_us=10000)

# MAX7219 Matrix definition 
din = 13
cs = 2
clk = 14
DISPLAY_BRIGHTNESS = 1

spi = SPI(1, baudrate=10000000, polarity=1, phase=0)
display = max7219.Matrix8x8(spi, Pin(cs), 4)
display.brightness(DISPLAY_BRIGHTNESS)

# Function to establish the network connection
def connect_network():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid,passwort)

    while station.isconnected() == False:
        pass

    print('Connection Network successful')

# Function for calculating and formatted display of the current, local time on the matrix display
def time_display():
    local_time_sec = utime.time() + timezone_hour * 3600
    local_time = utime.localtime(local_time_sec)
    mask = "{3:02d}{4:02d}"
    output = mask.format(*local_time)
    display.fill(0)
    display.text(output, 0, 0, 1)
    display.pixel(16,2,1)
    display.pixel(16,5,1)
    display.show()
    time.sleep(0.5)
    display.pixel(16,2,0)
    display.pixel(16,5,0)
    display.show()
    
# Temperature display function
def temp_display():
    display.fill(0)
    display.text(str(temp), 0, 0, 1)
    display.show()
        
# Temperature recall function
def temperatur():
    global temp
    roms = ds_sensor.scan() #Scan from Onewire 
    #print('Found DS devices: ', roms) # Output of the connected sensors

    ds_sensor.convert_temp() # Collect temperature values
    time.sleep_ms(750)
    for rom in roms:
        #print(rom)
        #print(ds_sensor.read_temp(rom)) # Read and output temperature
        temp = ds_sensor.read_temp(rom)
    return temp

# Start of ESP8266

# Start of network connection
try:
    connect_network()

except OSError as e:
    print("Network connection is not possible")

# Mainprogramm
display.fill(0)  # Display clean
display.show()

while True:
    data = []
    for x in range(2):
            dataread = sensor.distance_cm()
            if dataread > 2.0:
                data.append(dataread)
                time.sleep(0.25)
    #print(data)
    if len(data) == 0:  # Query and catch empty list - avoid division by 0
        continue
    
    else:
            distance = sum(data)/len(data)
            #print(distance)
            
            if distance < 60:
                #print("Display an")
                
                try:
                    ntptime.settime()   # Update time - only necessary if RTC is not running properly
                    temperatur()
                    #print(temp)
                    for y in range(3):  # Range for displaying the time in seconds
                        time_display()
                        time.sleep(1)
                    for z in range(1):  # Range for displaying the temperature in seconds
                        temp_display()
                        time.sleep(1)
                       
                except OSError as e:
                    print("NTP Error")
                    machine.reset()     # Reboot of ESP on NTP Error
                       
            else:
                display.fill(0)
                display.show()
                


