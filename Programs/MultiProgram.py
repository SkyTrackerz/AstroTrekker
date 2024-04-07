from dataclasses import dataclass
from threading import Event
from typing import List

from Programs.Program import Program

@dataclass
class MultiProgramInput:
    programs: List[Program]
class MultiProgram(Program[MultiProgramInput]):
    Input = MultiProgramInput

    def __init__(self, input: MultiProgramInput):
        assert len(input.programs) > 0, "Must provide at least one program"
        self.programs = input.programs
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        program = self.programs[0]
        # Run the next program on the same thread
        is_done = program.execute(cancellation_event)
        if is_done:
            self.programs.pop(0)
        return len(self.programs) > 0
