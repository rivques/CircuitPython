import time
import analogio
import pwmio
import board
import digitalio

pot = analogio.AnalogIn(board.A0)
motor_pin = pwmio.PWMOut(board.D5)
photointerruptor = digitalio.DigitalInOut(board.D7)
photointerruptor.direction = digitalio.Direction.INPUT

def map(x, in_min, in_max, out_min, out_max): # thanks arduino
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class PIDController:
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.last_error = 0
        self.target_speed = 0
    
    def calculate(self, speed):
        error = self.target_speed - speed
        derivative = self.last_error - error
        result = self.kP * error + self.kD * derivative # no I control for now
        self.last_error = error
        return result

class MotorController:
    def __init__(self, motor_pin: pwmio.PWMOut, photo_pin: digitalio.DigitalInOut, pulses_per_rot: int):
        self.motor_pin = motor_pin
        self.photo_pin = photo_pin
        self.pulses_per_rot = pulses_per_rot
        self.last_photo_val = False
        self.last_measure_time = time.monotonic()
        self.num_ticks: int = 0

    
    def update(self):
        # call every loop to poll photointerruptor
        if self.photo_pin.value != self.last_photo_val:
            self.last_photo_val = self.photo_pin.value
            self.num_ticks += 1
    
    def get_speed(self):
        mins_since_last_measurement = (time.monotonic()-self.last_measure_time)/60
        self.last_measure_time = time.monotonic()
        rots_since_last_measurement = self.num_ticks/self.pulses_per_rot
        return rots_since_last_measurement/mins_since_last_measurement

motor = MotorController(motor_pin, photointerruptor, 5)

try:
    while True:
        print(f"Actual speed: {motor.get_speed()}")
except KeyboardInterrupt:
    pot.deinit()
    motor.deinit()
    photointerruptor.deinit()