import config
from Motor.MockMotor import MockMotor
from StarTracker.MockStarTracker import MockStarTracker
from StarTracker.StarTracker import StarTracker
from StarTracker.StarTrackerService import StarTrackerService
from webapp.webapp import WebApp
import cryptography

mockTurntable, mockTurret, mockSpin = MockMotor(config.TURNTABLE), MockMotor(config.TURRET), MockMotor(config.SPIN)
starTracker = StarTracker(mockTurntable, mockTurret, mockSpin)
starTrackerService = StarTrackerService(starTracker)
webapp = WebApp(starTrackerService)
webapp.run()
