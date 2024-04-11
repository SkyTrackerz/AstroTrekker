from threading import Event
from typing import Optional

from Motor.IMotor import IMotor


class MockMotor(IMotor):
    def __init__(self, config):
        self.config = config
        self.current_step = 0
        print("Mock motor initialized with config:", config)

    def limit_switch_callback(self):
        print("Mock limit switch callback triggered")

    @property
    def current_angle(self) -> float:
        return self.config.degrees_per_step * self.current_step

    def step_motor(self, steps: int, direction: bool, seconds_per_step: float = 1, check_limit=True, cancellation_event: Optional[Event] = None):
        print(f"Mock stepping {steps} steps in {'FORWARD' if direction else 'BACKWARD'} direction at {seconds_per_step} seconds per step")

    def go_to(self, angle: float, degrees_per_second=1, check_limit=True, cancellation_event: Optional[Event] = None):
        print(f"Mock going to angle {angle} at {degrees_per_second} degrees per second")

    def go_to_absolute(self, angle: float, degrees_per_second, check_limit=True, cancellation_event: Optional[Event] = None):
        print(f"Mock going to absolute angle {angle} at {degrees_per_second} degrees per second")

    def zero(self):
        print("Mock zeroing")

    @property
    def degrees_per_step(self) -> float:
        """
        Calculate the degrees per step based on the degrees per full step,
        the number of microsteps per full step, and the gear ratio.
        """
        return self.config.degrees_per_step
