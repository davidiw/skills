import unittest

from src.events import EventBus


class EventBusTest(unittest.TestCase):
    def test_subscriber_receives_each_event_synchronously(self) -> None:
        received = []
        bus = EventBus()
        bus.subscribe(received.append)

        bus.publish("first")
        bus.publish("second")

        self.assertEqual(received, ["first", "second"])
