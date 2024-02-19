from abc import ABC, abstractmethod
from typing import Callable


class ILimitSwitch(ABC):
    
    @abstractmethod
    def isActive(self) -> bool:
        pass

    def add_active_callback(self, stop_callback: Callable):
        pass