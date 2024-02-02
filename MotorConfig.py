from dataclasses import dataclass
from LimitSwitch.ILimitSwitch import ILimitSwitch


@dataclass
class MotorConfig:
    degrees_per_step: float
    max_angle: int
    step_pin: int
    enable_pin: int
    direction_pin: int
    limit_switch: ILimitSwitch
