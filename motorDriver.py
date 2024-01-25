import RPi.GPIO as GPIO
import time

from Motor import Motor


class MotorDriver:
    def __init__(self, motor: Motor):
        self.motor = motor
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.motor.step_pin, GPIO.OUT)
        GPIO.setup(self.motor.direction_pin, GPIO.OUT)
        GPIO.setup(self.motor.enable_pin, GPIO.OUT)

        # Initialize ENABLE pin
        GPIO.output(self.motor.enable_pin, GPIO.LOW)  # Enable the motor

    def step_motor(self, steps, direction: bool):
        # Set direction
        GPIO.output(self.motor.direction_pin, GPIO.HIGH if direction else GPIO.LOW)

        # Perform steps
        for _ in range(steps):
            GPIO.output(self.motor.step_pin, GPIO.HIGH)
            time.sleep(0.01)  # Adjust this delay for speed control
            GPIO.output(self.motor.step_pin, GPIO.LOW)
            print('*', end='', flush=True)
            time.sleep(0.01)  # Adjust this delay for speed control

    def go_to(self, angle: float):
        self.step_motor(steps=self.motor.degrees_per_step * abs(angle),
                        direction=angle < 0)

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
