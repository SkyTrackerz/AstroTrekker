from skyCalculator import SkyCalculator
from simulatedObservatory import SimulatedObservatory
from skyfield.api import load
from time import sleep

if __name__ == '__main__':
    skyCalc = SkyCalculator(38.891329768, -77.070166386)

    planets = load('de421.bsp')
    mars = planets['mars']
    skyCalc.get_alt_az(mars)

    simOb = SimulatedObservatory()

    sleep(5)
    simOb.update_target_angles(0.3, 0, 0)
    simOb.update()
    print("Rotated turntable")

    sleep(5)
    simOb.update_target_angles(0.6, 0, 0)
    simOb.update()
    print("Rotated turntable")
