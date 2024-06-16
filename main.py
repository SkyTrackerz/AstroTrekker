import logging.config


import config
from StarTracker.StarTrackerService import StarTrackerService
from StarTracker.StarTracker import StarTracker
from Motor.Motor import Motor
from webapp.webapp import WebApp
import argparse

if __name__ == '__main__':

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Start the Flask application')
    parser.add_argument('--debug', action='store_true', help='Enable remote debugger')
    args = parser.parse_args()

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)
    logger.info("Starting!")


    if args.debug:
        logger.info("Remote debugger is enabled.")

    star_tracker = StarTracker(
        turntable=Motor(config.TURNTABLE),
        turret=Motor(config.TURRET),
        spin=Motor(config.SPIN)
    )

    star_tracker_service = StarTrackerService(star_tracker)
    webapp = WebApp(star_tracker_service)
    webapp.run()
