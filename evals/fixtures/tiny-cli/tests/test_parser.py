import unittest

from src.parser import parse_report


class ParseReportTest(unittest.TestCase):
    def test_parses_required_name(self) -> None:
        self.assertEqual(parse_report({"name": "sample"}), {"name": "sample"})

    def test_rejects_missing_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "name"):
            parse_report({})


if __name__ == "__main__":
    unittest.main()
