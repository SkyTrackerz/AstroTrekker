from dataclasses import dataclass
from LimitSwitch.ILimitSwitch import ILimitSwitch
from typing import Optional

@dataclass
class MotorConfig:
    degrees_per_step: float
    max_angle: int
    step_pin: int
    enable_pin: Optional[int]
    direction_pin: int
    limit_switch: Optional[ILimitSwitch]
    forward_direction: bool
