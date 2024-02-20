import Motor
from MotorConfig import MotorConfig
from LimitSwitch.LimitSwitch import LimitSwitch

TURNTABLE = MotorConfig(
    degrees_per_full_step=1.8,
    microsteps_per_step=16,
    gear_ratio=60 / 18,
    step_pin=32,
    enable_pin=None,
    direction_pin=22,
    max_angle=300,
    limit_switch=LimitSwitch(pin=10),
    forward_direction=Motor.BACKWARD
)

TURRET = MotorConfig(
    degrees_per_full_step=1.8,
    microsteps_per_step=16,
    step_pin=36,
    enable_pin=None,
    direction_pin=24,
    max_angle=300,
    #limit_switch=KeyboardLimitSwitch(key='k'),
    limit_switch=LimitSwitch(pin=10),
    forward_direction=Motor.FORWARD
)

SPIN = MotorConfig(
    degrees_per_full_step=1.8,
    microsteps_per_step=16,
    step_pin=26,
    enable_pin=None,
    direction_pin=18,
    max_angle=300,
    limit_switch=LimitSwitch(pin=10),
    #limit_switch=KeyboardLimitSwitch(key='l'),
    forward_direction=Motor.FORWARD
)

zero_degrees_per_sec=5