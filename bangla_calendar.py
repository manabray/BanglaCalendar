"""Bangla Calendar: Bangladesh revised civil calendar, MIT licensed."""
from __future__ import annotations
import calendar
import tkinter as tk
import webbrowser
from datetime import date, datetime, timedelta
from tkinter import ttk
from holidays import OFFICIAL_HOLIDAY_SOURCE, get_holidays_for_date, get_holidays_for_year

APP_TITLE = "বাংলা ক্যালেন্ডার"
VERSION = "0.1.0"
BANGLA_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
MONTHS = ["বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন",
          "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"]
WEEKDAYS = ["সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার", "রবিবার"]
WEEKDAY_SHORT = ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"]
GREGORIAN_MONTHS = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন",
                    "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
GREGORIAN_SHORT = ["জানু", "ফেব্রু", "মার্চ", "এপ্রি", "মে", "জুন",
                   "জুলাই", "আগস্ট", "সেপ্টে", "অক্টো", "নভে", "ডিসে"]

SEASONS = {
    1: ("গ্রীষ্ম", "গরমের দিন, আম-কাঁঠাল ও ফলের মৌসুম।"),
    2: ("গ্রীষ্ম", "গরমের দিন, আম-কাঁঠাল ও ফলের মৌসুম।"),
    3: ("বর্ষা", "বৃষ্টি, নদী ও সবুজে ভরা ঋতু।"),
    4: ("বর্ষা", "বৃষ্টি, নদী ও সবুজে ভরা ঋতু।"),
    5: ("শরৎ", "নীল আকাশ, সাদা মেঘ ও কাশফুলের সময়।"),
    6: ("শরৎ", "নীল আকাশ, সাদা মেঘ ও কাশফুলের সময়।"),
    7: ("হেমন্ত", "পাকা ধান ও নবান্নের ঋতু।"),
    8: ("হেমন্ত", "পাকা ধান ও নবান্নের ঋতু।"),
    9: ("শীত", "শীতের সকাল, কুয়াশা ও পিঠা-পুলির সময়।"),
    10: ("শীত", "শীতের সকাল, কুয়াশা ও পিঠা-পুলির সময়।"),
    11: ("বসন্ত", "ফুল, নতুন পাতা ও রঙিন প্রকৃতির ঋতু।"),
    12: ("বসন্ত", "ফুল, নতুন পাতা ও রঙিন প্রকৃতির ঋতু।"),
}

def season_for_month(bangla_month: int) -> tuple[str, str]:
    """Return the Bengali season and a short description for Bangla month 1-12."""
    if bangla_month not in SEASONS:
        raise ValueError("বাংলা মাস ১ থেকে ১২-এর মধ্যে হতে হবে")
    return SEASONS[bangla_month]


def bn_digits(value: int | str) -> str:
    return str(value).translate(BANGLA_DIGITS)

def bangla_year_for_date(gregorian_date: date) -> int:
    return gregorian_date.year - (593 if (gregorian_date.month, gregorian_date.day) >= (4, 14) else 594)

def month_lengths(bangla_year: int) -> tuple[int, ...]:
    falgun_year = bangla_year + 594
    return (31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30 if calendar.isleap(falgun_year) else 29, 30)

def bangla_year_start(bangla_year: int) -> date:
    return date(bangla_year + 593, 4, 14)

def bangla_month_start(bangla_year: int, month: int) -> date:
    if not 1 <= month <= 12:
        raise ValueError("বাংলা মাস ১ থেকে ১২-এর মধ্যে হতে হবে")
    return bangla_year_start(bangla_year) + timedelta(days=sum(month_lengths(bangla_year)[:month - 1]))

def bangla_to_gregorian(bangla_year: int, month: int, day: int) -> date:
    if not 1 <= month <= 12:
        raise ValueError("বাংলা মাস ১ থেকে ১২-এর মধ্যে হতে হবে")
    lengths = month_lengths(bangla_year)
    if not 1 <= day <= lengths[month - 1]:
        raise ValueError(f"এই মাসে {day} তারিখ নেই")
    return bangla_month_start(bangla_year, month) + timedelta(days=day - 1)

