from Programs.program import Program
from time import sleep

class Pan(Program):
    def __init__(self, rate, ob):
        super().__init__(ob)
        
        print("Intianted program")
        self.rate = rate

    def run(self):
        sleep(1)

        