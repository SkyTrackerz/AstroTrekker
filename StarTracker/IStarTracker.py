from abc import ABC, abstractmethod
from typing import Tuple


class IStarTracker(ABC):

    def __init__(self):
        self.zeroed = None

    @abstractmethod
    def go_to(self, altitude, azimuth, spin, degrees_per_second, cancellation_event=None):
        pass

    @abstractmethod
    def go_to_absolute(self, altitude, azimuth, spin, degrees_per_second=10, cancellation_event=None):
        pass

    @abstractmethod
    def get_current_pos(self) -> Tuple[float,float,float]:
        pass

    @abstractmethod
    def zero(self):
        pass
