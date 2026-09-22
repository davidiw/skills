import unittest

from report import render_report


class ReportTest(unittest.TestCase):
    def test_rejected_rows_are_visible(self):
        report = render_report({"accepted": ["first"], "rejected": [""]})
        self.assertIn("Rejected rows:", report)


if __name__ == "__main__":
    unittest.main()
