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
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

# get an i2c object
i2c = board.I2C()

# some LCDs are 0x3f... some are 0x27.
# but now i'm tsting new backpacks with addresses 0x20-27!
lcdA = Character_LCD_I2C(i2c, 16, 2, 0x20)
lcdANum = 0

lcdB = Character_LCD_I2C(i2c, 16, 2, 0x21)
lcdBNum = 0

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


@web_app.route("/a-offset/<offset>") # a request here changes lcd A by the requested offset
def offset(request, offset):  # pylint: disable=unused-argument
    global lcdANum
    print("A offset!")
    lcdANum += int(offset)
    printToLcd(lcdA, int(offset), lcdANum)
    return ("200 OK", [], "A changed!")


@web_app.route("/b-offset/<offset>") # a request here changes lcd B by the requested offset
def offset(request, offset):  # pylint: disable=unused-argument
    global lcdBNum
    print("B offset!")
    lcdBNum += int(offset)
    printToLcd(lcdB, int(offset), lcdBNum)
    return ("200 OK", [], "B changed!")


@web_app.route("/") # the homepage
def index(request):
    print("index!")
    with open("lib/static/lcd_index.html") as f: # collect the file into one big string
        print("getting HTML...")
        html =  ''.join(f.readlines())
    print("got HTML")
    return("200 OK", [], html)


# Here we setup our server, passing in our web_app as the application
server.set_interface(esp)
wsgiServer = server.WSGIServer(80, application=web_app)

print("open this IP in your browser: ", esp.pretty_ip(esp.ip_address))

def printToLcd(lcd, offset, lcdNum):
    lcd.clear()
    lcd.message = str(lcdNum)
    lcd.cursor_position(15,1)
    lcd.message = ("+" if offset > 0 else "-")

# print(esp.get_time())
printToLcd(lcdA, 1, lcdANum)
printToLcd(lcdB, 1, lcdBNum)
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