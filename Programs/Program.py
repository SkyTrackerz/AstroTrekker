import queue
import threading
from abc import ABC, abstractmethod
from threading import Event


class Program(ABC):
    Input = None

    @abstractmethod
    def __init__(self):
        # TODO: Set max size, which blocks adding to the queue?
        self.command_queue = queue.Queue()
        self.cancellation_event = Event()
        self.thread = threading.Thread(target=self._run)

    def start(self):
        if not self.cancellation_event.is_set():
            self.thread.start()

    def _run(self):
        while not self.cancellation_event.is_set():
            try:
                # If this ends up over-utilizing the CPU by executing too quickly, consider get-waiting for .01 seconds?
                command = self.command_queue.get_nowait()
                self.handle_command(command)
            except queue.Empty:
                if self.execute():
                    break

    @abstractmethod
    def execute(self) -> bool:
        pass

    def handle_command(self, command):
        pass

    def stop(self):
        self.cancellation_event.clear()
        if self.thread:
            self.thread.join()
