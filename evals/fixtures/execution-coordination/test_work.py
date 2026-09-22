import unittest

from work import import_rows


class ImportRowsTest(unittest.TestCase):
    def test_accepts_valid_rows_and_reports_invalid_rows(self):
        self.assertEqual(
            import_rows(["  first  ", "", None]),
            {"accepted": ["first"], "rejected": ["", None]},
        )


if __name__ == "__main__":
    unittest.main()
