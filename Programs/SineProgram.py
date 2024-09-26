from dataclasses import dataclass
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService


@dataclass
class SineProgramInput:
    numXSwivels: int
    numYSwivels: int
    rate: float

class SineProgram(Program[SineProgramInput]):
    Input=SineProgramInput
    def __init__(self, input: SineProgramInput):
        self.input = input
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        minAlt = 10
        maxAlt = 80
        minAz = 0
        maxAz = 180
        startY = 0
        xMovePerSwiv = (maxAz - minAz) / self.input.numYSwivels
        for x_i in range(self.input.numXSwivels):
            for y_i in range(self.input.numYSwivels):
                targetAlt = minAlt if y_i % 2 == 0 else maxAlt
                targetAz = y_i * xMovePerSwiv
                targetAz = targetAz if x_i % 2 == 0 else maxAz - targetAz
                StarTrackerService.StarTracker.go_to_absolute(altitude=targetAlt,
                                              azimuth=targetAz,
                                              spin=0,
                                              degrees_per_second=self.input.rate,
                                              cancellation_event=cancellation_event)
        return True