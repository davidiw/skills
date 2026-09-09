import unittest
from promo import apply
class PromoTest(unittest.TestCase):
    def test_known(self):
        self.assertEqual(apply(100, "SAVE10"), 90)
    def test_unknown(self):
        self.assertEqual(apply(100, "OTHER"), 100)
