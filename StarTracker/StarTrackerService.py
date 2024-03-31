from typing import Union, Type

from Location import Location
from Programs.Program import Program
import Programs.ManualControlService as ManualControlService
from Programs.StarTrackProgram import StarTrackProgram
from StarTracker.IStarTracker import IStarTracker


class StarTrackerService:
    def __init__(self, star_tracker: IStarTracker, location: Location = None):
        self.star_tracker = star_tracker
        self.current_program: Program = None
        self.location = location
        #self.current_program.start()

    def start_manual_control_program(self):
        # program = ManualControlProgram(self.star_tracker)
        # self.start_program(program)
        pass

    def start_star_tracker_program(self):
        if self.location is None:
            raise NoLocationException()
        program = StarTrackProgram(self.star_tracker, self.location, "Jupiter")
        self.start_program(program)

    def start_program(self, program: Union[Type[Program], Program]):
        if self.current_program is not None:
            self.current_program.stop()

        # Check if 'program' is a subclass of Program
        if isinstance(program, type) and issubclass(program, Program):
            # Instantiate the program
            self.current_program = program(self.star_tracker)
        elif isinstance(program, Program):
            # Set the program directly if it's an instance of Program
            self.current_program = program
        else:
            raise TypeError("Invalid program type")

        self.current_program.start()

    # TODO: come up with generic way to send commands to programs
    async def send_joystick_command(self, x, y):
        #if isinstance(self.current_program, ManualControlProgram):
        #    self.current_program.handle_command(DirectionCommand(x, y))
        #else:
        #    print("Not a manual control command! ")
        pass

    def set_location(self, location: Location):
        self.location = location


class NoLocationException(Exception):
    pass
