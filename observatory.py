from math import radians
from operator import mod

from skyCalculator import SkyCalculator
from skyfield.api import load

class Observatory:
    def __init__(self, lattitude, longitude):
        self.targetTurntableAngle = 0
        self.targetTrackAngle = 0
        self.targetPivotAngle = 0

        self.skyCalc = SkyCalculator(lattitude, longitude)

        # Position data given by star tracker GPS and magnetometer:
        self.lattitude = 38.891329768
        self.longitude = -77.070166386
        self.compassHeading = 62.78 # deg around a comapss (NE)

    # Called by program to update observatory to new star position
    def update(self, targetAzimuth, targetAltitude):
        pass

    # Uses geometry of observatory to calculate the corresponding position of all joints
    def calculate_target_configuration(self, target):
        # Use offset from North to calculate device-relative angles

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
        pass

    # Actually command the picture/motors to move 
    def move(self):
        pass

    

