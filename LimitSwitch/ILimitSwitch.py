from abc import ABC, abstractmethod

class ILimitSwitch(ABC):
    
    @abstractmethod
    def isActive(self) -> bool:
        pass