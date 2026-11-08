"""Mobile-friendly calendar view model shared by the Kivy Android app."""
from __future__ import annotations

from datetime import date, timedelta
from calendar_core import (
    GREGORIAN_SHORT,
    WEEKDAY_SHORT,
    bangla_month_start,
    bn_digits,
    month_lengths,
)
from holidays import get_holidays_for_date


def build_month_grid(year: int, month: int, today: date | None = None) -> list[dict | None]:
    """Return exactly 42 Sunday-first slots for a Bangla month."""
    if not 1 <= month <= 12:
        raise ValueError("বাংলা মাস ১ থেকে ১২-এর মধ্যে হতে হবে")
    today = today or date.today()
    start = bangla_month_start(year, month)
    offset = (start.weekday() + 1) % 7
    days = month_lengths(year)[month - 1]
    slots: list[dict | None] = [None] * offset
    for day in range(1, days + 1):
        gregorian = start + timedelta(days=day - 1)
        events = get_holidays_for_date(gregorian)
        public_holidays = [event for event in events if event.get("holiday", True)]
        observances = [event for event in events if not event.get("holiday", True)]
        slots.append({
            "date": gregorian,
            "bangla_day": day,
            "bangla_day_text": bn_digits(day),
            "gregorian_text": f"{bn_digits(gregorian.day)} {GREGORIAN_SHORT[gregorian.month - 1]}",
            "is_today": gregorian == today,
            "is_holiday": bool(public_holidays),
            "is_observance": bool(observances),
            "holiday_names": [event["name"] for event in public_holidays],
            "observance_names": [event["name"] for event in observances],
            "events": events,
        })
    slots.extend([None] * (42 - len(slots)))
    return slots


def selected_day_details(selected: date) -> dict:
    """Return structured date and holiday details for the mobile detail panel."""
    events = get_holidays_for_date(selected)
    return {
        "date": selected,
        "is_today": selected == date.today(),
        "events": events,
        "holidays": [event for event in events if event.get("holiday", True)],
        "observances": [event for event in events if not event.get("holiday", True)],
    }


def weekday_labels() -> tuple[str, ...]:
    return tuple(WEEKDAY_SHORT)
