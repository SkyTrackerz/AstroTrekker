from math import radians
from operator import mod
import config  
from motorDriver import MotorDriver
from Motor import Motor
import time

from skyCalculator import SkyCalculator
from skyfield.api import load

class ObservatoryCalculator:
    def __init__(self, turntable: Motor, turret: Motor, spin: Motor):
        self._targetTurntableAngle = 0
        self._targetTurretAngle = 0
        self._targetPivotAngle = 0

        self._observatoryAltitude = 0
        self._observatoryAzimuth = 0

        self.turntableConfig = turntable
        self.turretConfig = turret
        self.spinConfig = spin

        self.turntable = MotorDriver(turntable)
        self.turret = MotorDriver(turret)
        self.spin = MotorDriver(spin)

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






""""# Use offset from North to calculate device-relative angles

        # Get the local altitude and azimuth relative to the observer
        local_azimuth, local_altitude = self.skyCalc.get_local_alt_az(target)
        # Adjust azimuth for observer's heading
        adjusted_azimuth = mod(local_azimuth - observer_heading, 360)

        # Convert to radians for calculations
        azimuth_rad = radians(adjusted_azimuth)
        altitude_rad = radians(local_altitude)
        pitch_rad = radians(device_pitch)
        roll_rad = radians(device_roll)

        # Apply rotation matrix here for pitch and roll
        # This is a simplified version and might need refinement
        x = cos(altitude_rad) * sin(azimuth_rad)
        y = cos(altitude_rad) * cos(azimuth_rad)
        z = sin(altitude_rad)

        # Apply pitch (rotation around y-axis)
        x_prime = x * cos(pitch_rad) - z * sin(pitch_rad)
        z_prime = x * sin(pitch_rad) + z * cos(pitch_rad)
        x, z = x_prime, z_prime

        # Apply roll (rotation around x-axis)
        y_prime = y * cos(roll_rad) - z * sin(roll_rad)
        z = y * sin(roll_rad) + z * cos(roll_rad)
        y = y_prime

        # Convert back to azimuth and altitude
        final_azimuth_rad = arctan2(x, y)
        final_altitude_rad = arctan2(z, sqrt(x ** 2 + y ** 2))

        final_azimuth = degrees(final_azimuth_rad)
        final_altitude = degrees(final_altitude_rad)
        """