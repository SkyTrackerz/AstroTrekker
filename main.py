import config
from simulatedObservatory import SimulatedObservatory
from Programs.pan import Pan
from motor import Motor
import logging.config

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    # This is how you get the logger from any class
    logger = logging.getLogger(__name__)
    logger.log("Starting!")
    motorDriver1 = Motor(config.TURNTABLE)
    simOb = SimulatedObservatory(47.6061, -122.3328)
    panProgram = Pan(1, simOb)
  
    while 1:
        panProgram.run()
