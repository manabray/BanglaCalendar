import ast
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mobile_calendar_model import build_month_grid, selected_day_details, weekday_labels


class MobileCalendarModelTests(unittest.TestCase):
    def test_kivy_frontend_sources_are_valid_python(self):
        root = Path(__file__).resolve().parents[1]
        for filename in ("main.py", "mobile_ui.py", "mobile_calendar_model.py"):
            source = (root / filename).read_text(encoding="utf-8")
            ast.parse(source, filename=filename)

    def test_mobile_about_discloses_ai_assistance(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "mobile_ui.py").read_text(encoding="utf-8")
        self.assertIn("Manab Ray", source)
        self.assertIn("OpenAI ChatGPT", source)

    def test_grid_always_has_42_slots(self):
        for year, month in ((1433, 7), (1432, 12), (1433, 1), (1430, 11)):
            self.assertEqual(len(build_month_grid(year, month)), 42)

    def test_kartik_1433_contains_today_and_bangla_day(self):
        target = date(2026, 11, 8)
        cells = build_month_grid(1433, 7, today=target)
        cell = next(item for item in cells if item and item["date"] == target)
        self.assertEqual(cell["bangla_day"], 23)
        self.assertEqual(cell["bangla_day_text"], "২৩")
        self.assertTrue(cell["is_today"])

    def test_public_holiday_is_separate_from_observance(self):
        # ২১ ফেব্রুয়ারি সরকারি ছুটি; রবীন্দ্র জয়ন্তী দিবস, ছুটি নয়।
        february = build_month_grid(1432, 11)
        day = next(item for item in february if item and item["date"] == date(2026, 2, 21))
        self.assertTrue(day["is_holiday"])
        self.assertFalse(day["is_observance"])

    def test_selected_day_details_include_events(self):
        target = date(2026, 12, 16)
        details = selected_day_details(target)
        self.assertTrue(any("বিজয় দিবস" in event["name"] for event in details["holidays"]))

    def test_weekdays_are_sunday_first(self):
        self.assertEqual(weekday_labels()[0], "রবি")
        self.assertEqual(weekday_labels()[-1], "শনি")


if __name__ == "__main__":
    unittest.main()
