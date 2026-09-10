import unittest
from service import publish, display_fields
class DisplayTest(unittest.TestCase):
    def test_label(self):
        self.assertEqual(publish("[[ref:a]]: 12 kg", "Crate: 12 kg", {"a":"Crate"}), "Crate: 12 kg")
    def test_schema(self):
        self.assertIn("internal_code", display_fields({"input_schema":{"properties":{"internal_code":{}}}}))
