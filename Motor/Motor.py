from threading import Event, Thread

import time
import asyncio
import config
from Motor.IMotor import IMotor
import logging
import logging.config
import RPi.GPIO as GPIO

from Motor.MotorConfig import MotorConfig


class Motor(IMotor):
    BACKWARD = False
    FORWARD = not BACKWARD
    limit_switch = None

    def __init__(self, config: MotorConfig):
        self.config = config
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.config.step_pin, GPIO.OUT)
        GPIO.setup(self.config.direction_pin, GPIO.OUT)
        if self.config.enable_pin:
            GPIO.setup(self.config.enable_pin, GPIO.OUT)
            GPIO.output(self.config.enable_pin, GPIO.LOW)  # Enable the Motor

        # Initialize ENABLE pin
        self.current_step = 0

        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger(__name__)

        self.stop_event = Event()  # Use an event for signaling

        if config.limit_switch:
            self.limit_switch = config.limit_switch
            # self.limit_switch.add_active_callback(self.limit_switch_callback)

    def enable(self):
        if self.config.enable_pin:
            GPIO.output(self.config.enable_pin, GPIO.LOW)

    def disable(self):
        if self.config.enable_pin:
            GPIO.output(self.config.enable_pin, GPIO.HIGH)

    def limit_switch_callback(self):
        self.stop_event.set()
        self.logger.info("Limit switch detected " + f" from {self.config.name} motor" if self.config.name else "")

    @property
    def current_angle(self):
        return self.calculate_current_angle()

    @property
    def degrees_per_step(self) -> float:
        """
        Calculate the degrees per step based on the degrees per full step,
        the number of microsteps per full step, and the gear ratio.
        """
        return self.config.degrees_per_step

    def should_stop(self, direction: bool, zeroing: bool, cancellation_event: Event = None):
        stop_from_cancellation = cancellation_event and cancellation_event.is_set()
        stop_from_limit = direction != self.config.forward_direction and self.limit_switch.isActive()
        return stop_from_cancellation or stop_from_limit


    def step_motor(self, steps: int, direction: bool, seconds_per_step: float = 1, check_limit=True, zeroing=False,
                   cancellation_event: Event = None):
        # print(f"stepping {steps} steps in {direction} dir at {seconds_per_step} sps")
        # if check_limit:
        #    steps = self._limit_in_range(steps, direction)
        # Set direction
        GPIO.output(self.config.direction_pin, GPIO.HIGH if direction else GPIO.LOW)
        # Perform steps
        half_seconds_per_step = seconds_per_step / 2
        step_inc = 1 if direction == self.config.forward_direction else -1
        for i in range(steps):
            if i % 10 == 0 and self.should_stop(direction, zeroing, cancellation_event) or (
                    cancellation_event and cancellation_event.is_set()):
                print(f"Stopping motor stepping {steps} in {direction} dir because cancellation or limit switch")
                self.logger.debug(f"Cancelled motor {self.config.name}")
                break
            GPIO.output(self.config.step_pin, GPIO.HIGH)
            time.sleep(half_seconds_per_step)
            GPIO.output(self.config.step_pin, GPIO.LOW)
            self.current_step += step_inc
            # print("*", end="")
            time.sleep(half_seconds_per_step)  # Adjust this delay for speed control
        # print(f'Done at {time.perf_counter()} for sps {seconds_per_step}')

    def _limit_in_range(self, steps: int, direction: bool) -> int:
        max_steps = int(self.config.max_angle * self.config.degrees_per_step)

        if direction == self.FORWARD:
            potential_pos = self.current_step + steps
            if potential_pos <= max_steps:
                return steps
            else:
                return max_steps - self.current_step
        else:
            potential_pos = self.current_step - steps
            if potential_pos >= 0:
                return steps
            else:
                return self.current_step

    def go_to(self, angle: float, degrees_per_second=1, check_limit=True, cancellation_event: Event = None):
        self.logger.debug(
            f"Go to called on {self.config.name}. Angle: {angle}, dps: {degrees_per_second}, checkLimit: {check_limit}")
        if angle == 0:
            return
        seconds_per_step = self._calculate_seconds_per_step(degrees_per_second)
        self.logger.debug(f"calculated seconds per step: {seconds_per_step}")
        step_dir = angle > 0
        if not self.config.forward_direction:
            step_dir = not step_dir
        # TODO: rounding errors?
        self.step_motor(steps=int(abs(angle) / self.config.degrees_per_step),
                        direction=step_dir, seconds_per_step=seconds_per_step, check_limit=check_limit,
                        cancellation_event=cancellation_event)

    def go_to_absolute(self, angle: float, degrees_per_second, check_limit=True, cancellation_event=None):
        current_angle = self.calculate_current_angle()
        print(f"calculated current angle as {current_angle}")
        target_rel_angle = angle - current_angle
        self.go_to(target_rel_angle, degrees_per_second, check_limit, cancellation_event)

    def calculate_current_angle(self):
        return self.config.degrees_per_step * self.current_step + self.config.offset_angle

    def zero(self):
        self.logger.debug(f'zeroing using {self.config.limit_switch.__class__.__name__}')
        if not self.config.limit_switch:
            pass
        while not self.config.limit_switch.isActive():
            self.step_motor(10, not self.config.forward_direction,
                            seconds_per_step=self._calculate_seconds_per_step(config.zero_degrees_per_sec),
                            check_limit=False)
        self.current_step = 0

    def _calculate_seconds_per_step(self, degrees_per_second: float):
        return self.config.degrees_per_step / degrees_per_second

    def __del__(self):
        # Clean up 
        # GPIO.cleanup()
        # TODO: Use pull up resisters so the enable pin defaults to On
        pass


