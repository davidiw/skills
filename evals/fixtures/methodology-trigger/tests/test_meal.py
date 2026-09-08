import unittest
from meal import enrich, LookupUnavailable
class ContractTest(unittest.TestCase):
    def test_known_failure_falls_back(self):
        def fail(): raise LookupUnavailable()
        self.assertEqual(enrich(fail), "estimate")
    def test_unexpected_failure_propagates(self):
        def fail(): raise ValueError()
        with self.assertRaises(ValueError): enrich(fail)
