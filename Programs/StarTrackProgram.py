from abc import ABC
from dataclasses import dataclass

from Location import Location
from Programs.Program import Program
from StarTracker.IStarTracker import IStarTracker
from skyCalculator import SkyCalculator

@dataclass
class StarTrackProgramInput:
    bodyToTrack: str

class StarTrackProgram(Program):
    Input = StarTrackProgramInput

    def __init__(self, star_tracker: IStarTracker, location: Location, planet_to_track='Jupiter'):
        self.star_tracker = star_tracker
        self.sky_calculator = SkyCalculator(location)
        self.sky_calculator.set_target("Jupiter")
        super().__init__()

    def execute(self) -> bool:
        target_alt, target_az = self.sky_calculator.get_local_alt_az()
        self.star_tracker.go_to_absolute(target_alt, target_az, degrees_per_second=1)
        return True
