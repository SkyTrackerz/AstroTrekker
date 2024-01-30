import RPi.GPIO as GPIO
import time

from Motor import Motor

BACKWARD = False
FORWARD = not BACKWARD

class MotorDriver:
    def __init__(self, motor: Motor):
        self.motor = motor
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.motor.step_pin, GPIO.OUT)
        GPIO.setup(self.motor.direction_pin, GPIO.OUT)
        if self.motor.enable_pin:
            GPIO.setup(self.motor.enable_pin, GPIO.OUT)
            GPIO.output(self.motor.enable_pin, GPIO.LOW)  # Enable the motor
        GPIO.setup(self.motor.step_pin, GPIO.IN)
        # Initialize ENABLE pin
        self.current_pos = 0
        self.zero()

    def step_motor(self, steps: int, direction: bool, seconnds_per_step=1, check_limit=True):
        if check_limit:
            steps = self._limit_in_range(steps, direction)
        # Set direction
        GPIO.output(self.motor.direction_pin, GPIO.HIGH if direction else GPIO.LOW)
        # Perform steps
        for _ in range(steps):
            GPIO.output(self.motor.step_pin, GPIO.HIGH)
            GPIO.output(self.motor.step_pin, GPIO.LOW)
            self.current_pos += 1
            time.sleep(seconnds_per_step)  # Adjust this delay for speed control

    def _limit_in_range(self, steps: int, direction: bool) -> int:
        max_steps = int(self.motor.max_angle * self.motor.degrees_per_step)

        if direction == FORWARD:
            potential_pos = self.current_pos + steps
            if potential_pos <= max_steps:
                return steps
            else:
                return max_steps - self.current_pos
        else:
            potential_pos = self.current_pos - steps
            if potential_pos >= 0:
                return steps
            else:
                return self.current_pos

    def go_to(self, angle: float, degrees_per_second=1, check_limit=True):
        seconds_per_step = self.motor.degrees_per_step / degrees_per_second
        # TODO: rounding errors?
        self.step_motor(steps=int(abs(angle) / self.motor.degrees_per_step),
                        direction=angle < 0, seconnds_per_step=seconds_per_step, check_limit=check_limit)

    def zero(self):
        print('zeroing')
        while not GPIO.input(self.motor.limit_pin):
            self.step_motor(10, BACKWARD, rate=0.2, check_limit=False)
        self.current_pos = 0

    def __del__(self):
        # Clean up
        GPIO.cleanup()


if __name__ == '__main__':
    # Example usage
    motor = MotorDriver()
    while True:
        print("moving forward")
        motor.step_motor(10, True)  # Steps the motor forward 10 steps
        print("pausing 3 seconds")
        time.sleep(3)
        print("moving backward")
        motor.step_motor(10, False)  # Steps the motor backward 10 steps
        print("moving 90 degrees forward")
        motor.go_to(90)
        print("moving 90 degrees backward")
        motor.go_to(-90)
