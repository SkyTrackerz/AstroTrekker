import logging.config

import config
from Motor import Motor
from StarTracker.StarTrackerService import StarTrackerService
from StarTracker.StarTracker import StarTracker
from webapp.webapp import WebApp

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    # This is how you get the logger from any class
    logger = logging.getLogger(__name__)
    logger.info("Starting!")

    star_tracker = StarTracker(
        turntable=Motor(config.TURNTABLE),
        turret=Motor(config.TURRET),
        spin=Motor(config.SPIN)
    )
    star_tracker_service = StarTrackerService(star_tracker)
    webapp = WebApp(star_tracker_service)
    webapp.run()
