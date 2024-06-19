import asyncio
import logging
import math
from threading import Event
from typing import Tuple
import config
import time
from concurrent.futures import ThreadPoolExecutor

from Motor.IMotor import IMotor
from StarTracker.IStarTracker import IStarTracker


class StarTracker(IStarTracker):
    def __init__(self, turntable: IMotor, turret: IMotor, spin: IMotor, compass=None):
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

        # Manages the threads used for concurrent motor execution
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix='MotorThread')

        self.logger = logging.getLogger(__name__)

    # Called by program to update observatory to new star position (this function calls _calculate_target_configuration and _move)
    def go_to(self, altitude, azimuth, degrees_per_second, cancellation_event: Event = None):
        # Calculate observatory altitude and azimuth based on orientation of observatory
        self._observatoryAltitude = altitude
        self._observatoryAzimuth = azimuth - self._compassHeading

        # Calculate what that means for the observatory in terms of joints
        # targetTurntable, targetTurret = self._calculate_target_configuration()

        # Command the motors to move
        self._move(altitude, azimuth, degrees_per_second, cancellation_event)

    # TODO: Knows how to get to an absolute angle based on current motor positions
    def go_to_absolute(self, altitude, azimuth, degrees_per_second=10, cancellation_event: Event = None):
        dx = azimuth - self.turntable.current_angle
        self.logger.debug(f'DX = target ({azimuth}) - current ({self.turntable.current_angle}) = {dx}')
        dy = altitude - self.turret.current_angle
        self.logger.debug(f'DY = target ({altitude}) - current ({self.turret.current_angle}) = {dy}')

        # Calculate degrees of direct path
        # TODO: Fix Approximation, spherical trigonometry required for more accuracy
        overall_degrees = math.sqrt(dx*dx + dy*dy)
        min_operable_degree = min((self.turntable.degrees_per_step, self.turret.degrees_per_step, self.spin.degrees_per_step))
        if overall_degrees < min_operable_degree:
            self.logger.debug(f"Skipping movement as requested overall angle {overall_degrees} is less than min operable angle {min_operable_degree}")
            return
        inverse_overall_time = degrees_per_second / overall_degrees
        # Component speeds
        x_speed = abs(dx * inverse_overall_time)
        y_speed = abs(dy * inverse_overall_time)
        self.logger.info(f"Speed components to move {degrees_per_second} deg/sec. X: {x_speed}, Y:{y_speed}")
        # This function is intended to be called within a new thread,
        # and sets up its own event loop for asyncio operations.

        self.run_go_tos_concurrently(dx, dy, x_speed, y_speed, cancellation_event)
        """
        # Create a new event loop for the current thread.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Now you can safely run asyncio operations in this thread.
            loop.run_until_complete(
                asyncio.gather(
                    asyncio.to_thread(self.turntable.go_to, dx, x_speed, True, cancellation_event),
                    asyncio.to_thread(self.turret.go_to, dy, y_speed, True, cancellation_event)
                    # asyncio.to_thread(self.spin.go_to, -180, 60)
                )
            )
        finally:
            loop.close()
        """

    # Function to run the go_to methods concurrently
    def run_go_tos_concurrently(self, dx, dy, x_speed, y_speed, cancellation_event: Event = None):
        futures = [
            self.executor.submit(self.turntable.go_to, dx, x_speed, True, cancellation_event),
            self.executor.submit(self.turret.go_to, dy, y_speed, True, cancellation_event)
            # Uncomment the following line if you need to include spin.go_to
            # executor.submit(spin.go_to, -180, 60)
        ]
        # Wait for all futures to complete
        for future in futures:
            future.result()

    def shutdown(self):
        # Use wait=True if it's desired for ongoing tasks to finish
        self.executor.shutdown()
        for motor in [self.turntable, self.turret, self.spin]:
            motor.disable()
        self.logger.info("StarTracker succesfully shutdown")
        
    def zero(self):
        # TODO: Clear current thread pool executor?
        futures = [
            self.executor.submit(self.turntable.zero),
            self.executor.submit(self.turret.zero)
            # Uncomment the following line if you need to include spin.go_to
            # executor.submit(spin.go_to, -180, 60)
        ]
        # Wait for all futures to complete
        for future in futures:
            future.result()

    """
    Returns a tuple of alt, az, spin
    """
    def get_current_pos(self) -> Tuple[float,float,float]:
        return self.turntable.current_angle, self.turret.current_angle, self.spin.current_angle

    # Uses geometry of observatory to calculate the corresponding position of all joints
    def _calculate_target_configuration(self) -> Tuple[float, float]:
        # Use gyro, do some caluclations
        return

    # Actually command the motors to move
    def _move(self, target_turntable_angle: float, target_turret_angle: float, degrees_per_second: float,
                    cancellation_event: Event = None):
        # TODO: Use maths to calculate the vertical/horizontal component degrees per second
        # This function is intended to be called within a new thread,
        # and sets up its own event loop for asyncio operations.

        # Create a new event loop for the current thread.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Now you can safely run asyncio operations in this thread.
            loop.run_until_complete(
                asyncio.gather(
                    asyncio.to_thread(self.turntable.go_to, target_turntable_angle, degrees_per_second, cancellation_event),
                    asyncio.to_thread(self.turret.go_to, target_turret_angle, degrees_per_second, cancellation_event)
                    # asyncio.to_thread(self.spin.go_to, -180, 60)
                )
            )
        finally:
            loop.close()


if __name__ == '__main__':
    starTracker = StarTracker(config.TURNTABLE, config.TURRET, config.SPIN)

    for i in range(3):
        for j in range(4):
            starTracker.goto(45 * i, 90 * j)
            time.sleep(1)
