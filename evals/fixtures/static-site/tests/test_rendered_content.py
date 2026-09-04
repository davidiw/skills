import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RenderedContentTest(unittest.TestCase):
    def test_page_has_existing_heading(self) -> None:
        page = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("<h1>Small Site</h1>", page)


if __name__ == "__main__":
    unittest.main()
