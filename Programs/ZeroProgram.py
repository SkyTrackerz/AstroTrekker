import logging
from dataclasses import dataclass
from threading import Event

from Programs.Program import Program
from StarTracker.StarTrackerService import StarTrackerService


@dataclass
class ZeroProgramInput:
    rate: float  # TODO: replace rate with "TIME" so the user can say how long the shot is


class ZeroProgram(Program[ZeroProgramInput]):
    Input = ZeroProgramInput

    def __init__(self, input: ZeroProgramInput):
        self.input = input
        self.logger = logging.getLogger(__name__)
        super().__init__()

    def execute(self, cancellation_event: Event) -> bool:
        self.logger.info(f"Starting zero program")
        StarTrackerService.StarTracker.zero()
        return True
