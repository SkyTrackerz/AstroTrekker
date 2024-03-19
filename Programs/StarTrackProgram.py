import time
from dataclasses import dataclass
from threading import Lock

from Location import Location
from Programs.Program import Program
from SkyCalculator import SkyCalculator

from starTracker import StarTracker

class StarTrackProgram(Program):
    """
    @param: star_tracker - The star tracker object to operate on
    @param: velocity - The speed to move the star tracker in, in degrees per second
    """
    def __init__(self, star_tracker: StarTracker, location: Location, planet_to_track='Jupiter'):
        self.star_tracker = star_tracker
        self.sky_calculator = SkyCalculator(location)
        self.planet_to_track = planet_to_track
        super().__init__()

    def execute(self):
        target = self.sky_calculator.planets[self.planet_to_track + ' Barycenter']
        target_alt, target_az = self.sky_calculator.get_local_alt_az(target)
        self.star_tracker.go_to_absolute(target_alt, target_az, degrees_per_second=1)


if __name__ == '__main__':
    class TestStarTracker()