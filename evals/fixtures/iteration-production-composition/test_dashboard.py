import unittest

from app import Dashboard


class DashboardTest(unittest.TestCase):
    def test_enabled_dashboard_shows_summary_for_signed_in_user(self):
        self.assertEqual(Dashboard(login_enabled=True).summary(signed_in=True), "summary")


if __name__ == "__main__":
    unittest.main()
