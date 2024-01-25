from typing import Tuple

from skyfield.api import N, W, wgs84, load
from skyfield.toposlib import GeographicPosition
from skyfield.units import Angle

from environment import Environment


class SkyCalculator:

    """
    If elevation is not provided, SRTM data is used
    """
    def __init__(self, lat: float, long: float, elev=None):
        # Import planets
        planets = load('de421.bsp')
        earth = planets['earth']
        if elev is not None:
            if Environment.has_internet:
                # TODO: Get elevation here
                pass
        # Define current location
        self.loc: GeographicPosition = earth + wgs84.latlon(lat, long)

    def get_local_alt_az(self, target) -> Tuple[Angle, Angle]:
        # Get current time from skyfield
        ts = load.timescale()
        t = ts.now()
        print(t.tt_strftime())

        # Observe target object
        astronomic = self.loc.at(t).observe(target)
        alt, az, dist = astronomic.apparent().altaz()

        print(alt)
        print(az)
        return alt, az
