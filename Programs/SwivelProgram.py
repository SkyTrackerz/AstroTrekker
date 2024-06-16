from dataclasses import dataclass
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService


@dataclass
class SwivelProgramInput:
    degreesPerSec: float
    numSwivels: int
    degrees: int
class SwivelProgram(Program):
    Input=SwivelProgramInput
    def __init__(self, input: SwivelProgramInput):
        self.input = input
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        # TODO: Add cancellation logic
        degrees = min(180, self.input.degrees)
        for _ in range(self.input.numSwivels):
            StarTrackerService.StarTracker.go_to_absolute(0,degrees,self.input.degreesPerSec, cancellation_event)
            StarTrackerService.StarTracker.go_to_absolute(0,180-degrees,self.input.degreesPerSec, cancellation_event)
        return True