# CircuitPython
Fooling around with various CircuitPython features on a Metro M4 Airlift Lite.
# Assignments
## `neopixel.py`
A basic test of the M4's onboard NeoPixel. Flashes through off, red, green, and blue.
### Assignment
For this assignment, we just had to make the onboard neopixel change colors.
### Media
![The project in action](/docs/neopixel.gif)
### Reflection
This assignment was just a test to make sure that everything was runing correctly. While there was an optional assignment to make the NeoPixel rainbow, I chose not to do it because I wanted to move on to the other assignments.
## `servo.py`, `internet_servo.py`
A basic servo motor control test and a website to control a servo.
### Assignment
For this assignment, we had to make a servo sweep across its length. There was an option make the servo controllable with capacitive touch, but because the new boards we are using do not support that natively (instead requiring a supplemental 1MOhm resistor) I decided to make the servo controllable over the internet instead.
### Circuitry
Servo|Metro
---|----
Power|5V
Signal|D7
Ground|Ground
### Media
![The project in action](/docs/internet-servo.gif)
### Reflection
I ran into a bit of trouble making the servo cross its full range of motion. It turns out that the servos we have need a slightly wider pulse range than default. This was a good exercise in troubleshooting. 
## `hcsr04.py`
Fades the onboard NeoPixel through different colors depending on the distance detected by an ultrasonic sensor.
### Assignment
For this assignment, we had to make the NeoPixel on board the Metro change color according to the following diagram:

![A labeled color gradient](/docs/color%20spectrum.png)
### Circuitry
HC-SR04|Metro
---|---
Vcc|5V
Trig|D2
Echo|D3
Gnd|Ground
### Media
![The project in action](/docs/hc-sr04.gif)
### Reflection
Originally, I tried to make a method that was very easy to extend and modify, but it ended up taking too much time for a non-functional product. I pivoted to doing it the easy-to-write, hard-to-modify way and finished it in no time.
## `lcd.py`, `internet_lcd.py`
Allows control of a pair of LCD screens over a website
### Assignment
For this assignment, we had to make 1 or 2 LCD screens display a count that was controllable by some input method. I wanted to test my internet code, so I chose to control it over IoT.
### Circuitry
LCD-A (address 0x27)|LCD-B (address 0x3F)|Metro
---|---|---
SDA|SDA|SDA
SCL|SCL|SCL
VCC|VCC|5V
GND|GND|GND
### Media
![The project in action](/docs/IoT-LCD.gif)
### Reflection
This went of relatively easily because of how adaptable my internet code is. I'm very proud of how simple it is to drop it into a new application and be up and running with only a few lines of code. I was also able to use a test bench I made last year to quickly detect the address of any given LCD screen, so it was nice to be able to reuse an old project as a useful time saver.

# Experiments
## `helloworld.py`
A basic test of CircuitPython installation.
## `internet.py`
Hosts a webpage that lets you control the onboard LED.
## `adafruitio*.py`
Various experiments with adafruitio instead of self-hosting a webpage.
## `ble*.py`, `ancs.py`
Experiments with the Airlift's Bluetooth. Haven't been able to get this working.
