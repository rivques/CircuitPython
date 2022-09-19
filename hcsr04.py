import time
import board

import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D2, echo_pin=board.D3) # initialize hc-sr04

import neopixel

led: neopixel.Neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2) # initialize neopixel

clamp = lambda value, minv, maxv: max(min(value, maxv), minv) # helps ensure that the distance is within expected range

def dist_to_color(distance):
    distance = clamp(distance, 5, 35)
    if distance < 20: # use the red-blue range
        r = map(distance, 5, 20, 255, 0)
        g = 0
        b = map(distance, 5, 20, 0, 255)
        return (r, g, b)
    else: # distance must be between 20 and 35 because of the clamp, so use the blue-green range
        r = 0
        g = map(distance, 20, 35, 0, 255)
        b = map(distance, 20, 35, 255, 0)
        return (r, g, b)

def map(x, in_min, in_max, out_min, out_max): # thanks arduino
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        try:
            distance = sonar.distance
        except RuntimeError: # if there's nothing in range
            time.sleep(0.1)
            continue
        color = dist_to_color(distance)
        print(f"Distance: {distance}, color: {color}")
        led.fill(color)
        time.sleep(0.1)
except KeyboardInterrupt: # gracefully exit from a stop command
    pass