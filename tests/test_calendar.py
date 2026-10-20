import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bangla_calendar import bangla_to_gregorian, gregorian_to_bangla, month_lengths

class CalendarTests(unittest.TestCase):
    def test_pohela_boishakh(self):
        self.assertEqual(bangla_to_gregorian(1433, 1, 1), date(2026, 4, 14))
        self.assertEqual(gregorian_to_bangla(date(2026, 4, 14)), (1433, 1, 1))
    def test_february_21(self):
        self.assertEqual(gregorian_to_bangla(date(2026, 2, 21)), (1432, 11, 8))
        self.assertEqual(gregorian_to_bangla(date(2024, 2, 21)), (1430, 11, 8))
    def test_poush_first(self):
        self.assertEqual(gregorian_to_bangla(date(2026, 12, 16)), (1433, 9, 1))
    def test_falgun_leap_rules(self):
        self.assertEqual(month_lengths(1430)[10], 30)
        self.assertEqual(month_lengths(1431)[10], 29)
        self.assertEqual(sum(month_lengths(1430)), 366)
        self.assertEqual(sum(month_lengths(1431)), 365)
    def test_round_trip(self):
        for d in (date(2023, 4, 14), date(2024, 2, 29), date(2024, 4, 13), date(2026, 10, 20)):
            self.assertEqual(bangla_to_gregorian(*gregorian_to_bangla(d)), d)

if __name__ == "__main__": unittest.main()
