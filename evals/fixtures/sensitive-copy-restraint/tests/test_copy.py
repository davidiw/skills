import unittest
from pathlib import Path

class CopyTest(unittest.TestCase):
    def test_copy_is_a_single_nonempty_message(self):
        values = {}
        exec(Path("messages.py").read_text(), values)
        self.assertTrue(values["EMPTY_MESSAGE"])
