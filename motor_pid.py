
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

class PDController:
    def __init__(self, kP, kD):
        self.kP = kP
        self.kD = kD
        self.last_error = 0
        self.target_speed = 0
    
    def calculate(self, speed):
        error = self.target_speed - speed
        derivative = self.last_error - error
        result = self.kP * error + self.kD * derivative 
        self.last_error = error
        return max(min(int(result), 65535), 0) # cast to int and clamp to useable duty cycles

class Tick:
    def __init__(self, tick_time: int, num: int):
        self.time: int = tick_time
        self.num: int = num
    
    def __repr__(self) -> str:
        return f"(t:{self.time}, c:{self.num})"


class MotorController:
    def __init__(self, motor_pin: pwmio.PWMOut, photo_pin, pulses_per_rot: int):
        self.motor_pin = motor_pin
        self.photo_pin = photo_pin
        self.ticks_per_rot = pulses_per_rot
        self.last_photo_val = False
        self.last_measure_time = time.monotonic_ns()
        self.ticks = []
        self.current_speed = 0

    
    async def update(self):
        # call every loop to poll photointerruptor
        with countio.Counter(self.photo_pin, pull=digitalio.Pull.UP) as interrupt:
            while True:
                if interrupt.count > 0:
                    self.ticks.append(Tick(time.monotonic_ns(), interrupt.count))
                    interrupt.count = 0
                # Let another task run.
                await asyncio.sleep(0)
    
    def update_speed(self):
        self.cull_ticks()
        if len(self.ticks) <= 1:
            self.current_speed =  0
            return
        avg_ns_between_ticks = (sum([self.ticks[i+1].time - self.ticks[i].time for i in range(len(self.ticks)-1)])/len(self.ticks))
        #print(avg_ns_between_ticks)
        self.current_speed =  1_000_000_000 / (self.ticks_per_rot * avg_ns_between_ticks) # rps, see https://www.motioncontroltips.com/what-type-of-encoder-can-be-used-to-measure-speed/

    def cull_ticks(self):
        BUFFER_LEN = 100_000_000 # ns
        now = time.monotonic_ns()
        try:
            while now - self.ticks[0].time > BUFFER_LEN:
                self.ticks.pop(0)
        except IndexError:
            # we emptied the list
            pass
    
    def set_duty_cycle(self, new_duty_cycle: int):
        self.motor_pin.duty_cycle = new_duty_cycle

motor = MotorController(motor_pin, board.D7, 5)
motorPD = PDController(5000,1)
async def display_info():
    while True:
        target_speed = max(map(pot.value, 1000, 65535, 0, 120), 0) # the pot doesn't hit 0 so have a deadzone
        motorPD.target_speed = target_speed
        print(f"{target_speed - motor.current_speed}, {motor.current_speed}, {motor.motor_pin.duty_cycle}, {target_speed}")
        await asyncio.sleep(0.1)

async def update_motor_pid():
    while True:
        motor.update_speed()
        motor.set_duty_cycle(motorPD.calculate(motor.current_speed))
        await asyncio.sleep(0.01)

async def main():
    motor_update_task = asyncio.create_task(motor.update())
    display_info_task = asyncio.create_task(display_info())
    update_motor_duty_cycle_task = asyncio.create_task(update_motor_pid())
    await asyncio.gather(motor_update_task, display_info_task, update_motor_duty_cycle_task)

asyncio.run(main())