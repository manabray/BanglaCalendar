import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from holidays import (
    HOLIDAYS, OFFICIAL_HOLIDAY_SOURCE, get_holidays_for_date, get_holidays_for_year,
)

class HolidayTests(unittest.TestCase):
    def test_recurring_language_day(self):
        items = get_holidays_for_date(date(2027, 2, 21))
        self.assertTrue(any("মাতৃভাষা" in event["name"] for event in items))

    def test_2026_eid_fitr_span(self):
        for day in (19, 20, 21, 22, 23):
            items = get_holidays_for_date(date(2026, 3, day))
            self.assertTrue(any("ঈদুল ফিতর" in event["name"] for event in items))

    def test_2026_victory_day(self):
        items = get_holidays_for_date(date(2026, 12, 16))
        self.assertTrue(any("বিজয় দিবস" in event["name"] for event in items))

    def test_wikipedia_attribution_exists(self):
        self.assertGreaterEqual(len(HOLIDAYS), 30)
        for event in HOLIDAYS:
            self.assertTrue(event.get("summary"), event.get("name"))
            self.assertTrue(event.get("wiki", "").startswith("https://en.wikipedia.org/wiki/"), event.get("name"))

    def test_holiday_year_list_is_sorted(self):
        items = get_holidays_for_year(2026)
        starts = [event["start_date"] for event in items]
        self.assertEqual(starts, sorted(starts))
        self.assertGreater(len(items), 30)

    def test_non_2026_year_discloses_recurring_dates_only(self):
        names = [event["name"] for event in get_holidays_for_year(2027)]
        self.assertIn("পহেলা বৈশাখ", names)
        self.assertIn("বিজয় দিবস", names)
        self.assertNotIn("ঈদুল ফিতরের ছুটি", names)

    def test_official_source_is_mopa(self):
        self.assertIn("mopa.gov.bd", OFFICIAL_HOLIDAY_SOURCE)

if __name__ == "__main__":
    unittest.main()
