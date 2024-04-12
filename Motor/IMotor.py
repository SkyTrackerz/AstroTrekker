from abc import ABC, abstractmethod
from threading import Event
from typing import Optional


class IMotor(ABC):
    BACKWARD = False
    FORWARD = not BACKWARD
    @abstractmethod
    def limit_switch_callback(self):
        pass

    @property
    @abstractmethod
    def current_angle(self) -> float:
        pass

    @abstractmethod
    def step_motor(self, steps: int, direction: bool, seconds_per_step: float = 1, check_limit=True,
                   cancellation_event: Optional[Event] = None):
        pass

    @abstractmethod
    def go_to(self, angle: float, degrees_per_second=1, check_limit=True, cancellation_event: Optional[Event] = None):
        pass

    @abstractmethod
    def go_to_absolute(self, angle: float, degrees_per_second, check_limit=True,
                       cancellation_event: Optional[Event] = None):
        pass

    @abstractmethod
    def zero(self):
        pass

    @abstractmethod
    def degrees_per_step(self):
        pass