def precise_sleep(duration: float):
    start_time = time.perf_counter()
    while True:
        elapsed_time = time.perf_counter() - start_time
        remaining_time = duration - elapsed_time
        if remaining_time <= 0:
            break
        if remaining_time >= 0.02:
            time.sleep(max(remaining_time / 2, 0.0001))
        else:
            pass


async def main():
    def set_cancellation_event_after_delay(event: Event, delay: float):
        time.sleep(delay)
        print('Cancelling movement...')
        event.set()

    cancellation_event = Event()  # Define the cancellation event
    cancellation_thread = Thread(target=set_cancellation_event_after_delay, args=(cancellation_event, 7))
    # cancellation_thread.start()

    # Example usage
    turntable = Motor(config.TURNTABLE)
    turret = Motor(config.TURRET)
    spin = Motor(config.SPIN)

    # asyncio.run(turntable.zero())
    # asyncio.run(Motor.zero())
    # asyncio.run(spin.zero())
    # turntable.zero()
    # await Motor.go_to(10, 10)
    try:
        while True and not cancellation_event.is_set():
            print("moving 90 degrees forward")
            await asyncio.gather(
                # turntable.go_to(90, 10),
                asyncio.to_thread(turntable.go_to, 90, 30, cancellation_event=cancellation_event),
                asyncio.to_thread(turret.go_to, 90, 30, cancellation_event=cancellation_event),
                asyncio.to_thread(spin.go_to, 180, 60, cancellation_event=cancellation_event)
            )

            print("moving 90 degrees backward")
            await asyncio.gather(
                # turntable.go_to(90, 10),
                asyncio.to_thread(turntable.go_to, -90, 30, cancellation_event=cancellation_event),
                asyncio.to_thread(turret.go_to, -90, 30, cancellation_event=cancellation_event),
                asyncio.to_thread(spin.go_to, -180, 60, cancellation_event=cancellation_event)
            )
            print("sleeping")
            time.sleep(2)
    except KeyboardInterrupt:
        cancellation_event.set()


if __name__ == '__main__':
    logging.config.fileConfig('../logging.conf')
    asyncio.run(main())
