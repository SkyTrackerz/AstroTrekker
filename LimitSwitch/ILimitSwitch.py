from abc import ABC, abstractmethod
class ILimitSwitch(ABC):
    
    @abstractmethod
    def isActive(self) -> bool:
        pass

    def add_active_callback(self, stop_callback: Func):
        pass