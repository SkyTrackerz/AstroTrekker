from Motor.IMotor import IMotor
from Motor.MotorConfig import MotorConfig
from LimitSwitch.LimitSwitch import LimitSwitch

TURNTABLE = MotorConfig(
    name="TURNTABLE",
    degrees_per_full_step=1.8,
    microsteps_per_step=1,
    gear_ratio=160 / 15,
    step_pin=11,
    enable_pin=16,
    direction_pin=36,
    max_angle=360,
    #limit_switch=LimitSwitch(pin=10),
    limit_switch=None,
    forward_direction=IMotor.BACKWARD
)

TURRET = MotorConfig(
    name="TURRET",
    degrees_per_full_step=1.8,
    microsteps_per_step=16,
    gear_ratio=100 / 16,
    step_pin=13,
    enable_pin=26,
    direction_pin=38,
    max_angle=270,
    limit_switch=LimitSwitch(pin=31),
    #limit_switch=KeyboardLimitSwitch(key='k'),
    forward_direction=IMotor.FORWARD
)

SPIN = MotorConfig(
    name="SPIN",
    degrees_per_full_step=1.8,
    microsteps_per_step=1,
    gear_ratio=100 / 17,
    step_pin=15,
    enable_pin=None,
    direction_pin=40,
    max_angle=300,
    #limit_switch=LimitSwitch(pin=10),
    limit_switch=None,
    #limit_switch=KeyboardLimitSwitch(key='l'),
    forward_direction=IMotor.FORWARD
)

zero_degrees_per_sec=5