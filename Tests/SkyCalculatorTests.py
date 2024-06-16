import unittest
from unittest.mock import patch
from SkyCalculator import SkyCalculator

class TestSkyCalculator(unittest.TestCase):

    @patch('environment.Environment.has_internet', True)
    def test_initialization_with_internet(self):
        """
        Test initialization with internet access, expecting stars data to be loaded.
        """
        # Assuming internet access, the star data should be loaded.
        calculator = SkyCalculator(0, 0)  # Use equator coordinates as an example
        self.assertIsNotNone(calculator.star_df, "Star DataFrame should not be None with internet access.")

    @patch('environment.Environment.has_internet', False)
    def test_initialization_without_internet(self):
        """
        Test initialization without internet access but with a local file present.
        """
        calculator = SkyCalculator(0, 0)
        self.assertIsNotNone(calculator.star_df, "Star DataFrame should be loaded from a file if it exists.")

    def test_set_target_planet(self):
        """
        Test setting a planetary target.
        """
        calculator = SkyCalculator(0, 0)
        result = calculator.set_target('mars')  # Example with Mars
        self.assertTrue(result, "Setting a planetary target should return True.")
        self.assertIsNotNone(calculator.target, "Setting target should set Target field")
        alt, az = calculator.get_local_alt_az()
        self.assertIsNotNone(alt, "Getting altitude should return value")
        self.assertIsNotNone(az, "Getting azimuth should return value")

    def test_set_target_star(self):
        """
        Test setting a planetary target.
        """
        calculator = SkyCalculator(0, 0)
        result = calculator.set_target(320)  # Example with Mars
        self.assertTrue(result, "Setting a planetary target should return True.")
        self.assertIsNotNone(calculator.target, "Setting target should set Target field")
        alt, az = calculator.get_local_alt_az()
        self.assertIsNotNone(alt, "Getting altitude should return value")
        self.assertIsNotNone(az, "Getting azimuth should return value")


if __name__ == '__main__':
    unittest.main()
