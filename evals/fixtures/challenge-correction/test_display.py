import unittest
from renderer import render
class DisplayTest(unittest.TestCase):
    def test_existing_render(self):
        self.assertEqual(render("[[ref:a]]: 12 kg", {"a":"Crate"}), "Crate: 12 kg")
