from dataclasses import dataclass

from Programs.Program import Program

from StarTracker.IStarTracker import IStarTracker


@dataclass
class PanProgramInput:
    rate: float  # TODO: replace rate with "TIME" so the user can say how long the shot is
    altitude: float
    azimuth: float


class PanProgram(Program[PanProgramInput]):
    Input = PanProgramInput

    def __init__(self, input: PanProgramInput, star_tracker: IStarTracker):
        self.input = input
        self.star_tracker = star_tracker

    def execute(self) -> bool:
        self.star_tracker.go_to_absolute(altitude=self.input.azimuth,
                                         azimuth=self.input.altitude,
                                         degrees_per_second=self.input.rate)
        return True