from dataclasses import dataclass
from LimitSwitch.ILimitSwitch import ILimitSwitch
from typing import Optional

@dataclass
class MotorConfig:
    name: Optional[str]
    degrees_per_full_step: float
    microsteps_per_step: float
    max_angle: int
    step_pin: int
    enable_pin: Optional[int]
    direction_pin: int
    limit_switch: Optional[ILimitSwitch]
    forward_direction: bool
    gear_ratio: float = 1

    @property
    def degrees_per_step(self) -> float:
        """
        Calculate the degrees per step based on the degrees per full step,
        the number of microsteps per full step, and the gear ratio.
        """
        return (self.degrees_per_full_step / self.microsteps_per_step) / self.gear_ratio
