import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import calendar_core as core
from calendar_core import bangla_to_gregorian, gregorian_to_bangla


class CoreTests(unittest.TestCase):
    def test_month_starts_2019_revised_rule(self):
        # ১৪৩৩ বঙ্গাব্দের প্রতি মাসের ১ তারিখ (বাংলা একাডেমি, ২০১৯)
        expected = [(2026, 4, 14), (2026, 5, 15), (2026, 6, 15), (2026, 7, 16), (2026, 8, 16),
                    (2026, 9, 16), (2026, 10, 17), (2026, 11, 16), (2026, 12, 16),
                    (2027, 1, 15), (2027, 2, 14), (2027, 3, 15)]
        for month, ymd in enumerate(expected, 1):
            self.assertEqual(bangla_to_gregorian(1433, month, 1), date(*ymd), month)

    def test_official_anchor_days(self):
        self.assertEqual(gregorian_to_bangla(date(2026, 3, 26)), (1432, 12, 12))   # ১২ চৈত্র
        self.assertEqual(gregorian_to_bangla(date(2026, 5, 8)), (1433, 1, 25))     # ২৫ বৈশাখ
        self.assertEqual(gregorian_to_bangla(date(2026, 5, 25)), (1433, 2, 11))    # ১১ জ্যৈষ্ঠ
        self.assertEqual(gregorian_to_bangla(date(2026, 8, 9)), (1433, 4, 25))     # ২৫ শ্রাবণ
        self.assertEqual(gregorian_to_bangla(date(2026, 11, 8)), (1433, 7, 23))    # ২৩ কার্তিক

    def test_year_end_and_leap(self):
        self.assertEqual(gregorian_to_bangla(date(2026, 4, 13)), (1432, 12, 30))
        self.assertEqual(gregorian_to_bangla(date(2024, 2, 29)), (1430, 11, 16))
        self.assertEqual(gregorian_to_bangla(date(2024, 3, 14)), (1430, 11, 30))
        self.assertEqual(gregorian_to_bangla(date(2024, 3, 15)), (1430, 12, 1))
        self.assertEqual(gregorian_to_bangla(date(2026, 3, 14)), (1432, 11, 29))

    def test_year_lengths_match_gregorian(self):
        for year in range(1300, 1600):
            days = (core.bangla_year_start(year + 1) - core.bangla_year_start(year)).days
            self.assertEqual(sum(core.month_lengths(year)), days, year)

    def test_round_trip_every_day_300_years(self):
        d, end = date(1900, 1, 1), date(2200, 12, 31)
        while d <= end:
            self.assertEqual(bangla_to_gregorian(*gregorian_to_bangla(d)), d)
            d += timedelta(days=1)

    def test_invalid_input_raises_valueerror(self):
        for args in ((1432, 11, 30), (1432, 13, 1), (1432, 1, 32), (1432, 0, 1), (0, 1, 1),
                     (core.MAX_BANGLA_YEAR + 1, 1, 1), (-700, 1, 1)):
            with self.assertRaises(ValueError, msg=args):
                bangla_to_gregorian(*args)

    def test_digits(self):
        self.assertEqual(core.bn_digits(2026), "২০২৬")
        self.assertEqual(core.parse_int(" ১৪৩৩ "), 1433)
        self.assertEqual(core.parse_int("12"), 12)
        with self.assertRaises(ValueError):
            core.parse_int("")

    def test_clamp_year(self):
        self.assertEqual(core.clamp_year(-5), core.MIN_BANGLA_YEAR)
        self.assertEqual(core.clamp_year(10**6), core.MAX_BANGLA_YEAR)

    def test_extreme_supported_years_work(self):
        for year in (core.MIN_BANGLA_YEAR, core.MAX_BANGLA_YEAR):
            last = bangla_to_gregorian(year, 12, 30)
            self.assertEqual(gregorian_to_bangla(last), (year, 12, 30))


if __name__ == "__main__":
    unittest.main()
