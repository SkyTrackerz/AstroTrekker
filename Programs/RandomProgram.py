from dataclasses import dataclass
from threading import Event
import random
from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService

@dataclass
class RandomProgramInput:
    max_alt: float
    max_az: float
    max_spin: float
    rate: float
    num_points: int

class RandomProgram(Program[RandomProgramInput]):
    Input = RandomProgramInput

    def __init__(self, input: RandomProgramInput):
        self.input = input
        super().__init__()

    def _get_random_point(self) -> tuple[float, float, float]:
        alt = random.uniform(0, self.input.max_alt)
        az = random.uniform(0, self.input.max_az)
        spin = random.uniform(0, self.input.max_spin)
        return alt, az, spin

    def execute(self, cancellation_event: Event) -> bool:
        for _ in range(self.input.num_points):
            if cancellation_event.is_set():
                return False

            alt, az, spin = self._get_random_point()
            
            StarTrackerService.StarTracker.go_to_absolute(
                altitude=alt,
                azimuth=az,
                spin=spin,
                degrees_per_second=self.input.rate,
                cancellation_event=cancellation_event
            )

        return True