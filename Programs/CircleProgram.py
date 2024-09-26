from dataclasses import dataclass
from threading import Event
from typing import List
from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService
import math

@dataclass
class CircleProgramInput:
    center_alt: float
    center_az: float
    radius: float
    num_points: int
    rate: float

class CircleProgram(Program[CircleProgramInput]):
    Input = CircleProgramInput

    def __init__(self, input: CircleProgramInput):
        self.input = input
        self.points: List[tuple[float, float]] = self._calculate_circle_points()
        super().__init__()

    def _calculate_circle_points(self) -> List[tuple[float, float]]:
        points = []
        for i in range(self.input.num_points):
            angle = 2 * math.pi * i / self.input.num_points
            alt = self.input.center_alt + self.input.radius * math.sin(angle)
            az = self.input.center_az + self.input.radius * math.cos(angle)
            points.append((alt, az))
        return points

    def execute(self, cancellation_event: Event) -> bool:
        for alt, az in self.points:
            if cancellation_event.is_set():
                return False
            
            StarTrackerService.StarTracker.go_to_absolute(
                altitude=alt,
                azimuth=az,
                spin=0,
                degrees_per_second=self.input.rate,
                cancellation_event=cancellation_event
            )

        return True