import asyncio
import os
from pathlib import Path

import pandas as pd
from typing import Tuple, Union

from skyfield.api import N, W, wgs84, load
from skyfield.starlib import Star
from skyfield.toposlib import GeographicPosition
from skyfield.units import Angle
from skyfield.data import hipparcos
from environment import Environment
import logging

STORAGE_DIR_PATH = 'Storage/Astronomy'

class SkyCalculator:

    """
    If elevation is not provided, SRTM data is used
    """
    def __init__(self, lat: float, long: float, elev=None):
        self.load_astro_data()
        # Import planets
        self.earth = self.planets['earth']
        # Define current location
        self.loc: GeographicPosition = self.earth + wgs84.latlon(lat, long)
        self.target = None
        self.star_df = None
        logging.basicConfig(level=logging.WARNING)
    def set_target(self, target: Union[str, int]) -> bool:
        if target in self.planets:
            self.target = self.planets[target]
            return True
        if target in self.star_df.index:
            self.target = Star.from_dataframe(self.star_df.loc[target])
            return True
        return False

        
    def get_local_alt_az(self) -> Tuple[Angle, Angle]:
        # Get current time from skyfield
        ts = load.timescale()
        t = ts.now()

        # Observe target object
        astronomic = self.loc.at(t).observe(self.target)
        alt, az, dist = astronomic.apparent().altaz()

        return alt, az

    def load_astro_data(self):
        astro_data_dir = Environment.get_project_root() / STORAGE_DIR_PATH
        self.planets = load('de421.bsp', astro_data_dir)
        hippa_filepath = astro_data_dir / 'hipparcos_data.csv'

        if asyncio.run(Environment.check_internet()):
            with load.open(hipparcos.URL) as f:
                self.star_df = hipparcos.load_dataframe(f)
                self.star_df.to_csv(hippa_filepath)
                logging.info("Loaded and saved star data from internet")
        elif os.path.exists(hippa_filepath):
            # Load df from file
            self.star_df = pd.read_csv(hippa_filepath)
            logging.info("Using cached star data")
        else:
            # Log a warning if the file is not found
            logging.error(
                f"The file {hippa_filepath} does not exist. Please ensure you have an internet connection to download the data.")
# Find the project root
def find_project_root(relative_path=''):
    current = Path(__file__).parent  # Start from the current file location
    while current != current.parent:
        if current.joinpath(relative_path).exists():  # Check if the marker exists at this level
            return current
        current = current.parent
    return current  # Fallback to the current directory if nothing is found

class AstroNotFoundException(Exception):
    pass

if __name__ == '__main__':
    pass