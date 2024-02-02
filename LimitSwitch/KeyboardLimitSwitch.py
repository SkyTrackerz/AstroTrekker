from ILimitSwitch import ILimitSwitch
import keyboard

class KeyboardLimitSwitch(ILimitSwitch):
    def __init__(self, key: str = "L"):
        self.key = key
    
    def isActive(self) -> bool:
        return keyboard.is_pressed(self.key)