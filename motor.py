import time
import analogio
import pwmio
import board

pot = analogio.AnalogIn(board.A0)
motor = pwmio.PWMOut(board.D5)


def map(x, in_min, in_max, out_min, out_max): # thanks arduino
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        motor_speed = pot.value # both of these values are 16 bit so no mapping is needed
        print(f"Speed: {motor_speed}")
        motor.duty_cycle = motor_speed
except KeyboardInterrupt:
    pot.deinit()
    motor.deinit()