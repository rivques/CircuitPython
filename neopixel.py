import time
import board

import neopixel

led: neopixel.Neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
print("neopixel")

led.brightness = 0.3

while True:
    print("starting loop")
    led[0] = (255, 0, 0)
    time.sleep(0.5)
    led[0] = (0, 255, 0)
    time.sleep(0.5)
    led[0] = (0, 0, 255)
    time.sleep(0.5)
    led[0] = (0, 0, 0)
    time.sleep(0.5)