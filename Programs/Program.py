import queue
import threading
from abc import ABC, abstractmethod
from threading import Event
from typing import Generic, TypeVar

T = TypeVar('T')


class Program(ABC, Generic[T]):
    Input: T

    @abstractmethod
    def __init__(self):
        # TODO: Set max size, which blocks adding to the queue?
        self.command_queue = queue.Queue()
        self.cancellation_event = Event()
        self.thread = threading.Thread(target=self._run, name="ProgramThread")
        self._is_done = False

    @property
    def is_done(self):
        return self._is_done

    def start(self):
        if not self.cancellation_event.is_set():
            self.thread.start()

    def _run(self):
        while not self.cancellation_event.is_set():
            self._is_done = self.execute(self.cancellation_event)
            if self._is_done:
                break

    """
    @returns if execution should continue
    """
    @abstractmethod
    def execute(self, cancellation_event: Event) -> bool:
        pass

    def handle_command(self, command):
        pass

    def stop(self):
        self.cancellation_event.set()
        if self.thread:
            self.thread.join()
