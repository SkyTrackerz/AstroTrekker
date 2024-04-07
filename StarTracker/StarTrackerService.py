import logging.config
from typing import Union, Type, List

from Location import Location
from Programs.Program import Program
from StarTracker.IStarTracker import IStarTracker
from config_logging import LOGGING_CONFIG


class StarTrackerService:
    StarTracker: IStarTracker = None
    Location: Location = None
    def __init__(self, star_tracker: IStarTracker, location: Location = None):
        StarTrackerService.StarTracker = star_tracker
        StarTrackerService.Location = location
        self.current_program: Program = None
        # Entry point of logging setup in project
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)
        #self.current_program.start()

    """    
    def start_manual_control_program(self):
        # program = ManualControlProgram(self.star_tracker)
        # self.start_program(program)
        pass

    def start_star_tracker_program(self, ):
        if self.location is None:
            raise NoLocationException()
        program = StarTrackProgram(StarTrackerService.StarTracker, self.location, "Jupiter")
        self.start_program(program)"""

    def start_programs(self, programs: List[Program]):
        if self.current_program is not None:
            self.logger.info(f'Stopping currently running program {self.current_program.__name__}')
            self.current_program.stop()
        self.logger.info(f"Starting programs {[program.__name__ for program in programs]}")

        # Check if 'program' is a subclass of Program
        if isinstance(program, type) and issubclass(program, Program):
            # Instantiate the program
            self.current_program = program(StarTrackerService.StarTracker)
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
        StarTrackerService.Location = location

class NoLocationException(Exception):
    pass
