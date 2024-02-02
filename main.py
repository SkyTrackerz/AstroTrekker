import config
from simulatedObservatory import SimulatedObservatory
from Programs.pan import Pan
from motor import Motor

if __name__ == '__main__':
    motorDriver1 = Motor(config.TURNTABLE)
    simOb = SimulatedObservatory(47.6061, -122.3328)
    panProgram = Pan(1, simOb)
  
    while(1):
        panProgram.run()
