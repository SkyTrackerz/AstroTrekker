import config
from motor import Motor
from MotorConfig import MotorConfig
import time


class ObservatoryCalculator:
    def __init__(self, turntable: MotorConfig, turret: MotorConfig, spin: MotorConfig):
        self._targetTurntableAngle = 0
        self._targetTurretAngle = 0
        self._targetPivotAngle = 0

        self._observatoryAltitude = 0
        self._observatoryAzimuth = 0

        self.turntableConfig = turntable
        self.turretConfig = turret
        self.spinConfig = spin

        self.turntable = Motor(turntable)
        self.turret = Motor(turret)
        self.spin = Motor(spin)

        # Position data given by star tracker GPS and magnetometer:
        self._compassHeading = 0 # deg around a comapss (dead N)

    # Called by program to update observatory to new star position (this function calls _calculate_target_configuration and _move)
    def go_to(self, altitude, azimuth):
        # Calculate observatory altitude and azimuth based on orientation of observatory
        self._observatoryAltitude = altitude
        self._observatoryAzimuth = azimuth - self._compassHeading

        # Calculate what that means for the observatory in terms of joints
        self._calculate_target_configuration()

        # Command the motors to move
        self._move()
        
    # Uses geometry of observatory to calculate the corresponding position of all joints
    def _calculate_target_configuration(self):
        self._targetTurntableAngle = self._observatoryAzimuth
        self._targetTurretAngle = self._observatoryAltitude

    # Actually command the motors to move 
    def _move(self):
        self.turntable.go_to(self._targetTurntableAngle)
        self.turret.go_to(self._targetTurretAngle)

if __name__ == '__main__':
    observatory = ObservatoryCalculator(config.TURNTABLE, config.TURRET, config.SPIN)
    
    for i in range(3):
        for j in range(4):
            ObservatoryCalculator.goto(45 * i, 90 * j)
            time.sleep(1)