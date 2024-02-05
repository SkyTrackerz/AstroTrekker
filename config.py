import motor
from MotorConfig import MotorConfig
from LimitSwitch.LimitSwitch import LimitSwitch
from LimitSwitch.KeyboardLimitSwitch import KeyboardLimitSwitch
TURNTABLE = MotorConfig(
    degrees_per_step=1.8 / 4,
    step_pin=36,
    enable_pin=None,
    direction_pin=24,
    max_angle=300,
    limit_switch=LimitSwitch(pin=10),
    forward_direction=motor.BACKWARD
)

TURRET = MotorConfig(
    degrees_per_step=1.8,
    step_pin=32,
    enable_pin=None,
    direction_pin=22,
    max_angle=300,
    limit_switch=KeyboardLimitSwitch(key='k'),
    forward_direction=motor.FORWARD
)

SPIN = MotorConfig(
    degrees_per_step=1.8,
    step_pin=26,
    enable_pin=None,
    direction_pin=18,
    max_angle=300,
    limit_switch=KeyboardLimitSwitch(key='l'),
    forward_direction=motor.FORWARD
)

zero_degrees_per_sec=5