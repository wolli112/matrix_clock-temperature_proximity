![IMG_8620](https://user-images.githubusercontent.com/103441220/162838043-0afe66b2-6abd-4815-b34e-df6322c48cc0.JPG)

# MicroPython - matrix clock which shows the time and temperature when approaching
My son gave me the idea for this project. He wanted a clock that he could put in his children's room without disturbing him with the light. The idea was born that the display only goes on when you approach the clock or approach it with your hand. The clock should show the time and the room temperature.

![ESP8266](https://user-images.githubusercontent.com/103441220/163267061-917eaa48-3666-42e4-8d0d-f1f5da3cb266.svg)

![IMG_4749](https://user-images.githubusercontent.com/103441220/163554693-3afe04eb-39d5-40c1-be71-572a3b8f5ae6.gif)

## Items:
NodeMCU V3 Module ESP8266 12F with MicroPython from http://micropython.org

MAX7219 4in1 Dot Matrix Display

HC-SR04 Ultrasonic Sensor

DS18B20 Sensor Breakout Modul

StepDown Converter with 3,3V output

3D Printed Case from https://www.thingiverse.com/thing:5350119

## Pinout:
### ESP8266
Data Pin DS18B20  on  GPIO 4  / D2

Trigger Pin SR04  on  GPIO 5  / D1

Echo Pin SR04     on  GPIO 16 / D0

CS Pin MAX7219    on  GPIO 2  / D4

CLK Pin MAX7219   on  GPIO 14 / D5

DIN Pin MAX7219   on  GPIO 13 / D7

#### To protect the ESP Pin from 5V, connected a step down converter (3,3 V) between Echo from SR04 and ESP Pin D0 !

## The following MicroPython modules are required, from these sources:
### MAX7219
https://github.com/mcauser/micropython-max7219 
### HS-SR04
https://github.com/rsc1975/micropython-hcsr04
### DS18B20
Module ds18x20 from MicroPython

## Construction:
The display is mounted on the front of the slot, the ESP on the back of the slot.
The slot with the display must be installed first, then the SR04 can be installed in the upper part.
The DS18B20 is installed in such a way that it looks out of the back of the case so that it can measure the room temperature.

![IMG_8691](https://user-images.githubusercontent.com/103441220/163554016-c8eed7f4-4fb4-4129-b5b4-5226ad99e38f.JPG)
![IMG_8692](https://user-images.githubusercontent.com/103441220/163554055-40b1870f-6681-447b-bac3-fa7344a66816.JPG)


## Instructions:

You can load the main.py directly onto your ESP. The wlan.py must also be loaded onto the ESP. The data of your WLAN must still be entered in the wlan.py .
