from Programs.program import Program
from time import sleep

from observatory import Observatory

class Pan(Program):
    def __init__(self, rate, ob: Observatory):
        super().__init__(ob)
        
        print("Intianted program")
        self.rate = rate

    def run(self):
        self.observatory.
        sleep(1)

        