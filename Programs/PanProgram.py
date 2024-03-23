from Programs.Program import Program
from time import sleep

from StarTracker.StarTracker import Observatory

class PanProgram(Program):
    def __init__(self, rate, observatory: Observatory):
        self.current_azimuth = 0
        self.current_altitude = 0
        self.observatory: Observatory = observatory
        self.rate = rate

        print("Intianted program")

    def run(self):
        sleep(1)

        