import typing

from threading import Thread, Event
from redis import Redis


class FakeApp:

    def __init__(self, client: Redis, logic: typing.Callable[[Redis], None]):
        self.client = client
        self.logic = logic

    def run(self):
        e = Event()
        t = Thread(target=self._run_logic, args=(e,))
        t.start()
        return e, t

    def _run_logic(self, e: Event):
        while not e.is_set():
            self.logic(self.client)
