import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from secrets import secrets
import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
import neopixel
from adafruit_wsgi.wsgi_app import WSGIApp
from adafruit_motor import servo
import pwmio

status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
) # a status light for the wifi connection
pwm = pwmio.PWMOut(board.D7, duty_cycle=2 ** 15, frequency=50) # the pwm object for the servo

my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500) #custom pulse lengths because our servos are *special*

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO) # comms w/ esp32
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except (RuntimeError, ConnectionError) as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

socket.set_interface(esp) # use the esp32 instead of the default (non-existent) builtin wifi
requests.set_socket(socket, esp)

web_app = WSGIApp()


@web_app.route("/servo/<angle>") # a request here sets the servo to the rquested angle
def led_on(request, angle):  # pylint: disable=unused-argument
    print("servo set!")
    my_servo.angle = int(angle)
    return ("200 OK", [], "servo on!")


@web_app.route("/") # the homepage
def index(request):
    print("index!")
    with open("lib/static/servo_index.html") as f: # collect the file into one big string
        print("getting HTML...")
        html =  ''.join(f.readlines())
    print("got HTML")
    return("200 OK", [], html)


# Here we setup our server, passing in our web_app as the application
server.set_interface(esp)
wsgiServer = server.WSGIServer(80, application=web_app)

print("open this IP in your browser: ", esp.pretty_ip(esp.ip_address))

# print(esp.get_time())
# Start the server
wsgiServer.start()
while True:
    # Our main loop where we have the server poll for incoming requests
    try:
        wsgiServer.update_poll()
        # Could do any other background tasks here, like reading sensors
    except (ValueError, RuntimeError) as e:
        print("Failed to update server, restarting ESP32\n", e)
        esp.reset()
        continue