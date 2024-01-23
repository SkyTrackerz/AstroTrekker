class Program:
    def __init__(self, ob):
        self.current_ra = 0
        self.current_dec = 0
        self.observatory = ob

    # Uses time to calculate new position and request observatory to move there
    def run(self):
        pass