import unittest
from preview import preview
class PreviewTest(unittest.TestCase):
    def test_list(self):
        self.assertEqual(preview(["7", "3"]), {"count": 2, "total": 10})
