from typing import Tuple
from StarTracker.IStarTracker import IStarTracker


class MockStarTracker(IStarTracker):

    def __init__(self):
        self.altitude = 0
        self.azimuth = 0
        self.spin = 0
    
    def go_to(self, altitude, azimuth, spin, degrees_per_second, cancellation_event=None):
        self.altitude = altitude
        self.azimuth = azimuth
        self.spin = spin
        print(f"Mock go_to called with altitude={altitude}, azimuth={azimuth}, degrees_per_second={degrees_per_second}")

    
    def go_to_absolute(self, altitude, azimuth, spin, degrees_per_second=10, cancellation_event=None):
        self.altitude = altitude
        self.azimuth = azimuth
        self.spin = spin
        print(f"Mock go_to_absolute called with altitude={altitude}, azimuth={azimuth}, degrees_per_second={degrees_per_second}")

    def get_current_pos(self) -> Tuple[float,float,float]:
        return (self.altitude, self.azimuth, self.spin)
