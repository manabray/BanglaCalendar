"""Touch-friendly Kivy interface for Android (and future mobile targets)."""
from __future__ import annotations

import os
import webbrowser
from datetime import date, datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from calendar_core import (
    GREGORIAN_MONTHS, MONTHS, SEASONS, bangla_to_gregorian,
    bn_digits, format_bangla_date, format_gregorian_date,
    gregorian_to_bangla, month_lengths,
)
from holidays import OFFICIAL_HOLIDAY_SOURCE
from mobile_calendar_model import build_month_grid, selected_day_details, weekday_labels

APP_VERSION = "0.3.0"
# Use Android's Bengali system font when available; otherwise Kivy uses its bundled Roboto font.
ANDROID_BENGALI_FONT = "/system/fonts/NotoSansBengali-Regular.ttf"
MOBILE_FONT = ANDROID_BENGALI_FONT if platform == "android" and os.path.exists(ANDROID_BENGALI_FONT) else "Roboto"
PRIMARY = (0.0, 0.341, 0.557, 1)
SECONDARY = (0.0, 0.518, 0.784, 1)
ACCENT = (0.0, 0.733, 1.0, 1)
PALE = (0.875, 0.961, 1.0, 1)
BG = (0.949, 0.980, 0.996, 1)
WHITE = (1, 1, 1, 1)
TEXT = (0.071, 0.188, 0.278, 1)
MUTED = (0.345, 0.451, 0.522, 1)
HOLIDAY = (0.91, 0.95, 1.0, 1)

def ui_label(text="", size=14, color=TEXT, bold=False, height=None, halign="left"):
    label = Label(
        text=text,
        color=color,
        bold=bold,
        font_size=sp(size),
        halign=halign,
        valign="middle",
        size_hint_y=None,
        height=dp(height or 30),
        markup=True,
        font_name=MOBILE_FONT,
    )
    label.bind(size=lambda inst, _value: setattr(inst, "text_size", (inst.width - dp(4), None)))
    return label

def ui_button(text, callback, color=SECONDARY, text_color=WHITE, height=42, font_size=14):
    button = Button(
        text=text,
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_down="",
        background_color=color,
        color=text_color,
        font_size=sp(font_size),
        bold=True,
        font_name=MOBILE_FONT,
        halign="center",
        valign="middle",
    )
    button.bind(on_release=lambda *_: callback())
    return button

def card(title, background=WHITE, heading_color=PRIMARY):
    from kivy.graphics import Color, RoundedRectangle
    outer = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        height=dp(10),
        padding=(dp(12), dp(9)),
        spacing=dp(5),
    )
    with outer.canvas.before:
        outer._card_color = Color(*background)
        outer._card_shape = RoundedRectangle(pos=outer.pos, size=outer.size, radius=[dp(9)])
    def update_card(_widget, _value):
        outer._card_shape.pos = outer.pos
        outer._card_shape.size = outer.size
    outer.bind(pos=update_card, size=update_card)
    heading = ui_label(title, 15, heading_color, True, 28)
    outer.heading = heading
    outer.add_widget(heading)
    outer.bind(minimum_height=outer.setter("height"))
    return outer

def auto_label(text, size=13, color=TEXT, bold=False, background=None):
    label = Label(
        text=text,
        color=color,
        bold=bold,
        font_size=sp(size),
        halign="left",
        valign="middle",
        size_hint_y=None,
        markup=True,
        font_name=MOBILE_FONT,
    )
    label.bind(size=lambda inst, _value: setattr(inst, "text_size", (inst.width - dp(6), None)))
    label.bind(texture_size=lambda inst, value: setattr(inst, "height", value[1] + dp(8)))
    return label


class BanglaCalendarMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(6), padding=dp(7), **kwargs)
        self.view_year, self.view_month, _ = gregorian_to_bangla(date.today())
        self.selected_date = date.today()
        self._now = datetime.now()
        self._build()
        self.render()
        Clock.schedule_interval(self.update_clock, 1)

    def _build(self):
        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            padding=(dp(12), dp(6)),
            spacing=dp(8),
        )
        header.add_widget(ui_label("[b]বাংলা ক্যালেন্ডার[/b]\n[size=11]বাংলার সময়, বাংলার ঐতিহ্য[/size]", 19, WHITE, True, 46))
        about = ui_button("AI সহায়তা", self.show_about, ACCENT, PRIMARY, 38, 11)
        about.size_hint_x = None
        about.width = dp(88)
        header.add_widget(about)
        header.canvas.before.clear()
        from kivy.graphics import Color, RoundedRectangle
        with header.canvas.before:
            Color(*PRIMARY)
            self._header_bg = RoundedRectangle(pos=header.pos, size=header.size, radius=[dp(10)])
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)
        self.add_widget(header)

        self.scroller = ScrollView(do_scroll_x=False, bar_width=dp(3), scroll_type=["bars", "content"])
        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(1), dp(2), dp(1), dp(10)),
            size_hint_y=None,
        )
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroller.add_widget(self.content)
        self.add_widget(self.scroller)

        # Compact clock + today's date.
        self.clock_card = card("আজকের তারিখ ও সময়", SECONDARY, WHITE)
        self.clock_card.add_widget(ui_label("", 20, ACCENT, True, 30))
        self.clock_line = self.clock_card.children[0]
        self.today_line = auto_label("", 13, WHITE, True)
        self.clock_card.add_widget(self.today_line)
        self.content.add_widget(self.clock_card)

        # Season information.
        self.season_card = card("বাংলার ছয় ঋতু", PALE)
        self.season_line = auto_label("", 16, PRIMARY, True)
        self.season_description = auto_label("", 12, TEXT)
        self.season_card.add_widget(self.season_line)
        self.season_card.add_widget(self.season_description)
        self.content.add_widget(self.season_card)

        # Month navigation.
        nav = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(5))
        nav.add_widget(ui_button("‹ আগের", lambda: self.move_month(-1), PRIMARY, WHITE, 40, 12))
        nav.add_widget(ui_button("আজ", self.go_today, ACCENT, PRIMARY, 40, 12))
        nav.add_widget(ui_button("পরের ›", lambda: self.move_month(1), PRIMARY, WHITE, 40, 12))
        self.content.add_widget(nav)

        self.month_title = auto_label("", 21, PRIMARY, True)
        self.month_range = auto_label("", 11, MUTED)
        self.content.add_widget(self.month_title)
        self.content.add_widget(self.month_range)

        weekday_grid = GridLayout(cols=7, size_hint_y=None, height=dp(34), spacing=dp(2))
        for weekday in weekday_labels():
            weekday_grid.add_widget(Label(text=weekday, color=WHITE, bold=True, font_size=sp(10)))
        weekday_grid.canvas.before.clear()
        with weekday_grid.canvas.before:
            Color(*SECONDARY)
            self._weekday_bg = RoundedRectangle(pos=weekday_grid.pos, size=weekday_grid.size, radius=[dp(5)])
        weekday_grid.bind(pos=self._update_weekday_bg, size=self._update_weekday_bg)
        self.content.add_widget(weekday_grid)

        self.calendar_grid = GridLayout(
            cols=7,
            spacing=dp(2),
            padding=dp(2),
            size_hint_y=None,
            row_default_height=dp(62),
            row_force_default=True,
        )
        self.calendar_grid.bind(minimum_height=self.calendar_grid.setter("height"))
        self.content.add_widget(self.calendar_grid)

        # Selected day and holiday information.
        self.detail_card = card("নির্বাচিত তারিখ", WHITE)
        self.detail_date = auto_label("", 16, PRIMARY, True)
        self.detail_gregorian = auto_label("", 11, MUTED)
        self.detail_card.add_widget(self.detail_date)
        self.detail_card.add_widget(self.detail_gregorian)
        self.content.add_widget(self.detail_card)

        self.holiday_card = card("আজকের ছুটি ও দিবস", PALE, PRIMARY)
        self.holiday_content = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_y=None)
        self.holiday_content.bind(minimum_height=self.holiday_content.setter("height"))
        self.holiday_card.add_widget(self.holiday_content)
        self.content.add_widget(self.holiday_card)

        credit = auto_label(
            f"[b]BanglaCalendar v{APP_VERSION}[/b]\nManab Ray-এর উদ্যোগে, AI-এর সহায়তায় তৈরি",
            11, MUTED
        )
        credit.halign = "center"
        self.content.add_widget(credit)

    def _update_header_bg(self, widget, _value):
        self._header_bg.pos = widget.pos
        self._header_bg.size = widget.size

    def _update_weekday_bg(self, widget, _value):
        self._weekday_bg.pos = widget.pos
        self._weekday_bg.size = widget.size

    def update_clock(self, _dt):
        now = datetime.now()
        today = date.today()
        self.clock_line.text = f"[b]{bn_digits(now.strftime('%H:%M:%S'))}[/b]"
        _, month, day = gregorian_to_bangla(today)
        self.today_line.text = f"আজ {bn_digits(day)} {MONTHS[month - 1]} {bn_digits(today.year - (593 if (today.month, today.day) >= (4, 14) else 594))} বঙ্গাব্দ"

    def move_month(self, delta):
        absolute = self.view_year * 12 + self.view_month - 1 + delta
        year, month0 = divmod(absolute, 12)
        if not 1 <= year <= 9000:
            return
        self.view_year, self.view_month = year, month0 + 1
        day = min(gregorian_to_bangla(self.selected_date)[2], month_lengths(year)[self.view_month - 1])
        self.selected_date = bangla_to_gregorian(year, self.view_month, day)
        self.render()

    def go_today(self):
        self.selected_date = date.today()
        self.view_year, self.view_month, _ = gregorian_to_bangla(self.selected_date)
        self.render()
        self.scroller.scroll_y = 1

    def select_date(self, selected):
        self.selected_date = selected
        self.view_year, self.view_month, _ = gregorian_to_bangla(selected)
        self.render()

    def render(self):
        season, description = SEASONS[self.view_month]
        self.season_line.text = f"ঋতু: [b]{season}[/b]"
        self.season_description.text = description
        start = __import__("calendar_core").bangla_month_start(self.view_year, self.view_month)
        days = month_lengths(self.view_year)[self.view_month - 1]
        end = start + timedelta(days=days - 1)
        self.month_title.text = f"{MONTHS[self.view_month - 1]} {bn_digits(self.view_year)} বঙ্গাব্দ"
        self.month_range.text = (
            f"{bn_digits(start.day)} {GREGORIAN_MONTHS[start.month - 1]} {bn_digits(start.year)}"
            f" — {bn_digits(end.day)} {GREGORIAN_MONTHS[end.month - 1]} {bn_digits(end.year)}"
        )
        self.calendar_grid.clear_widgets()
        cells = build_month_grid(self.view_year, self.view_month)
        for item in cells:
            if item is None:
                cell = Button(
                    text="",
                    disabled=True,
                    background_normal="",
                    background_color=(0.96, 0.985, 0.996, 1),
                )
            else:
                selected = item["date"] == self.selected_date
                holiday = item["is_holiday"]
                observance = item["is_observance"]
                if selected:
                    color = ACCENT
                elif holiday:
                    color = HOLIDAY
                elif item["is_today"]:
                    color = PALE
                else:
                    color = WHITE
                badge = "ছুটি" if holiday else ("দিবস" if observance else ("আজ" if item["is_today"] else ""))
                badge_markup = f"\n[size=8][color=#0084C8]{badge}[/color][/size]" if badge else ""
                cell = Button(
                    text=f"[b]{item['bangla_day_text']}[/b]\n[size=8]{item['gregorian_text']}[/size]{badge_markup}",
                    markup=True,
                    halign="center",
                    valign="middle",
                    font_size=sp(12),
                    color=PRIMARY,
                    background_normal="",
                    background_down="",
                    background_color=color,
                )
                cell.bind(on_release=lambda _button, d=item["date"]: self.select_date(d))
            self.calendar_grid.add_widget(cell)

        self.detail_date.text = format_bangla_date(self.selected_date)
        self.detail_gregorian.text = format_gregorian_date(self.selected_date)
        self.render_holidays()

    def render_holidays(self):
        self.holiday_content.clear_widgets()
        details = selected_day_details(self.selected_date)
        title = "আজকের ছুটি ও দিবস" if details["is_today"] else "এই দিনের ছুটি ও দিবস"
        self.holiday_card.heading.text = title
        if not details["events"]:
            self.holiday_content.add_widget(
                auto_label("এই দিনে তালিকাভুক্ত সরকারি ছুটি বা দিবস নেই।", 12, MUTED)
            )
            return
        for event in details["events"][:3]:
            is_public = event.get("holiday", True)
            kind = "ছুটি" if is_public else "দিবস"
            self.holiday_content.add_widget(
                auto_label(f"[b]{event['name']}[/b]  [color=#0084C8]({kind})[/color]", 14, PRIMARY)
            )
            self.holiday_content.add_widget(auto_label(event.get("summary", ""), 12, TEXT))
            if event.get("wiki"):
                self.holiday_content.add_widget(
                    ui_button(
                        "উইকিপিডিয়ায় আরও পড়ুন ↗",
                        lambda url=event["wiki"]: webbrowser.open(url),
                        SECONDARY, WHITE, 36, 11,
                    )
                )

    def show_about(self):
        body = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8))
        body.add_widget(auto_label(f"[b]বাংলা ক্যালেন্ডার v{APP_VERSION}[/b]", 19, PRIMARY))
        body.add_widget(auto_label(
            "প্রকল্পের ধারণা, নির্দেশনা ও রক্ষণাবেক্ষণ: Manab Ray।\n"
            "কোড, পরীক্ষা, নথি ও প্ল্যাটফর্ম প্রস্তুতে OpenAI ChatGPT-সহ AI-এর সহায়তা নেওয়া হয়েছে।\n"
            "চূড়ান্ত সিদ্ধান্ত, যাচাই ও প্রকাশনার দায়িত্ব প্রকল্প-রক্ষণাবেক্ষণকারীর।",
            13, TEXT
        ))
        body.add_widget(ui_button(
            "GitHub Repository খুলুন ↗",
            lambda: webbrowser.open("https://github.com/manabray/BanglaCalendar"),
            PRIMARY, WHITE, 42
        ))
        popup = Popup(
            title="পরিচিতি ও কৃতিত্ব",
            content=body,
            size_hint=(0.92, 0.55),
            auto_dismiss=True,
        )
        popup.open()


class BanglaCalendarMobileApp(App):
    title = "বাংলা ক্যালেন্ডার"

    def build(self):
        self.root_widget = BanglaCalendarMobile()
        return self.root_widget


def main():
    BanglaCalendarMobileApp().run()


if __name__ == "__main__":
    main()
