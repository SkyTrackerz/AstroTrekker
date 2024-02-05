from .ILimitSwitch import ILimitSwitch
import keyboard
import logging.config
import logging

#TODO: This doesnt work on linux without root
class KeyboardLimitSwitch(ILimitSwitch):
    def __init__(self, key: str = "L"):
        self.key = key
    
    def isActive(self) -> bool:
        return keyboard.is_pressed(self.key)

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)
    switch = KeyboardLimitSwitch()
    while True:
        logger.debug(switch.isActive())