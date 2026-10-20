"""Bangla Calendar: Bangladesh revised civil calendar, MIT licensed."""
from __future__ import annotations
import calendar
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk

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
    BG, GREEN, DARK, LIGHT, TEXT, MUTED, LINE, WHITE = "#F3F7F4", "#15583F", "#103E2D", "#DDF2E5", "#1E2B24", "#69766E", "#DCE5DE", "#FFFFFF"
    FONT = "Nirmala UI"
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title(f"{APP_TITLE} · বঙ্গাব্দ")
        root.geometry("900x790")
        root.minsize(790, 720)
        root.configure(bg=self.BG)
        root.option_add("*Font", (self.FONT, 10))
        today = date.today()
        self.selected_date = today
        self.view_year, self.view_month, _ = gregorian_to_bangla(today)
        self._build()
        self.render_calendar()

    def _build(self):
        top = tk.Frame(self.root, bg=self.GREEN, padx=22, pady=16)
        top.pack(fill="x")
        tk.Label(top, text="বাংলা ক্যালেন্ডার", bg=self.GREEN, fg=self.WHITE, font=(self.FONT, 23, "bold")).pack(anchor="w")
        tk.Label(top, text="বাংলাদেশের সংশোধিত বাংলা বর্ষপঞ্জি", bg=self.GREEN, fg="#DDF2E5", font=(self.FONT, 10)).pack(anchor="w", pady=(3, 0))
        main = tk.Frame(self.root, bg=self.BG, padx=18, pady=15)
        main.pack(fill="both", expand=True)
        nav = tk.Frame(main, bg=self.BG)
        nav.pack(fill="x", pady=(0, 12))
        tk.Button(nav, text="‹ আগের মাস", command=lambda: self.move_month(-1), padx=12, pady=7).pack(side="left")
        tk.Button(nav, text="আজ", command=self.go_today, padx=18, pady=7).pack(side="left", padx=8)
        tk.Button(nav, text="পরের মাস ›", command=lambda: self.move_month(1), padx=12, pady=7).pack(side="right")
        self.month_title = tk.Label(main, text="", bg=self.BG, fg=self.DARK, font=(self.FONT, 22, "bold"))
        self.month_title.pack()
        self.range_label = tk.Label(main, text="", bg=self.BG, fg=self.MUTED, font=(self.FONT, 10))
        self.range_label.pack(pady=(0, 12))
        shell = tk.Frame(main, bg=self.WHITE, highlightbackground=self.LINE, highlightthickness=1)
        shell.pack(fill="both", expand=True)
        weekdays = tk.Frame(shell, bg=self.GREEN); weekdays.pack(fill="x")
        for col, label in enumerate(WEEKDAY_SHORT):
            weekdays.grid_columnconfigure(col, weight=1, uniform="weekday")
            tk.Label(weekdays, text=label, bg=self.GREEN, fg="#FFE4B8" if col >= 5 else self.WHITE, font=(self.FONT, 10, "bold"), pady=9).grid(row=0, column=col, sticky="nsew")
        self.grid = tk.Frame(shell, bg=self.LINE); self.grid.pack(fill="both", expand=True, padx=1, pady=1)
        for col in range(7): self.grid.grid_columnconfigure(col, weight=1, uniform="days")
        for row in range(6): self.grid.grid_rowconfigure(row, weight=1, uniform="weeks")
        detail = tk.Frame(main, bg=self.WHITE, highlightbackground=self.LINE, highlightthickness=1, padx=18, pady=13)
        detail.pack(fill="x", pady=(14, 0))
        tk.Label(detail, text="নির্বাচিত তারিখ", bg=self.WHITE, fg=self.MUTED, font=(self.FONT, 9)).pack(anchor="w")
        self.detail_bn = tk.Label(detail, text="", bg=self.WHITE, fg=self.DARK, font=(self.FONT, 17, "bold")); self.detail_bn.pack(anchor="w", pady=(2, 0))
        self.detail_en = tk.Label(detail, text="", bg=self.WHITE, fg=self.TEXT, font=(self.FONT, 10)); self.detail_en.pack(anchor="w", pady=(2, 0))
        tk.Label(main, text="বাংলাদেশের সংশোধিত বাংলা বর্ষপঞ্জি · তারিখের গণনা অফলাইনে হয়", bg=self.BG, fg=self.MUTED, font=(self.FONT, 9)).pack(pady=(10, 0))

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
        lengths = month_lengths(self.view_year)
        start = bangla_month_start(self.view_year, self.view_month)
        days = lengths[self.view_month - 1]
        end = start + timedelta(days=days - 1)
        self.month_title.configure(text=f"{MONTHS[self.view_month - 1]} {bn_digits(self.view_year)}")
        self.range_label.configure(text=f"{bn_digits(start.day)} {GREGORIAN_MONTHS[start.month - 1]} {bn_digits(start.year)} — {bn_digits(end.day)} {GREGORIAN_MONTHS[end.month - 1]} {bn_digits(end.year)}")
        for child in self.grid.winfo_children(): child.destroy()
        first_col = (start.weekday() + 1) % 7
        for day in range(1, days + 1):
            greg = start + timedelta(days=day - 1)
            row, col = divmod(first_col + day - 1, 7)
            today, selected = greg == date.today(), greg == self.selected_date
            bg = self.LIGHT if selected else ("#EAF5EE" if today else ("#FFF5E8" if col >= 5 else self.WHITE))
            cell = tk.Frame(self.grid, bg=bg, highlightbackground=self.LINE, highlightthickness=1, cursor="hand2")
            cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1); cell.grid_propagate(False)
            fg = self.DARK if today or selected else self.TEXT
            day_label = tk.Label(cell, text=bn_digits(day), bg=bg, fg=fg, font=(self.FONT, 17, "bold"), cursor="hand2"); day_label.pack(anchor="nw", padx=8, pady=(5, 0))
            greg_label = tk.Label(cell, text=f"{bn_digits(greg.day)} {GREGORIAN_SHORT[greg.month - 1]}", bg=bg, fg=self.MUTED, font=(self.FONT, 8), cursor="hand2"); greg_label.pack(anchor="nw", padx=8)
            if today: tk.Label(cell, text="আজ", bg=bg, fg=self.GREEN, font=(self.FONT, 8, "bold"), cursor="hand2").place(relx=1, x=-7, y=6, anchor="ne")
            for widget in (cell, day_label, greg_label): widget.bind("<Button-1>", lambda _e, chosen=greg: self.select_date(chosen))
        self.detail_bn.configure(text=format_bangla_date(self.selected_date))
        self.detail_en.configure(text=f"ইংরেজি তারিখ: {format_gregorian_date(self.selected_date)}")

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
