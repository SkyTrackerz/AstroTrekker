from Motor.MockMotor import MockMotor
from StarTracker.MockStarTracker import MockStarTracker
#from StarTracker.StarTracker import StarTracker
from StarTracker.StarTrackerService import StarTrackerService
from webapp.webapp import WebApp

#mockTurntable, mockTurret, mockSpin = MockMotor(), MockMotor(), MockMotor()
#starTracker = StarTracker(mockTurntable, mockTurret, mockSpin)
starTracker = MockStarTracker()

starTrackerService = StarTrackerService(starTracker)
webapp = WebApp(starTrackerService)
webapp.run()
