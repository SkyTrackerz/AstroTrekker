from StarTracker.IStarTracker import IStarTracker


class MockStarTracker(IStarTracker):
    def go_to(self, altitude, azimuth, degrees_per_second, cancellation_event=None):
        print(f"Mock go_to called with altitude={altitude}, azimuth={azimuth}, degrees_per_second={degrees_per_second}")

    def go_to_absolute(self, altitude, azimuth, degrees_per_second=10, cancellation_event=None):
        print(f"Mock go_to_absolute called with altitude={altitude}, azimuth={azimuth}, degrees_per_second={degrees_per_second}")