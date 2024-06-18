from threading import Event

from Motor.Motor import Motor
from Motor.MotorConfig import MotorConfig


class TurntableMotor(Motor):
    def __init__(self, config: MotorConfig):
        super().__init__(config)
        # Something to track cycles forward and back?
        # 0 is first 0-360, 1 is 360-720, -1 is -360-0
        self.current_cycle = 0

    def should_stop(self, direction: bool, zeroing: bool, cancellation_event: Event = None):
        if zeroing:
            return super().should_stop(direction, zeroing, cancellation_event)
        if self.limit_switch.isActive():
            self._update_positioning(direction)
        # Only need this check if we are updating positioning. Also add min angle
        stop_from_angle = self.current_angle > self.config.max_angle
        stop_from_cancellation = cancellation_event and cancellation_event.is_set()
        return stop_from_angle or stop_from_cancellation

    def _update_positioning(self, direction):
        # TBH this is probably more harm than good because offsets based on direction
        # And perhaps such an update would cause jitter
        # Re-introduce after measurements? Write a script that measures number of steps of limit switch activation?
        # self.current_step = 0
        # increment cycle and override the angle calcuation
        pass
