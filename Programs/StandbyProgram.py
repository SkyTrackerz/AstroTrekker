import time
from dataclasses import dataclass

from Programs.Program import Program


@dataclass
class StandbyProgramInput:
    minutes: float


class StandbyProgram(Program):
    Input = StandbyProgramInput

    def __init__(self, input: StandbyProgramInput):
        self.input = input
        pass

    def execute(self) -> bool:
        time.sleep(self.input.minutes * 60)
