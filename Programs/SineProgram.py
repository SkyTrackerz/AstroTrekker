from dataclasses import dataclass
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService


@dataclass
class SineProgramInput:
    degreesPerSec: float
    radius: float
class SineProgram(Program):
    Input=SineProgramInput
    def __init__(self, input: SineProgramInput):
        self.input = input
        # lets say move 1 degree at a time
        center_x, center_y = 180, 
        self.alt_path=[]
        #self.path = StarTrackerService.StarTracker.
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        # TODO: Add cancellation logic
        for _ in range(self.input.numSwivels):
            StarTrackerService.StarTracker.go_to_absolute(0,0,self.input.degreesPerSec, cancellation_event)
            StarTrackerService.StarTracker.go_to_absolute(0,180,self.input.degreesPerSec, cancellation_event)
        return True