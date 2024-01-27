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
        GPIO.setup(self.motor.enable_pin, GPIO.OUT)
        GPIO.setup(self.motor.limit_pin, GPIO.IN)
        # Initialize ENABLE pin
        GPIO.output(self.motor.enable_pin, GPIO.LOW)  # Enable the motor

        self.zero()
        self.current_pos = 0

    def step_motor(self, steps: int, direction: bool):
        steps = self._limit_in_range(steps, direction)
        # Set direction
        GPIO.output(self.motor.direction_pin, GPIO.HIGH if direction else GPIO.LOW)
        # Perform steps
        for _ in range(steps):
            GPIO.output(self.motor.step_pin, GPIO.HIGH)
            time.sleep(0.01)  # Adjust this delay for speed control
            GPIO.output(self.motor.step_pin, GPIO.LOW)

            self.current_pos += 1
            print('*', end='', flush=True)
            time.sleep(0.01)  # Adjust this delay for speed control

    def _limit_in_range(self, steps: int, direction: bool) -> int:
        # TODO: Wrap around
        if direction == FORWARD:
            return max(self.current_pos + steps, int(self.motor.max_angle * self.motor.degrees_per_step))
        return min(self.current_pos - steps, 0)

    def go_to(self, angle: float):
        self.step_motor(steps=self.motor.degrees_per_step * abs(angle),
                        direction=angle < 0)

    def zero(self):
        while not GPIO.input(self.motor.limit_pin):
            self.step_motor(1, BACKWARD)
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
