import config
from Motor.Motor import Motor
from Motor.TurntableMotor import TurntableMotor
import time
turntable = TurntableMotor(config.TURNTABLE)
turret = Motor(config.TURRET)
spin = Motor(config.SPIN)

while True:
    if turret.limit_switch.isActive(): print("turret active")
    if turntable.limit_switch.isActive(): print("turntable active")
    if spin.limit_switch.isActive(): print("spin active")
