# CircuitPython
Fooling around with various CircuitPython features on a Metro M4 Airlift Lite.
# Assignments
## `neopixel.py`
A basic test of the M4's onboard NeoPixel. Flashes through off, red, green, and blue.
### Assignment
For this assignment, we just had to make the onboard neopixel change colors.
### Code
The code is available at </neopixel.py>. For the sake of space it will not be pasted in full here.
### Media
![The project in action](/docs/neopixel.gif)
### Reflection
This assignment was just a test to make sure that everything was runing correctly. While there was an optional assignment to make the NeoPixel rainbow, I chose not to do it because I wanted to move on to the other assignments. I felt I could accomplish more interesting things this way.
## `servo.py`, `internet_servo.py`
A basic servo motor control test and a website to control a servo.
### Assignment
For this assignment, we had to make a servo sweep across its length. There was an option make the servo controllable with capacitive touch, but because the new boards we are using do not support that natively (instead requiring a supplemental 1MOhm resistor) I decided to make the servo controllable over the internet instead.
### Code
The code is available at </servo.py> and </internet_servo.py>. For the sake of space it will not be pasted in full here.
### Circuitry
![The circuitry](/docs/servocircuit.png)
### Media
![The project in action](/docs/internet-servo.gif)
### Reflection
I ran into a bit of trouble making the servo cross its full range of motion. It turns out that the servos we have need a slightly wider pulse range than default. This was a good exercise in troubleshooting and learning from documentation. 
## `hcsr04.py`
Fades the onboard NeoPixel through different colors depending on the distance detected by an ultrasonic sensor.
### Assignment
For this assignment, we had to make the NeoPixel on board the Metro change color according to the following diagram:

![A labeled color gradient](/docs/color%20spectrum.png)
### Code
The code is available at </hcsr04.py>. For the sake of space it will not be pasted in full here.
### Circuitry
![The circuitry](/docs/hcsr04circuit.png)
### Media
![The project in action](/docs/hc-sr04.gif)
### Reflection
Originally, I tried to make a method that was very easy to extend and modify, but it ended up taking too much time for a non-functional product. I pivoted to doing it the easy-to-write, hard-to-modify way and finished it in no time. Sometimes this is a necessary sacrifice to make but it requires knowledge of the future uses of the project.
## `lcd.py`, `internet_lcd.py`
Allows control of a pair of LCD screens over a website
### Assignment
For this assignment, we had to make 1 or 2 LCD screens display a count that was controllable by some input method. I wanted to test my internet code, so I chose to control it over IoT.
### Code
The code is available at </lcd.py> and </internet_lcd.py>. For the sake of space it will not be pasted in full here.
### Circuitry
![The circuitry](/docs/lcdcircuit.png)
### Media
![The project in action](/docs/IoT-LCD.gif)
### Reflection
This went of relatively easily because of how adaptable my internet code is. I'm very proud of how simple it is to drop it into a new application and be up and running with only a few lines of code. I was also able to use a test bench I made last year to quickly detect the address of any given LCD screen, so it was nice to be able to reuse an old project as a useful time saver.

# Experiments (not assigned, these just happen to live here)
## `helloworld.py`
A basic test of CircuitPython installation.
## `internet.py`
Hosts a webpage that lets you control the onboard LED.
## `adafruitio*.py`
Various experiments with adafruitio instead of self-hosting a webpage.
## `ble*.py`, `ancs.py`
Experiments with the Airlift's Bluetooth. Haven't been able to get this working.
