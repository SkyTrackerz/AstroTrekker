from dataclasses import dataclass

@dataclass
class Motor:
    degrees_per_step: float
    max_angle: int
    step_pin: int
    enable_pin: int
    direction_pin: int
    limit_pin: int
