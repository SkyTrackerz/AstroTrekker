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
    def calculate_target_configuration(self, targetAzimuth, targetAltitude):
        # Use offset from North to calculate device-relative angles
        # Fill in compass heading
        pass

    # Actually command the picture/motors to move 
    def move(self):
        pass

    

