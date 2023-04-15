# rgb_led.py --- RGB LED test

from common.device.ws2812 import WS2812

import machine
import time

power = machine.Pin(11,machine.Pin.OUT)
power.value(1)

led = WS2812(12,1)#WS2812(pin_num,led_count)

r = int(input('Red  (0-255):'))
g = int(input('Green(0-255):'))
b = int(input('Blue (0-255):'))

color = (r,g,b)
led.pixels_fill(color)
led.pixels_show()

