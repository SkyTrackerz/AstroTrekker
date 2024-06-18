import time
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService, NoLocationException
from SkyCalculator import SkyCalculator


@dataclass
class StarTrackProgramInput:
    bodyToTrack: str
    timeMultiplier: int

class StarTrackProgram(Program[StarTrackProgramInput]):
    Input = StarTrackProgramInput

    def __init__(self, input: Input):
        if StarTrackerService.Location is None:
            raise NoLocationException("Location must be set to Star Track")
        self.sky_calculator = SkyCalculator(StarTrackerService.Location)
        self.sky_calculator.set_target(input.bodyToTrack)
        self.time_gen = accelerated_time_generator(input.timeMultiplier)
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        target_alt, target_az = self.sky_calculator.get_local_alt_az(next(self.time_gen))
        print(f"Going to star coord {target_alt, target_az}")
        StarTrackerService.StarTracker.go_to_absolute(target_alt.degrees, target_az.degrees,
                                                      degrees_per_second=20,
                                                      cancellation_event=cancellation_event)
        # TODO: check if time has passed
        # returning "not done"
        return False


def accelerated_time_generator(multiplier):
    start_time = datetime.now(timezone.utc)
    start_real_time = time.time()
    while True:
        elapsed_real_time = time.time() - start_real_time
        accelerated_time = start_time + timedelta(seconds=elapsed_real_time * multiplier)
        yield accelerated_time
