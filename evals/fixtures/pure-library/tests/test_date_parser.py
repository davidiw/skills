import unittest

from src.date_parser import parse_date


class ParseDateTest(unittest.TestCase):
    def test_iso_date(self) -> None:
        self.assertEqual(parse_date("2026-09-04").isoformat(), "2026-09-04")
