import asyncio
from threading import Event
from typing import Tuple
import config
from motor import Motor
from MotorConfig import MotorConfig
import time


class StarTracker:
    def __init__(self, turntable: Motor, turret: Motor, spin: Motor, compass=None):
        self._targetTurntableAngle = 0
        self._targetTurretAngle = 0
        self._targetPivotAngle = 0

        self._observatoryAltitude = 0
        self._observatoryAzimuth = 0

        self.turntable = turntable
        self.turret = turret
        self.spin = spin

        # Position data given by star tracker GPS and magnetometer:
        self._compassHeading = 0  # deg around a comapss (dead N)

    # Called by program to update observatory to new star position (this function calls _calculate_target_configuration and _move)
    def go_to(self, altitude, azimuth, degrees_per_second, cancellation_event: Event = None):
        # Calculate observatory altitude and azimuth based on orientation of observatory
        self._observatoryAltitude = altitude
        self._observatoryAzimuth = azimuth - self._compassHeading

        # Calculate what that means for the observatory in terms of joints
        # targetTurntable, targetTurret = self._calculate_target_configuration()

        # Command the motors to move
        self._move(altitude, azimuth, degrees_per_second, cancellation_event)

    # Uses geometry of observatory to calculate the corresponding position of all joints
    def _calculate_target_configuration(self) -> Tuple[float, float]:
        # Use gyro, do some caluclations
        return

    # Actually command the motors to move
    async def _move(self, target_turntable_angle: float, target_turret_angle: float, degrees_per_second: float,
                    cancellation_event: Event):
        # TODO: Use maths to calculate the vertical/horizontal component degrees per second
        # TODO: pass cancellation event to the threads
        await asyncio.gather(
            asyncio.to_thread(self.turntable.go_to, target_turntable_angle, degrees_per_second),
            asyncio.to_thread(self.turret.go_to, target_turret_angle, degrees_per_second)
            # asyncio.to_thread(self.spin.go_to, -180, 60) 
        )


if __name__ == '__main__':
    starTracker = StarTracker(config.TURNTABLE, config.TURRET, config.SPIN)

    for i in range(3):
        for j in range(4):
            starTracker.goto(45 * i, 90 * j)
            time.sleep(1)
