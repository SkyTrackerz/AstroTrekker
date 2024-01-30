from Motor import Motor

TURNTABLE = Motor(
    degrees_per_step=1.8 / 4,
    step_pin=36,
    enable_pin=None,
    direction_pin=24,
    max_angle=300,
    limit_pin=16
)

TURRET = Motor(
    degrees_per_step=1.8,
    step_pin=32,
    enable_pin=None,
    direction_pin=22,
    max_angle=300,
    limit_pin=16
)

SPIN = Motor(
    degrees_per_step=1.8,
    step_pin=26,
    enable_pin=None,
    direction_pin=18,
    max_angle=300,
    limit_pin=16
)