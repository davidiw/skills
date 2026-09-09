import unittest
from transport import wire
from client import render
class CardTest(unittest.TestCase):
    def test_plan_preview(self):
        self.assertIn("23",render(wire("plan_replace","Dispatch",{"quantity":23})))
