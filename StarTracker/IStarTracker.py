from abc import ABC, abstractmethod


class IStarTracker(ABC):

    @abstractmethod
    def go_to(self, altitude, azimuth, degrees_per_second, cancellation_event=None):
        pass

    @abstractmethod
    def go_to_absolute(self, altitude, azimuth, degrees_per_second=10, cancellation_event=None):
        pass

