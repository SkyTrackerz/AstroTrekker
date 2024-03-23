from abc import ABC

from Location import Location
from Programs.Program import Program
from StarTracker.IStarTracker import IStarTracker
from skyCalculator import SkyCalculator


class StarTrackProgram(Program, ABC):
    """
    @param: star_tracker - The star tracker object to operate on
    @param: velocity - The speed to move the star tracker in, in degrees per second
    """

    def __init__(self, star_tracker: IStarTracker, location: Location, planet_to_track='Jupiter'):
        self.star_tracker = star_tracker
        self.sky_calculator = SkyCalculator(location)
        self.sky_calculator.set_target("Jupiter")
        super().__init__()

    def execute(self) -> bool:
        target_alt, target_az = self.sky_calculator.get_local_alt_az()
        self.star_tracker.go_to_absolute(target_alt, target_az, degrees_per_second=1)
        return True
