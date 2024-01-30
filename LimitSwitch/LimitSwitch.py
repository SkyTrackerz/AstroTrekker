from ILimitSwitch import ILimitSwitch
import RPi.GPIO as GPIO
class LimitSwitch(ILimitSwitch):
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(pin, GPIO.IN)
    
    def isActive(self) -> bool:
        return GPIO.input(self.motor.limit_pin)