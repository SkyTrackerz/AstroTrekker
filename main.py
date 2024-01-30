import config
from simulatedObservatory import SimulatedObservatory
from Programs.pan import Pan
from motorDriver import MotorDriver

if __name__ == '__main__':
    motorDriver1 = MotorDriver(config.TURNTABLE)
    simOb = SimulatedObservatory(47.6061, -122.3328)
    panProgram = Pan(1, simOb)
  
    while(1):
        panProgram.run()
