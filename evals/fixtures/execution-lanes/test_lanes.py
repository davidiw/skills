import unittest

from lanes import settle


class LaneAdmissionTest(unittest.TestCase):
    def test_failure_stops_pending_lanes_but_keeps_running_results(self):
        self.assertEqual(
            settle({"one": "failed", "two": "passed"}, ["three", "four"]),
            {"finished": {"one": "failed", "two": "passed"}, "started_pending": []},
        )


if __name__ == "__main__":
    unittest.main()
