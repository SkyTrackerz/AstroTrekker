from skyfield.api import N, W, wgs84, load


class SkyCalculator:

    def __init__(self, lat: float, long: float):
        # Import planets
        planets = load('de421.bsp')
        earth = planets['earth']

        # Define current location
        self.loc = earth + wgs84.latlon(lat, long)

    def get_alt_az(self, target):
        # Get current time from skyfield
        ts = load.timescale()
        t = ts.now()
        print(t.tt_strftime())

        # Observe target object
        astronomic = self.loc.at(t).observe(target)
        alt, az, d = astronomic.apparent().altaz()

        print(alt)
        print(az)
