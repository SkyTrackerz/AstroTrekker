from abc import ABC
from dataclasses import dataclass

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService
from skyCalculator import SkyCalculator


@dataclass
class StarTrackProgramInput:
    bodyToTrack: str


class StarTrackProgram(Program[StarTrackProgramInput]):
    Input = StarTrackProgramInput

    def __init__(self, input: Input):
        self.sky_calculator = SkyCalculator(StarTrackerService.Location)
        self.sky_calculator.set_target(input.bodyToTrack)
        super().__init__()

    def execute(self) -> bool:
        target_alt, target_az = self.sky_calculator.get_local_alt_az()
        StarTrackerService.StarTracker.go_to_absolute(target_alt, target_az, degrees_per_second=1)
        return True
