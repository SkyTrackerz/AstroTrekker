import time
from dataclasses import dataclass
from threading import Event

from Programs.Program import Program


@dataclass
class StandbyProgramInput:
    minutes: float


class StandbyProgram(Program[StandbyProgramInput]):
    Input = StandbyProgramInput

    def __init__(self, input: StandbyProgramInput):
        self.input = input
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        # TODO: Add cancellation logic
        time.sleep(self.input.minutes * 60)
        return True