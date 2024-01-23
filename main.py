from simulatedObservatory import SimulatedObservatory
from time import sleep
from Programs.pan import Pan    

if __name__ == '__main__':
    simOb = SimulatedObservatory(47.6061, -122.3328)
    panProgram = Pan(1, simOb)
  
    while(1):
        panProgram.run()
