import logging
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
        self.program_i = 0
        self.logger = logging.getLogger(__name__)
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        # Log here
        # Log all program names in the list
        program_names = [p.__class__.__name__ for p in self.programs]
        self.logger.info(f"All programs: {', '.join(program_names)}")        
        program = self.programs[self.program_i % len(self.programs)]
                # Log the currently executing program, its index, and the total list of programs
        self.logger.info(f"Executing {program.__class__.__name__} (index: {self.program_i}, total programs: {len(self.programs)})")
        # Run the next program on the same thread
        is_done = program.execute(cancellation_event)
        if is_done:
            self.program_i += 1
        #return self.program_i >= len(self.programs)
        return False
