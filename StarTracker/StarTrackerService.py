import logging.config
from typing import Union, Type, List

from Location import Location
from Programs.MultiProgram import MultiProgramInput, MultiProgram
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
        if not StarTrackerService.StarTracker.zeroed:
            StarTrackerService.StarTracker.zero()

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

    def start_programs(self, programs: List[Program]) -> None:
        if len(programs) == 0:
            return
        if self.current_program is not None and not self.current_program.is_done:
            self.logger.info(f'Stopping currently running program {type(self.current_program).__name__}')
            self.current_program.stop()
        if len(programs) == 1:
            self.current_program = programs[0]
            self.logger.info(f"Starting program {type(self.current_program).__name__}")
        else:
            self.logger.info(f"Starting MultiProgram of {[type(program).__name__ for program in programs]}")
            self.current_program = MultiProgram(MultiProgramInput(programs=programs))
        self.current_program.start()

    def cancel_program(self):
        if self.current_program:
            self.logger.info(f"Stopping current program {self.current_program.__class__.__name__}")
            self.current_program.stop()

    # TODO: come up with generic way to send commands to programs
    async def send_joystick_command(self, x, y):
        # if isinstance(self.current_program, ManualControlProgram):
        #    self.current_program.handle_command(DirectionCommand(x, y))
        # else:
        #    print("Not a manual control command! ")
        pass

    def set_location(self, location: Location):
        StarTrackerService.Location = location


class NoLocationException(Exception):
    pass
