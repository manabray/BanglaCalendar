import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import tkinter as tk
except ImportError:  # tkinter ছাড়া পাইথন
    tk = None


@unittest.skipIf(tk is None, "tkinter নেই")
class GuiSmokeTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError:
            self.skipTest("ডিসপ্লে নেই")
        self.root.withdraw()
        import bangla_calendar
        self.mod = bangla_calendar
        self.app = bangla_calendar.BanglaCalendarApp(self.root)

    def tearDown(self):
        if hasattr(self, "root"):
            self.root.destroy()

    def test_navigation_is_bounded(self):
        self.app.view_year, self.app.view_month = self.mod.MIN_BANGLA_YEAR, 1
        self.app.move_month(-1)
        self.assertEqual((self.app.view_year, self.app.view_month), (self.mod.MIN_BANGLA_YEAR, 1))
        self.app.view_year, self.app.view_month = self.mod.MAX_BANGLA_YEAR, 12
        self.app.move_month(1)
        self.assertEqual((self.app.view_year, self.app.view_month), (self.mod.MAX_BANGLA_YEAR, 12))
        self.app.move_month(-24)
        self.app.go_today()

    def test_every_month_of_several_years_renders(self):
        for year in (1430, 1432, 1433):
            for month in range(1, 13):
                self.app.view_year, self.app.view_month = year, month
                self.app.selected_date = self.mod.bangla_to_gregorian(year, month, 1)
                self.app.render_calendar()

    def test_midnight_rollover_updates_today(self):
        self.app._rendered_today = date(2000, 1, 1)
        self.app.selected_date = date(2000, 1, 1)
        self.app.update_clock()
        self.assertEqual(self.app._rendered_today, date.today())
        self.assertEqual(self.app.selected_date, date.today())

    def test_holiday_list_window_opens(self):
        self.app.show_holiday_list()
        self.app.show_converter()


if __name__ == "__main__":
    unittest.main()
