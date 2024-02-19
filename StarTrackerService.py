from Programs.program import IProgram
from starTracker import StarTracker


class StarTrackerService:
    def __init__(self, motorController: StarTracker):
        self.motorController = motorController
        self.current_program=None

    def set_program(self, program: IProgram):
        if self.current_program is not None:
            self.current_program.stop()
        self.current_program = program
        self.current_program.run()