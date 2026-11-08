import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import holidays


class EventTests(unittest.TestCase):
    def tearDown(self):
        holidays.reload_user_events(Path(tempfile.gettempdir()) / "no-such-events.json")

    def names(self, d):
        return [e["name"] for e in holidays.get_holidays_for_date(d)]

    def test_bangla_date_observances_follow_the_bangla_calendar(self):
        for year in (2025, 2026, 2027, 2028):
            self.assertTrue(any("রবীন্দ্র জয়ন্তী" in n for n in self.names(date(year, 5, 8))), year)
            self.assertTrue(any("নজরুল জয়ন্তী" in n for n in self.names(date(year, 5, 25))), year)

    def test_observances_are_not_public_holidays(self):
        self.assertFalse(holidays.is_public_holiday(date(2026, 5, 8)))
        self.assertTrue(holidays.is_public_holiday(date(2026, 12, 16)))

    def test_user_events_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.json"
            path.write_text(json.dumps({
                "gregorian": {"03-17": "জন্মদিন", "13-45": "ভুল"},
                "bangla": {"10-20": "বিবাহ বার্ষিকী", "11-30": "ফাল্গুনের শেষ"},
                "dates": {"2027-03-10": "এক দিনের কাজ", "bad": "x"},
            }), encoding="utf-8")
            holidays.reload_user_events(path)
            self.assertIn("জন্মদিন", self.names(date(2026, 3, 17)))
            self.assertIn("এক দিনের কাজ", self.names(date(2027, 3, 10)))
            self.assertNotIn("এক দিনের কাজ", self.names(date(2026, 3, 10)))
            self.assertIn("বিবাহ বার্ষিকী", self.names(date(2027, 2, 3)))  # ২০ মাঘ ১৪৩৩
            self.assertFalse(holidays.is_public_holiday(date(2027, 3, 10)))  # ব্যক্তিগত দিবস ছুটি নয়
            self.assertNotIn("ভুল", [e["name"] for e in holidays.get_holidays_for_year(2026)])

    def test_missing_or_broken_user_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "events.json"
            bad.write_text("{not json", encoding="utf-8")
            self.assertEqual(holidays.load_user_events(bad), [])
            self.assertEqual(holidays.load_user_events(Path(tmp) / "missing.json"), [])
            bad.write_text("[1,2]", encoding="utf-8")
            self.assertEqual(holidays.load_user_events(bad), [])


if __name__ == "__main__":
    unittest.main()
