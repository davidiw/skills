import unittest
from sync import Queue, Coordinator

class WakeTest(unittest.TestCase):
    def test_existing_scheduled_wake_coalesces(self):
        q = Queue()
        c = Coordinator(q, "a")
        c.scheduled_wake()
        c.scheduled_wake()
        self.assertEqual(q.admissions, [("a", "provider"), ("a", "server")])
