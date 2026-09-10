import unittest

import client


class DisplayTest(unittest.TestCase):
    def test_label_and_availability_contract(self):
        self.assertEqual(client.LABEL, "Availability")
        self.assertEqual(client.availability(3), {"available": 3})


if __name__ == "__main__":
    unittest.main()
