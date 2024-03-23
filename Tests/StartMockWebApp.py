from StarTracker.MockStarTracker import MockStarTracker
from StarTracker.StarTrackerService import StarTrackerService
from webapp.webapp import WebApp
import cryptography

mockStarTracker = MockStarTracker()
starTrackerService = StarTrackerService(mockStarTracker)
webapp = WebApp(starTrackerService)
webapp.run()
