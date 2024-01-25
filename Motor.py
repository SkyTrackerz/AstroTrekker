from dataclasses import dataclass


@dataclass
class Motor:
    degrees_per_step: float
    step_pin: int
    enable_pin: int
    direction_pin: int
