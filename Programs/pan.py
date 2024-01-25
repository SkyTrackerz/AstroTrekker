from Programs.iprogram import Program
from time import sleep

from observatory import Observatory

class Pan(Program):
    def __init__(self, rate, observatory: Observatory):
        self.current_azimuth = 0
        self.current_altitude = 0
        self.observatory: Observatory = observatory
        self.rate = rate

        print("Intianted program")

    def run(self):
        self.observatory
        sleep(1)

        