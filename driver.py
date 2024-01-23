import RPi.GPIO as GPIO
import time

class StepperMotorDriver:
    def __init__(self):
        # GPIO pin numbers
        self.STEP_PIN = 32
        self.ENABLE_PIN = 24
        self.DIR_PIN = 26

        # Setup
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN, GPIO.OUT)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)

        # Initialize ENABLE pin

    def step_motor(self, steps, direction):
        GPIO.output(self.ENABLE_PIN, GPIO.HIGH)  # Enable the motor
        # Set direction
        GPIO.output(self.DIR_PIN, GPIO.HIGH if direction == 'forward' else GPIO.LOW)

        # Perform steps
        for _ in range(steps):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            time.sleep(0.01)  # Adjust this delay for speed control
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            print('*', end='', flush=True)
            time.sleep(0.01)  # Adjust this delay for speed control


    def __del__(self):
        # Clean up
        GPIO.cleanup()

# Example usage
motor = StepperMotorDriver()
while True:
    print("moving forward")
    motor.step_motor(10, 'forward')  # Steps the motor forward 100 steps
    print("pausing 3 seconds")
    time.sleep(3)
    print("moving backward")
    motor.step_motor(10, 'backward')  # Steps the motor backward 50 steps
