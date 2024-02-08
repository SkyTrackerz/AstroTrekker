import logging
import logging.config

import config
from .ILimitSwitch import ILimitSwitch
import RPi.GPIO as GPIO
from typing import Callable


class LimitSwitch(ILimitSwitch):
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.logger = logging.getLogger(__name__)

    def isActive(self) -> bool:
        value = GPIO.input(self.pin)
        # print(f'Limit Switch value: {GPIO.input(self.pin)}')
        # self.logger.info()
        return value

    def add_active_callback(self, stop_callback: Callable):
        pass

if __name__ == '__main__':
    logging.basicConfig()
    switch = LimitSwitch(config.TURNTABLE.limit_switch.pin)
    while True:
        switch.isActive()
