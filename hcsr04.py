import time
import board

import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D2, echo_pin=board.D3)

import neopixel

led: neopixel.Neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

COLORS = [
    {"range": 5, "color": 0},
    {"range": 20, "color": 240},
    {"range": 35, "color": 120}
]

clamp = lambda value, minv, maxv: max(min(value, maxv), minv)

def dist_to_color(distance):
    min_color = {}
    max_color = {}
    distance = clamp(distance, COLORS[0]["range"], COLORS[len(COLORS)-1]["range"])
    for color in COLORS:
        if distance >= color["range"]:
            min_color = color
            break # stop at the first color whose range is less than our distance
    else:
        min_color = COLORS[0] # no color has a small enough range, so use the smallest one
    for color in reversed(COLORS):
        if distance <= color["range"]:
            max_color = color
            break #stop at the first color whose range is larger than ours
    else:
        max_color = COLORS[len(COLORS)-1]  # no color has a big enough range, so use the biggest one
    print(distance, min_color["range"], max_color["range"], min_color["color"], max_color["color"])
    return map(distance, min_color["range"], max_color["range"], min_color["color"], max_color["color"])

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def hsv_to_rgb(  # pylint: disable=too-many-return-statements,inconsistent-return-statements
    hue: float, sat: float, val: float
):
    if sat == 0.0:
        return val, val, val
    i = int(hue * 6.0)  # assume int() truncates!
    hue1 = (hue * 6.0) - i
    chroma1 = val * (1.0 - sat)
    chroma2 = val * (1.0 - sat * hue1)
    chroma3 = val * (1.0 - sat * (1.0 - hue1))
    i = i % 6
    if i == 0:
        return int(val * 255), int(chroma3 * 255), int(chroma1 * 255)
    if i == 1:
        return int(chroma2 * 255), int(val * 255), int(chroma1 * 255)
    if i == 2:
        return int(chroma1 * 255), int(val * 255), int(chroma3 * 255)
    if i == 3:
        return int(chroma1 * 255), int(chroma2 * 255), int(val * 255)
    if i == 4:
        return int(chroma3 * 255), int(chroma1 * 255), int(val * 255)
    if i == 5:
        return int(val * 255), int(chroma1 * 255), int(chroma2 * 255)
try:
    while True:
        try:
            distance = sonar.distance
        except RuntimeError:
            time.sleep(0.1)
            continue
        hue = dist_to_color(distance)
        color = hsv_to_rgb(hue, 1, 1)
        print(f"Distance: {distance}, hue: {hue}, color: {color}")
        led.fill(color)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass