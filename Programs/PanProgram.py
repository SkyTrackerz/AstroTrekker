from dataclasses import dataclass
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService


@dataclass
class PanProgramInput:
    rate: float  # TODO: replace rate with "TIME" so the user can say how long the shot is
    altitude: float
    azimuth: float


class PanProgram(Program[PanProgramInput]):
    Input = PanProgramInput

    def __init__(self, input: PanProgramInput):
        self.input = input
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        StarTrackerService.StarTracker.go_to_absolute(altitude=self.input.azimuth,
                                                      azimuth=self.input.altitude,
                                                      degrees_per_second=self.input.rate,
                                                      cancellation_event=cancellation_event)
        return True