def gregorian_to_bangla(gregorian_date: date) -> tuple[int, int, int]:
    year = bangla_year_for_date(gregorian_date)
    offset = (gregorian_date - bangla_year_start(year)).days
    for month, length in enumerate(month_lengths(year), 1):
        if offset < length:
            return year, month, offset + 1
        offset -= length
    raise ValueError("তারিখটি বাংলা বর্ষের সীমার বাইরে")

def format_bangla_date(gregorian_date: date) -> str:
    year, month, day = gregorian_to_bangla(gregorian_date)
    return f"{bn_digits(day)} {MONTHS[month - 1]} {bn_digits(year)} বঙ্গাব্দ"

def format_gregorian_date(gregorian_date: date) -> str:
    return f"{bn_digits(gregorian_date.day)} {GREGORIAN_MONTHS[gregorian_date.month - 1]} {bn_digits(gregorian_date.year)} ({WEEKDAYS[gregorian_date.weekday()]})"

class BanglaCalendarApp:
    # Brand palette: deep blue, primary blue, and bright cyan, with neutral surfaces for readability.
    BG, PRIMARY, SECONDARY, ACCENT, LIGHT, TEXT, MUTED, LINE, WHITE = "#F2FAFE", "#00578E", "#0084C8", "#00BBFF", "#DFF5FF", "#123047", "#587385", "#C7E8F5", "#FFFFFF"
    FONT = "Nirmala UI"
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title(f"{APP_TITLE} · বঙ্গাব্দ")
        root.geometry("1140x820")
        root.minsize(980, 720)
        root.configure(bg=self.BG)
        root.option_add("*Font", (self.FONT, 10))
        today = date.today()
        self.selected_date = today
        self.view_year, self.view_month, _ = gregorian_to_bangla(today)
        self._build()
        self.render_calendar()

    def _build(self):
        top = tk.Frame(self.root, bg=self.PRIMARY, padx=22, pady=13)
        top.pack(fill="x")
        heading = tk.Frame(top, bg=self.PRIMARY)
        heading.pack(side="left", fill="x", expand=True)
        tk.Label(heading, text="বাংলা ক্যালেন্ডার", bg=self.PRIMARY, fg=self.WHITE,
                 font=(self.FONT, 22, "bold")).pack(anchor="w")
        tk.Label(heading, text="বাংলাদেশের সংশোধিত বাংলা বর্ষপঞ্জি",
                 bg=self.PRIMARY, fg=self.ACCENT, font=(self.FONT, 10)).pack(anchor="w", pady=(2, 0))
        tk.Label(top, text="বাংলা তারিখ  ·  ঘড়ি  ·  ঋতুচক্র",
                 bg=self.PRIMARY, fg=self.WHITE, font=(self.FONT, 10, "bold")).pack(side="right", anchor="center")

        content = tk.Frame(self.root, bg=self.BG, padx=14, pady=14)
        content.pack(fill="both", expand=True)

        # Sidebar combines month/year, today's date and a compact clock.
        side = tk.Frame(content, bg=self.PRIMARY, width=268, padx=16, pady=16)
        side.pack(side="left", fill="y", padx=(0, 14))
        side.pack_propagate(False)
        tk.Label(side, text="বাংলা ঋতুচক্র", bg=self.PRIMARY, fg=self.ACCENT,
                 font=(self.FONT, 10, "bold")).pack(anchor="w")
        self.side_month_title = tk.Label(side, text="", bg=self.PRIMARY, fg=self.WHITE,
                                         font=(self.FONT, 24, "bold"), wraplength=225, justify="left")
        self.side_month_title.pack(anchor="w", pady=(8, 0))
        self.side_year_title = tk.Label(side, text="", bg=self.PRIMARY, fg=self.WHITE,
                                        font=(self.FONT, 10))
        self.side_year_title.pack(anchor="w", pady=(0, 8))

        date_clock_row = tk.Frame(side, bg=self.SECONDARY, padx=9, pady=9,
                                  highlightbackground=self.ACCENT, highlightthickness=1)
        date_clock_row.pack(fill="x", pady=(0, 13))
        self.today_label = tk.Label(date_clock_row, text="", bg=self.SECONDARY,
                                    fg=self.WHITE, font=(self.FONT, 9, "bold"),
                                    justify="left", wraplength=115, anchor="w")
        self.today_label.pack(side="left", fill="x", expand=True, anchor="center")
        self.clock_label = tk.Label(date_clock_row, text="০০:০০:০০", bg=self.SECONDARY,
                                    fg=self.ACCENT, font=(self.FONT, 14, "bold"),
                                    cursor="hand2")
        self.clock_label.pack(side="right", anchor="center")
        self.clock_tooltip = None
        self.clock_label.bind("<Enter>", self.show_clock_tooltip)
        self.clock_label.bind("<Leave>", self.hide_clock_tooltip)

        tk.Frame(side, bg=self.ACCENT, height=3).pack(fill="x", pady=(0, 12))
        self.season_name_label = tk.Label(side, text="", bg=self.ACCENT, fg=self.PRIMARY,
                                          font=(self.FONT, 15, "bold"), padx=11, pady=6)
        self.season_name_label.pack(anchor="w")
        self.season_description_label = tk.Label(
            side, text="", bg=self.PRIMARY, fg=self.WHITE, font=(self.FONT, 9),
            justify="left", wraplength=225
        )
        self.season_description_label.pack(anchor="w", pady=(8, 14))

        self.side_holiday_card = tk.Frame(
            side, bg=self.SECONDARY, padx=10, pady=10,
            highlightbackground=self.ACCENT, highlightthickness=1
        )
        self.side_holiday_card.pack(fill="x", pady=(0, 4))
        self.side_holiday_title = tk.Label(
            self.side_holiday_card, text="আজকের ছুটি",
            bg=self.SECONDARY, fg=self.ACCENT, font=(self.FONT, 10, "bold"),
            justify="left", anchor="w"
        )
        self.side_holiday_title.pack(fill="x")
        self.side_holiday_content = tk.Frame(self.side_holiday_card, bg=self.SECONDARY)
        self.side_holiday_content.pack(fill="x", pady=(5, 0))

        # Main panel: a regular 7-column x 6-row calendar with consistent cell borders.
        main = tk.Frame(content, bg=self.BG)
        main.pack(side="left", fill="both", expand=True)
        nav = tk.Frame(main, bg=self.BG)
        nav.pack(fill="x", pady=(0, 8))
        tk.Button(nav, text="‹ আগের মাস", command=lambda: self.move_month(-1),
                  padx=12, pady=7, bg=self.SECONDARY, fg=self.WHITE,
                  activebackground=self.ACCENT, activeforeground=self.PRIMARY,
                  relief="flat", bd=0, cursor="hand2").pack(side="left")
        tk.Button(nav, text="আজ", command=self.go_today, padx=18, pady=7,
                  bg=self.ACCENT, fg=self.PRIMARY, activebackground=self.SECONDARY,
                  activeforeground=self.WHITE, relief="flat", bd=0, cursor="hand2",
                  font=(self.FONT, 10, "bold")).pack(side="left", padx=8)
        tk.Button(nav, text="ছুটির তালিকা", command=self.show_holiday_list,
                  padx=12, pady=7, bg=self.WHITE, fg=self.SECONDARY,
                  activebackground=self.ACCENT, activeforeground=self.PRIMARY,
                  relief="flat", bd=1, cursor="hand2").pack(side="left", padx=2)
        tk.Button(nav, text="পরের মাস ›", command=lambda: self.move_month(1),
                  padx=12, pady=7, bg=self.SECONDARY, fg=self.WHITE,
                  activebackground=self.ACCENT, activeforeground=self.PRIMARY,
                  relief="flat", bd=0, cursor="hand2").pack(side="right")

        title_row = tk.Frame(main, bg=self.BG)
        title_row.pack(fill="x", pady=(0, 8))
        self.month_title = tk.Label(title_row, text="", bg=self.BG, fg=self.PRIMARY,
                                    font=(self.FONT, 21, "bold"))
        self.month_title.pack(anchor="w")
        self.range_label = tk.Label(title_row, text="", bg=self.BG, fg=self.MUTED,
                                    font=(self.FONT, 9))
        self.range_label.pack(anchor="w", pady=(1, 0))

        shell = tk.Frame(main, bg=self.WHITE, highlightbackground=self.ACCENT,
                         highlightthickness=1)
        shell.pack(fill="both", expand=True)
        weekdays = tk.Frame(shell, bg=self.SECONDARY)
        weekdays.pack(fill="x")
        for col, label in enumerate(WEEKDAY_SHORT):
            weekdays.grid_columnconfigure(col, weight=1, uniform="weekday")
            tk.Label(weekdays, text=label, bg=self.SECONDARY, fg=self.WHITE,
                     font=(self.FONT, 9, "bold"), pady=8).grid(row=0, column=col, sticky="nsew")
        self.grid = tk.Frame(shell, bg=self.LINE)
        self.grid.pack(fill="both", expand=True, padx=1, pady=1)
        for col in range(7):
            self.grid.grid_columnconfigure(col, weight=1, uniform="days")
        for row in range(6):
            self.grid.grid_rowconfigure(row, weight=1, uniform="weeks")

        detail = tk.Frame(main, bg=self.WHITE, highlightbackground=self.LINE,
                          highlightthickness=1, padx=14, pady=8)
        detail.pack(fill="x", pady=(9, 0))
        tk.Label(detail, text="নির্বাচিত তারিখ", bg=self.WHITE, fg=self.MUTED,
                 font=(self.FONT, 8)).pack(anchor="w")
        self.detail_bn = tk.Label(detail, text="", bg=self.WHITE, fg=self.PRIMARY,
                                  font=(self.FONT, 14, "bold"))
        self.detail_bn.pack(anchor="w", pady=(1, 0))
        self.detail_en = tk.Label(detail, text="", bg=self.WHITE, fg=self.TEXT,
                                  font=(self.FONT, 9))
        self.detail_en.pack(anchor="w", pady=(1, 0))
        tk.Label(main, text="ছুটির তারিখ: সরকারি প্রজ্ঞাপন · সার-সংক্ষেপ: উইকিপিডিয়া নিবন্ধ",
                 bg=self.BG, fg=self.MUTED, font=(self.FONT, 8)).pack(pady=(5, 0))
        self.update_clock()


    def update_clock(self):
        """Refresh the compact clock and today's Bangla date every second."""
        now = datetime.now()
        self.clock_label.configure(text=bn_digits(now.strftime("%H:%M:%S")))
        today = date.today()
        _, month, day = gregorian_to_bangla(today)
        self.today_label.configure(text=f"আজ {bn_digits(day)} {MONTHS[month - 1]}")
        self.root.after(1000, self.update_clock)

    def show_clock_tooltip(self, _event=None):
        """Show clock-source information only while hovering over the clock."""
        if self.clock_tooltip is not None:
            return
        tip = tk.Toplevel(self.root)
        tip.overrideredirect(True)
        try:
            tip.attributes("-topmost", True)
        except tk.TclError:
            pass
        label = tk.Label(
            tip,
            text="সময় আপনার কম্পিউটারের ঘড়ি থেকে নেওয়া হয়েছে।",
            bg=self.PRIMARY, fg=self.WHITE,
            padx=9, pady=6, font=(self.FONT, 9),
            relief="solid", borderwidth=1
        )
        label.pack()
        x = self.clock_label.winfo_rootx()
        y = self.clock_label.winfo_rooty() + self.clock_label.winfo_height() + 5
        tip.geometry(f"+{x}+{y}")
        self.clock_tooltip = tip

    def hide_clock_tooltip(self, _event=None):
        if self.clock_tooltip is not None:
            try:
                self.clock_tooltip.destroy()
            except tk.TclError:
                pass
            self.clock_tooltip = None


    def move_month(self, delta: int):
        absolute = self.view_year * 12 + self.view_month - 1 + delta
        self.view_year, month0 = divmod(absolute, 12)
        self.view_month = month0 + 1
        day = min(self.selected_date.day, month_lengths(self.view_year)[self.view_month - 1])
        self.selected_date = bangla_to_gregorian(self.view_year, self.view_month, day)
        self.render_calendar()

    def go_today(self):
        self.selected_date = date.today()
        self.view_year, self.view_month, _ = gregorian_to_bangla(self.selected_date)
        self.render_calendar()

    def select_date(self, chosen: date):
        self.selected_date = chosen
        self.view_year, self.view_month, _ = gregorian_to_bangla(chosen)
        self.render_calendar()

    def render_calendar(self):
        season_name, season_description = season_for_month(self.view_month)
        self.side_month_title.configure(text=MONTHS[self.view_month - 1])
        self.side_year_title.configure(text=f"{bn_digits(self.view_year)} বঙ্গাব্দ")
        self.season_name_label.configure(text=f"ঋতু: {season_name}")
        self.season_description_label.configure(text=season_description)

        lengths = month_lengths(self.view_year)
        start = bangla_month_start(self.view_year, self.view_month)
        days = lengths[self.view_month - 1]
        end = start + timedelta(days=days - 1)
        self.month_title.configure(text=f"{MONTHS[self.view_month - 1]} {bn_digits(self.view_year)}")
        self.range_label.configure(
            text=f"{bn_digits(start.day)} {GREGORIAN_MONTHS[start.month - 1]} {bn_digits(start.year)} — "
                 f"{bn_digits(end.day)} {GREGORIAN_MONTHS[end.month - 1]} {bn_digits(end.year)}"
        )

        for child in self.grid.winfo_children():
            child.destroy()
        first_col = (start.weekday() + 1) % 7
        current_date = date.today()

        # Draw every slot first, including empty leading/trailing days, to keep
        # all rows and columns visually aligned and equally sized.
        for position in range(42):
            row, col = divmod(position, 7)
            day_number = position - first_col + 1
            is_valid_day = 1 <= day_number <= days
            default_bg = "#F7FCFF" if col < 5 else "#EEF9FE"
            cell = tk.Frame(
                self.grid, bg=default_bg, highlightbackground=self.LINE,
                highlightthickness=1, cursor="hand2" if is_valid_day else "arrow"
            )
            cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            cell.grid_propagate(False)
            if not is_valid_day:
                continue

            greg = start + timedelta(days=day_number - 1)
            is_today = greg == current_date
            selected = greg == self.selected_date
            holiday_events = get_holidays_for_date(greg)
            if selected:
                bg = self.ACCENT
            elif holiday_events:
                bg = "#DFF5FF"
            elif is_today:
                bg = "#E8F8FF"
            elif col >= 5:
                bg = "#F4FBFF"
            else:
                bg = self.WHITE
            cell.configure(
                bg=bg,
                highlightbackground=self.PRIMARY if holiday_events else (self.ACCENT if is_today or selected else self.LINE),
                highlightthickness=2 if holiday_events or is_today or selected else 1,
                cursor="hand2"
            )

            day_fg = self.PRIMARY if is_today or selected or holiday_events else self.TEXT
            day_label = tk.Label(
                cell, text=bn_digits(day_number), bg=bg, fg=day_fg,
                font=(self.FONT, 16, "bold"), cursor="hand2"
            )
            day_label.pack(anchor="nw", padx=7, pady=(4, 0))
            greg_label = tk.Label(
                cell, text=f"{bn_digits(greg.day)} {GREGORIAN_SHORT[greg.month - 1]}",
                bg=bg, fg=self.MUTED, font=(self.FONT, 8), cursor="hand2"
            )
            greg_label.pack(anchor="nw", padx=7, pady=(0, 1))

            if is_today or holiday_events:
                if is_today and holiday_events:
                    badge_text, badge_bg, badge_fg = "আজ · ছুটি", self.PRIMARY, self.WHITE
                elif holiday_events:
                    badge_text, badge_bg, badge_fg = "ছুটি", self.SECONDARY, self.WHITE
                else:
                    badge_text, badge_bg, badge_fg = "আজ", self.ACCENT, self.PRIMARY
                badge = tk.Label(
                    cell, text=badge_text, bg=badge_bg, fg=badge_fg,
                    font=(self.FONT, 7, "bold"), padx=4, pady=1, cursor="hand2"
                )
                badge.place(relx=1, x=-4, y=4, anchor="ne")

            def select_cell(_event, chosen=greg):
                self.select_date(chosen)
            for widget in (cell, day_label, greg_label):
                widget.bind("<Button-1>", select_cell)
            if is_today or holiday_events:
                badge.bind("<Button-1>", select_cell)

        self.detail_bn.configure(text=format_bangla_date(self.selected_date))
        self.detail_en.configure(text=f"ইংরেজি তারিখ: {format_gregorian_date(self.selected_date)}")
        self.render_holiday_detail()


    def _holiday_span_text(self, event: dict) -> str:
        start, end = event["start_date"], event["end_date"]
        if start == end:
            return f"{bn_digits(start.day)} {GREGORIAN_MONTHS[start.month - 1]} {bn_digits(start.year)}"
        if start.month == end.month:
            return f"{bn_digits(start.day)}–{bn_digits(end.day)} {GREGORIAN_MONTHS[start.month - 1]} {bn_digits(start.year)}"
        return f"{bn_digits(start.day)} {GREGORIAN_MONTHS[start.month - 1]} – {bn_digits(end.day)} {GREGORIAN_MONTHS[end.month - 1]} {bn_digits(end.year)}"

    def render_holiday_detail(self):
        """Place selected-day holiday information in the left sidebar."""
        for child in self.side_holiday_content.winfo_children():
            child.destroy()
        is_today = self.selected_date == date.today()
        self.side_holiday_title.configure(
            text="আজকের ছুটি" if is_today else "নির্বাচিত দিনের ছুটি"
        )
        events = get_holidays_for_date(self.selected_date)
        if not events:
            tk.Label(
                self.side_holiday_content,
                text="এই দিনে তালিকাভুক্ত সরকারি বা ঐচ্ছিক ছুটি নেই।",
                bg=self.SECONDARY, fg=self.WHITE, font=(self.FONT, 9),
                wraplength=218, justify="left", anchor="w"
            ).pack(fill="x")
            return

        for event in events[:2]:
            tk.Label(
                self.side_holiday_content,
                text=event["name"],
                bg=self.SECONDARY, fg=self.WHITE,
                font=(self.FONT, 10, "bold"), wraplength=218,
                justify="left", anchor="w"
            ).pack(fill="x", anchor="w", pady=(0, 2))
            tk.Label(
                self.side_holiday_content,
                text=event["category"],
                bg=self.SECONDARY, fg=self.ACCENT,
                font=(self.FONT, 8), wraplength=218,
                justify="left", anchor="w"
            ).pack(fill="x", anchor="w", pady=(0, 3))
            tk.Label(
                self.side_holiday_content,
                text=event["summary"],
                bg=self.SECONDARY, fg=self.WHITE, font=(self.FONT, 9),
                wraplength=218, justify="left", anchor="w"
            ).pack(fill="x", anchor="w", pady=(0, 4))
            tk.Button(
                self.side_holiday_content, text="আরও পড়ুন ↗",
                command=lambda url=event["wiki"]: webbrowser.open(url),
                bg=self.ACCENT, fg=self.PRIMARY, activebackground=self.WHITE,
                activeforeground=self.PRIMARY, relief="flat", bd=0,
                cursor="hand2", padx=7, pady=3, font=(self.FONT, 8, "bold")
            ).pack(anchor="w", pady=(0, 5))
        if len(events) > 2:
            tk.Label(
                self.side_holiday_content,
                text=f"এ ছাড়াও আরও {bn_digits(len(events) - 2)}টি ছুটির এন্ট্রি রয়েছে।",
                bg=self.SECONDARY, fg=self.WHITE, font=(self.FONT, 8),
                wraplength=218, justify="left", anchor="w"
            ).pack(fill="x", anchor="w")


    def show_holiday_list(self):
        year = self.selected_date.year
        events = get_holidays_for_year(year)
        window = tk.Toplevel(self.root)
        window.title(f"বাংলাদেশের ছুটির তালিকা · {bn_digits(year)}")
        window.geometry("900x690")
        window.minsize(760, 560)
        window.configure(bg=self.BG)
        header = tk.Frame(window, bg=self.PRIMARY, padx=18, pady=12)
        header.pack(fill="x")
        tk.Label(header, text=f"বাংলাদেশের ছুটির তালিকা · {bn_digits(year)}",
                 bg=self.PRIMARY, fg=self.WHITE, font=(self.FONT, 17, "bold")).pack(anchor="w")
        tk.Label(header, text="ছুটির সার-সংক্ষেপ উইকিপিডিয়া নিবন্ধের ভিত্তিতে প্রস্তুত",
                 bg=self.PRIMARY, fg=self.ACCENT, font=(self.FONT, 9)).pack(anchor="w", pady=(2, 0))
        body = tk.Frame(window, bg=self.BG, padx=14, pady=12)
        body.pack(fill="both", expand=True)
        tree_frame = tk.Frame(body, bg=self.WHITE)
        tree_frame.pack(fill="both", expand=True)
        columns = ("date", "name", "category")
        style = ttk.Style(window)
        try:
            if "clam" in style.theme_names():
                style.theme_use("clam")
            style.configure("Holiday.Treeview", font=(self.FONT, 9), rowheight=27)
            style.configure("Holiday.Treeview.Heading", font=(self.FONT, 9, "bold"))
        except tk.TclError:
            pass
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=14, style="Holiday.Treeview")
        tree.heading("date", text="তারিখ")
        tree.heading("name", text="ছুটির নাম")
        tree.heading("category", text="ধরন")
        tree.column("date", width=180, minwidth=150, anchor="w")
        tree.column("name", width=280, minwidth=200, anchor="w")
        tree.column("category", width=340, minwidth=240, anchor="w")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        detail = tk.Frame(body, bg=self.WHITE, highlightbackground=self.ACCENT, highlightthickness=1, padx=12, pady=10)
        detail.pack(fill="x", pady=(10, 0))
        selected_title = tk.Label(detail, text="তালিকা থেকে একটি ছুটি নির্বাচন করুন",
                                  bg=self.WHITE, fg=self.PRIMARY, font=(self.FONT, 11, "bold"), anchor="w")
        selected_title.pack(fill="x")
        selected_summary = tk.Label(detail, text="", bg=self.WHITE, fg=self.TEXT,
                                     font=(self.FONT, 9), justify="left", anchor="w", wraplength=830)
        selected_summary.pack(fill="x", pady=(4, 0))
        selected_note = tk.Label(detail, text="", bg=self.WHITE, fg=self.MUTED,
                                 font=(self.FONT, 8), justify="left", anchor="w")
        selected_note.pack(fill="x", pady=(3, 0))
        actions = tk.Frame(detail, bg=self.WHITE)
        actions.pack(fill="x", pady=(5, 0))
        wiki_btn = tk.Button(actions, text="উইকিপিডিয়া থেকে আরও পড়ুন ↗",
                             state="disabled", bg=self.SECONDARY, fg=self.WHITE,
                             activebackground=self.ACCENT, activeforeground=self.PRIMARY,
                             relief="flat", bd=0, cursor="hand2", padx=10, pady=5)
        wiki_btn.pack(side="left")
        tk.Button(actions, text="সরকারি ২০২৬ ছুটির প্রজ্ঞাপন ↗",
                  command=lambda: webbrowser.open(OFFICIAL_HOLIDAY_SOURCE),
                  bg=self.WHITE, fg=self.SECONDARY, activebackground=self.ACCENT,
                  relief="flat", bd=1, cursor="hand2", padx=10, pady=5).pack(side="left", padx=8)
        event_by_id = {}
        for index, event in enumerate(events):
            iid = str(index)
            event_by_id[iid] = event
            tree.insert("", "end", iid=iid, values=(
                self._holiday_span_text(event), event["name"], event["category"]
            ))
        if events:
            tree.selection_set("0")
        def show_selected(_event=None):
            chosen = tree.selection()
            if not chosen:
                return
            event = event_by_id[chosen[0]]
            selected_title.configure(text=f"{event['name']} · {event['category']}")
            selected_summary.configure(text=event["summary"])
            selected_note.configure(text="সার-সংক্ষেপের উৎস: সংশ্লিষ্ট উইকিপিডিয়া নিবন্ধ। ছুটির তারিখের সরকারি উৎস: জনপ্রশাসন মন্ত্রণালয়ের ২০২৬ সালের প্রজ্ঞাপন।")
            wiki_btn.configure(state="normal", command=lambda url=event["wiki"]: webbrowser.open(url))
        tree.bind("<<TreeviewSelect>>", show_selected)
        if events:
            show_selected()
        if year != 2026:
            footer = "সতর্কতা: সরকারি ২০২৬ সালের বিস্তারিত তালিকা এই প্রজেক্টে সংরক্ষিত। অন্য বছরের জন্য আপাতত শুধু স্থির-তারিখের ছুটি দেখানো হয়।"
        else:
            footer = "চাঁদ দেখার ওপর নির্ভরশীল ছুটির তারিখ পরিবর্তিত হতে পারে; সর্বশেষ সরকারি প্রজ্ঞাপন দেখে নিন।"
        tk.Label(body, text=footer, bg=self.BG, fg=self.MUTED, font=(self.FONT, 8),
                 anchor="w", justify="left", wraplength=860).pack(fill="x", pady=(7, 0))

def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "clam" in style.theme_names(): style.theme_use("clam")
    except tk.TclError: pass
    BanglaCalendarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
