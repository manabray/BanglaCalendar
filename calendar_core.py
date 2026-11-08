"""বাংলাদেশের সংশোধিত বঙ্গাব্দ পঞ্জিকার হিসাব (GUI-নিরপেক্ষ)।

নিয়ম (বাংলা একাডেমি, ২০১৯-এর সংশোধিত পঞ্জিকা):
* পহেলা বৈশাখ সবসময় ১৪ এপ্রিল; দিন শুরু মধ্যরাতে।
* বৈশাখ–আশ্বিন ৩১ দিন, কার্তিক–মাঘ ৩০ দিন, চৈত্র ৩০ দিন।
* ফাল্গুন ২৯ দিন; যে গ্রেগরীয় বছরে ফাল্গুন পড়ে সেটি লিপ ইয়ার হলে ৩০ দিন।
* এই নিয়ম অতীত/ভবিষ্যতের সব বছরে একইভাবে প্রয়োগ করা হয় (proleptic)।
"""
from __future__ import annotations
import calendar
from datetime import date, timedelta

BANGLA_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
ENGLISH_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
MONTHS = ["বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন",
          "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"]
WEEKDAYS = ["সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার", "রবিবার"]
WEEKDAY_SHORT = ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"]
GREGORIAN_MONTHS = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন",
                    "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
GREGORIAN_SHORT = ["জানু", "ফেব্রু", "মার্চ", "এপ্রি", "মে", "জুন",
                   "জুলাই", "আগস্ট", "সেপ্টে", "অক্টো", "নভে", "ডিসে"]

# গ্রেগরীয় তারিখের সীমা (datetime.date) থেকে নিরাপদ বঙ্গাব্দ পরিসর
MIN_BANGLA_YEAR = 1
MAX_BANGLA_YEAR = 9000

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


def parse_int(text: str) -> int:
    """বাংলা বা ইংরেজি অঙ্কে লেখা সংখ্যা পড়ে; ভুল হলে ValueError।"""
    return int(str(text).strip().translate(ENGLISH_DIGITS))


def _check_year(bangla_year: int) -> None:
    if not MIN_BANGLA_YEAR <= bangla_year <= MAX_BANGLA_YEAR:
        raise ValueError(
            f"বঙ্গাব্দ {bn_digits(MIN_BANGLA_YEAR)} থেকে {bn_digits(MAX_BANGLA_YEAR)}-এর মধ্যে হতে হবে"
        )


def clamp_year(bangla_year: int) -> int:
    return max(MIN_BANGLA_YEAR, min(MAX_BANGLA_YEAR, bangla_year))


def bangla_year_for_date(gregorian_date: date) -> int:
    return gregorian_date.year - (593 if (gregorian_date.month, gregorian_date.day) >= (4, 14) else 594)


def month_lengths(bangla_year: int) -> tuple[int, ...]:
    falgun_year = bangla_year + 594
    return (31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30 if calendar.isleap(falgun_year) else 29, 30)


def bangla_year_start(bangla_year: int) -> date:
    _check_year(bangla_year)
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
        raise ValueError(f"{MONTHS[month - 1]} {bn_digits(bangla_year)}-এ {bn_digits(lengths[month - 1])} দিন আছে")
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
    return (f"{bn_digits(gregorian_date.day)} {GREGORIAN_MONTHS[gregorian_date.month - 1]} "
            f"{bn_digits(gregorian_date.year)} ({WEEKDAYS[gregorian_date.weekday()]})")
