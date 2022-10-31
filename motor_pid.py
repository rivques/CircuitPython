import time
import analogio
import pwmio
import board
import digitalio
import countio
import asyncio

pot = analogio.AnalogIn(board.A0)
motor_pin = pwmio.PWMOut(board.D5)

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
    def __init__(self, motor_pin: pwmio.PWMOut, photo_pin, pulses_per_rot: int):
        self.motor_pin = motor_pin
        self.photo_pin = photo_pin
        self.pulses_per_rot = pulses_per_rot
        self.last_photo_val = False
        self.last_measure_time = time.monotonic()
        self.num_ticks: int = 0
        self.last_ticks: int = 0
        self.current_speed = 0

    
    async def update(self):
        # call every loop to poll photointerruptor
        with countio.Counter(self.photo_pin, pull=digitalio.Pull.UP) as interrupt:
            while True:
                if interrupt.count > 0:
                    self.num_ticks += interrupt.count
                    interrupt.count = 0
                # Let another task run.
                await asyncio.sleep(0)
    
    def update_speed(self):
        mins_since_last_measurement = (time.monotonic()-self.last_measure_time)/60
        self.last_measure_time = time.monotonic()
        rots_since_last_measurement = (self.num_ticks-self.last_ticks)/self.pulses_per_rot
        self.last_ticks = self.num_ticks
        self.current_speed =  rots_since_last_measurement/mins_since_last_measurement
    
    def set_duty_cycle(self, new_duty_cycle):
        self.motor_pin.duty_cycle = new_duty_cycle

motor = MotorController(motor_pin, board.D7, 5)
motorPID = PIDController(50,0,0)
async def display_info():
    while True:
        target_speed = map(pot.value, 0, 65535, 0, 6000)
        motorPID.target_speed = target_speed
        motor_speed = motor.current_speed
        print(f"{motor_speed}, {motor.motor_pin.duty_cycle}, {target_speed}")
        await asyncio.sleep(0.1)

async def update_motor_pid():
    while True:
        motor.update_speed()
        motor.set_duty_cycle(motorPID.calculate(motor.current_speed))
        await asyncio.sleep(0.1)

async def main():
    motor_update_task = asyncio.create_task(motor.update())
    print_speed_task = asyncio.create_task(display_info())
    update_motor_duty_cycle_task = asyncio.create_task(update_motor_pid())
    await asyncio.gather(motor_update_task, print_speed_task, update_motor_duty_cycle_task)

asyncio.run(main())