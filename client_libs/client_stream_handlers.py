import threading
from typing import Iterator, Callable


class ThreadedStreamHandler(threading.Thread):
    response_iterator = None
    response_data_lock = threading.Lock()
    data_handler = None
    transmission_exception = None

    def set_response_iterator(self, response_iterator: Iterator) -> None:
        self.response_iterator = response_iterator

    def set_data_handler(self, data_handler: Callable) -> None:
        self.data_handler = data_handler

    def run(self) -> None:
        if self.response_iterator is None:
            return

        self.response_data_lock.acquire()

        try:
            for response in self.response_iterator:
                self.data_handler(response)
        except Exception as e:
            self.transmission_exception = e

        del self.response_iterator
        self.response_iterator = None
        self.response_data_lock.release()
