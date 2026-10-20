"""Bangladesh public-holiday data and Wikipedia-attributed summaries.

Calendar dates for 2026 follow the Bangladesh Ministry of Public Administration
holiday circular. Other years show recurring fixed-date holidays only until their
government circular is added. Wikipedia is used for short descriptions, not as
the authority for official holiday dates.
"""
from __future__ import annotations
from datetime import date

OFFICIAL_HOLIDAY_SOURCE = (
    "https://mopa.gov.bd/pages/public-holiday/"
    "%E0%A7%A8%E0%A7%A6%E0%A7%A8%E0%A7%AC-%E0%A6%96%E0%A7%8D%E0%A6%B0%E0%A6%BF%E0%A6%B7%E0%A7%8D%E0%A6%9F%E0%A6%BE%E0%A6%AC%E0%A7%8D%E0%A6%A6%E0%A7%87%E0%A6%B0-%E0%A6%9B%E0%A7%81%E0%A6%9F%E0%A6%BF%E0%A6%B0-%E0%A6%A4%E0%A6%BE%E0%A6%B2%E0%A6%BF%E0%A6%95%E0%A6%BE%E0%A6%B0-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%9C%E0%A7%8D%E0%A6%9E%E0%A6%BE%E0%A6%AA%E0%A6%A8-2df487-694139b2a31054345f0e6346"
)
OFFICIAL_HOLIDAY_PDF = (
    "https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.oraclecloud15.com/"
    "n/axvjbnqprylg/b/V2Ministry/o/office-mopa/2024/12/209c6283d9234a0fa8f1f30b90068b57.pdf"
)
WIKIPEDIA_PUBLIC_HOLIDAYS = "https://en.wikipedia.org/wiki/Public_holidays_in_Bangladesh"

# Short summaries below are independently paraphrased from the linked Wikipedia
# articles. Those summaries are attribution-noted CC BY-SA material; code remains MIT.
HOLIDAYS = [
    # Fixed-date annual holidays. For dates that vary by year, use that year's
    # official government circular instead of assuming a date here.
    {"annual": "02-21", "name": "শহীদ দিবস ও আন্তর্জাতিক মাতৃভাষা দিবস",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "১৯৫২ সালের ভাষা আন্দোলনে বাংলাকে রাষ্ট্রভাষা করার দাবিতে আন্দোলনকারীদের আত্মত্যাগ স্মরণ করা হয়। দিনটি বিশ্বজুড়ে আন্তর্জাতিক মাতৃভাষা দিবস হিসেবেও পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Bengali_language_movement"},
    {"annual": "03-26", "name": "স্বাধীনতা ও জাতীয় দিবস",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "১৯৭১ সালে বাংলাদেশের স্বাধীনতার ঘোষণা ও মুক্তিযুদ্ধের সূচনাকে স্মরণ করে এই জাতীয় দিবস পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Independence_Day_(Bangladesh)"},
    {"annual": "04-14", "name": "পহেলা বৈশাখ",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "বাংলা নববর্ষের প্রথম দিন। শোভাযাত্রা, মেলা, সাংস্কৃতিক অনুষ্ঠান এবং হালখাতার মাধ্যমে নানা ধর্মের মানুষ দিনটি উদ্‌যাপন করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Pohela_Boishakh"},
    {"annual": "05-01", "name": "মে দিবস / আন্তর্জাতিক শ্রমিক দিবস",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "শ্রমিকদের অধিকার, ন্যায্য কর্মপরিবেশ ও শ্রমিক আন্দোলনের ইতিহাস স্মরণে আন্তর্জাতিকভাবে দিনটি পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/International_Workers%27_Day"},
    {"annual": "08-05", "name": "জুলাই গণ-অভ্যুত্থান দিবস",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "বাংলাদেশের ২০২৪ সালের জুলাই-আগস্ট গণ-অভ্যুত্থান ও তার ঐতিহাসিক প্রভাব স্মরণে দিবসটি পালন করা হয়।",
     "wiki": "https://en.wikipedia.org/wiki/2024_Bangladesh_quota_reform_movement"},
    {"annual": "12-16", "name": "বিজয় দিবস",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "১৯৭১ সালের ১৬ ডিসেম্বর পাকিস্তানি বাহিনীর আত্মসমর্পণ ও বাংলাদেশের মুক্তিযুদ্ধে চূড়ান্ত বিজয় স্মরণ করা হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Victory_Day_(Bangladesh)"},
    {"annual": "12-25", "name": "যিশুখ্রিষ্টের জন্মদিন (বড়দিন)",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "খ্রিস্টান সম্প্রদায় যিশুখ্রিষ্টের জন্ম উদ্‌যাপন করেন। বাংলাদেশে দিনটি বড়দিন নামে পরিচিত।",
     "wiki": "https://en.wikipedia.org/wiki/Christmas"},

    # Additional 2026 general holidays and leave days from the government circular.
    {"start": "2026-02-04", "end": "2026-02-04", "name": "শবে বরাত",
     "category": "নির্বাহী আদেশে সরকারি ছুটি",
     "summary": "ইসলামী ঐতিহ্যে শাবান মাসের মধ্যরাতের এই উপলক্ষ ইবাদত, দোয়া ও ক্ষমা প্রার্থনার সঙ্গে যুক্ত।",
     "wiki": "https://en.wikipedia.org/wiki/Mid-Sha%27ban"},
    {"start": "2026-01-23", "end": "2026-01-23", "name": "সরস্বতী পূজা",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "বিদ্যা, সংগীত ও শিল্পকলার দেবী সরস্বতীর আরাধনায় শিক্ষার্থী ও ভক্তরা পূজা করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Vasant_Panchami"},
    {"start": "2026-02-01", "end": "2026-02-01", "name": "মাঘী পূর্ণিমা",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "বৌদ্ধ সম্প্রদায়ের ধর্মীয় আচার, প্রার্থনা ও দানের সঙ্গে যুক্ত একটি পূর্ণিমা উপলক্ষ।",
     "wiki": "https://en.wikipedia.org/wiki/Magha_Purnima"},
    {"start": "2026-02-15", "end": "2026-02-15", "name": "শিবরাত্রি ব্রত",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "শিবের উদ্দেশে উপবাস, প্রার্থনা ও রাত্রিজাগরণের মাধ্যমে মহাশিবরাত্রি পালন করা হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Maha_Shivaratri"},
    {"start": "2026-01-17", "end": "2026-01-17", "name": "শবে মেরাজ",
     "category": "ঐচ্ছিক ছুটি — মুসলিম ধর্ম",
     "summary": "ইসলামী বিশ্বাসে মুহাম্মদের রাত্রিকালীন সফর ও ঊর্ধ্বারোহণের স্মারক উপলক্ষ।",
     "wiki": "https://en.wikipedia.org/wiki/Isra%27_and_Mi%27raj"},
    {"start": "2026-02-18", "end": "2026-02-18", "name": "ভস্ম বুধবার",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "পশ্চিমা খ্রিস্টীয় ধারায় লেন্ট বা উপবাস-প্রার্থনার সময়ের সূচনা হিসেবে দিনটি পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Ash_Wednesday"},
    {"start": "2026-03-03", "end": "2026-03-03", "name": "দোলযাত্রা",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "রঙ, গান ও ধর্মীয় আচারসহ পালিত হিন্দু বসন্তোৎসব; অনেক অঞ্চলে হোলির সঙ্গে সম্পর্কিত।",
     "wiki": "https://en.wikipedia.org/wiki/Holi"},
    {"start": "2026-03-17", "end": "2026-03-17", "name": "পবিত্র শবে কদর",
     "category": "নির্বাহী আদেশে সরকারি ছুটি",
     "summary": "রমজানের শেষ দশকের এক বিশেষ পবিত্র রাত, যা কুরআন নাজিলের সঙ্গে সম্পর্কিত বলে ইসলামে গভীর গুরুত্ব বহন করে।",
     "wiki": "https://en.wikipedia.org/wiki/Laylat_al-Qadr"},
    {"start": "2026-03-17", "end": "2026-03-17", "name": "হরিচাঁদ ঠাকুরের আবির্ভাব",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "মতুয়া ধর্মীয় আন্দোলনের প্রতিষ্ঠাতা হরিচাঁদ ঠাকুরের জন্ম ও শিক্ষাকে স্মরণ করে ভক্তরা দিনটি পালন করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Harichand_Thakur"},
    {"start": "2026-03-19", "end": "2026-03-23", "name": "ঈদুল ফিতরের ছুটি",
     "category": "সরকারি ছুটি — ২০২৬ সালের নির্ধারিত সময়",
     "summary": "রমজান মাসের রোজা শেষে শাওয়াল মাসের শুরুতে ঈদুল ফিতর পালিত হয়। ঈদের নামাজ, আত্মীয়-স্বজনের সঙ্গে সাক্ষাৎ, দান ও খাবার ভাগাভাগি এর গুরুত্বপূর্ণ অংশ। তারিখ চাঁদ দেখার ওপর নির্ভরশীল হতে পারে।",
     "wiki": "https://en.wikipedia.org/wiki/Eid_al-Fitr"},
    {"start": "2026-03-20", "end": "2026-03-20", "name": "জুমাতুল বিদা",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "রমজানের শেষ শুক্রবারে মুসলিমরা বিশেষ জুমার নামাজ ও প্রার্থনায় অংশ নেন।",
     "wiki": "https://en.wikipedia.org/wiki/Jumu%27at_al-Wida"},
    {"start": "2026-04-12", "end": "2026-04-15", "name": "বৈসাবি ও পার্বত্য উৎসব",
     "category": "বিশেষ ছুটি — পার্বত্য চট্টগ্রাম ও সংশ্লিষ্ট জনগোষ্ঠী",
     "summary": "পার্বত্য চট্টগ্রামের বিভিন্ন জাতিগোষ্ঠী নববর্ষ ও নতুন ঋতুকে কেন্দ্র করে বৈসাবি-সহ নানা ঐতিহ্যবাহী উৎসব পালন করেন। নির্দিষ্ট ছুটির প্রযোজ্যতা অঞ্চল ও সম্প্রদায়ভেদে আলাদা হতে পারে।",
     "wiki": "https://en.wikipedia.org/wiki/Biju_(festival)"},
    {"start": "2026-04-02", "end": "2026-04-02", "name": "পুণ্য বৃহস্পতিবার",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "খ্রিস্টান ঐতিহ্যে যিশুর শেষ নৈশভোজের স্মরণে পবিত্র সপ্তাহের বৃহস্পতিবার পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Maundy_Thursday"},
    {"start": "2026-04-03", "end": "2026-04-03", "name": "পুণ্য শুক্রবার",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "যিশুখ্রিষ্টের ক্রুশবিদ্ধ হওয়ার স্মরণে খ্রিস্টানরা প্রার্থনা ও ধর্মীয় আচার পালন করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Good_Friday"},
    {"start": "2026-04-04", "end": "2026-04-04", "name": "পুণ্য শনিবার",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "পবিত্র শনিবার হলো গুড ফ্রাইডে ও ইস্টার রবিবারের মাঝের খ্রিস্টীয় পালনদিবস।",
     "wiki": "https://en.wikipedia.org/wiki/Holy_Saturday"},
    {"start": "2026-04-05", "end": "2026-04-05", "name": "ইস্টার সানডে",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "খ্রিস্টান বিশ্বাসে যিশুখ্রিষ্টের পুনরুত্থান উদ্‌যাপনের প্রধান উৎসব।",
     "wiki": "https://en.wikipedia.org/wiki/Easter"},
    {"start": "2026-04-30", "end": "2026-04-30", "name": "বুদ্ধ পূর্ণিমার আগের দিন",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "বুদ্ধ পূর্ণিমা গৌতম বুদ্ধের জীবন, জ্ঞানলাভ ও শিক্ষার স্মরণের সঙ্গে যুক্ত; সরকার নির্ধারিত সূচিতে আগের দিনের ঐচ্ছিক ছুটিও রয়েছে।",
     "wiki": "https://en.wikipedia.org/wiki/Vesak"},
    {"start": "2026-05-01", "end": "2026-05-01", "name": "বুদ্ধ পূর্ণিমা",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "বৌদ্ধ সম্প্রদায় গৌতম বুদ্ধের জন্ম, বোধিলাভ ও মহাপরিনির্বাণের স্মরণে প্রার্থনা, দান ও ধর্মীয় অনুষ্ঠান করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Vesak"},
    {"start": "2026-05-02", "end": "2026-05-02", "name": "বুদ্ধ পূর্ণিমার পরের দিন",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "২০২৬ সালের সরকারি সূচিতে বুদ্ধ পূর্ণিমার পরের দিনের ঐচ্ছিক ছুটি হিসেবে তালিকাভুক্ত।",
     "wiki": "https://en.wikipedia.org/wiki/Vesak"},
    {"start": "2026-05-26", "end": "2026-05-31", "name": "ঈদুল আজহার ছুটি",
     "category": "সরকারি ছুটি — ২০২৬ সালের নির্ধারিত সময়",
     "summary": "ঈদুল আজহা ত্যাগ ও আল্লাহর প্রতি আনুগত্যের স্মারক উৎসব। ইব্রাহিমের কোরবানি-সংক্রান্ত ইসলামী ঐতিহ্য থেকে এর তাৎপর্য এসেছে; মুসলিমরা নামাজ, কোরবানি ও খাবার ভাগাভাগি করেন। তারিখ চাঁদ দেখার ওপর নির্ভরশীল হতে পারে।",
     "wiki": "https://en.wikipedia.org/wiki/Eid_al-Adha"},
    {"start": "2026-06-01", "end": "2026-06-01", "name": "ঈদুল আজহার পরবর্তী ঐচ্ছিক ছুটি",
     "category": "ঐচ্ছিক ছুটি — মুসলিম ধর্ম",
     "summary": "২০২৬ সালের সরকারি সূচিতে ঈদুল আজহার পরবর্তী দিনের ঐচ্ছিক ছুটি হিসেবে তালিকাভুক্ত।",
     "wiki": "https://en.wikipedia.org/wiki/Eid_al-Adha"},
    {"start": "2026-06-26", "end": "2026-06-26", "name": "আশুরা",
     "category": "নির্বাহী আদেশে সরকারি ছুটি",
     "summary": "মুহাররমের দশম দিনে পালিত আশুরা বিভিন্ন মুসলিম ধারায় ভিন্ন ঐতিহাসিক তাৎপর্য বহন করে; বিশেষভাবে কারবালার ঘটনা স্মরণ করা হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Ashura"},
    {"start": "2026-06-29", "end": "2026-06-29", "name": "আষাঢ়ী পূর্ণিমা",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "থেরবাদী বৌদ্ধ ঐতিহ্যে বর্ষাবাস ও বুদ্ধের শিক্ষার স্মরণে পালিত একটি পূর্ণিমা।",
     "wiki": "https://en.wikipedia.org/wiki/Asalha_Puja"},
    {"start": "2026-08-26", "end": "2026-08-26", "name": "ঈদে মিলাদুন্নবী (সা.)",
     "category": "নির্বাহী আদেশে সরকারি ছুটি",
     "summary": "মাওলিদ নামে পরিচিত এই উপলক্ষে অনেক মুসলিম নবী মুহাম্মদের জন্ম স্মরণে আলোচনা, দোয়া ও ধর্মীয় সমাবেশ করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Mawlid"},
    {"start": "2026-09-04", "end": "2026-09-04", "name": "জন্মাষ্টমী",
     "category": "সাধারণ সরকারি ছুটি",
     "summary": "হিন্দু ধর্মে কৃষ্ণের জন্মোৎসব হিসেবে জন্মাষ্টমী পালিত হয়; ভক্তরা উপবাস, পূজা, কীর্তন ও ধর্মীয় অনুষ্ঠান করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Krishna_Janmashtami"},
    {"start": "2026-09-26", "end": "2026-09-26", "name": "মধু পূর্ণিমা",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "বৌদ্ধ ঐতিহ্যে মধু পূর্ণিমা দান, সহমর্মিতা ও পারস্পরিক সহায়তার কাহিনির সঙ্গে যুক্ত।",
     "wiki": "https://en.wikipedia.org/wiki/Madhu_Purnima"},
    {"start": "2026-10-10", "end": "2026-10-10", "name": "মহালয়া",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "দুর্গাপূজার সূচনার সঙ্গে সম্পর্কিত মহালয়ায় ভক্তরা পূর্বপুরুষদের স্মরণ এবং দেবীপক্ষের আগমন উপলক্ষে আচার পালন করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Mahalaya"},
    {"start": "2026-10-18", "end": "2026-10-19", "name": "দুর্গাপূজা — সপ্তমী ও অষ্টমী",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "দুর্গাপূজা দেবী দুর্গার উপাসনা, সাংস্কৃতিক অনুষ্ঠান ও সম্প্রদায়ের সমাবেশের প্রধান হিন্দু উৎসব।",
     "wiki": "https://en.wikipedia.org/wiki/Durga_Puja"},
    {"start": "2026-10-20", "end": "2026-10-20", "name": "দুর্গাপূজা — নবমী",
     "category": "নির্বাহী আদেশে সরকারি ছুটি",
     "summary": "দুর্গাপূজার নবমী তিথিতে দেবী দুর্গার পূজা ও উৎসবের আচার পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Durga_Puja"},
    {"start": "2026-10-21", "end": "2026-10-21", "name": "বিজয়া দশমী",
     "category": "সাধারণ সরকারি ছুটি — ২০২৬",
     "summary": "দুর্গাপূজার সমাপ্তি উপলক্ষে বিজয়া দশমী পালিত হয়; প্রচলিত কাহিনিতে দেবী দুর্গার মহিষাসুরের ওপর বিজয় স্মরণ করা হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Vijayadashami"},
    {"start": "2026-10-25", "end": "2026-10-25", "name": "লক্ষ্মী পূজা",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "হিন্দু ঐতিহ্যে লক্ষ্মী পূজা সমৃদ্ধি ও সৌভাগ্যের দেবী লক্ষ্মীর আরাধনা হিসেবে পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Lakshmi_Puja"},
    {"start": "2026-10-25", "end": "2026-10-25", "name": "প্রবারণা পূর্ণিমা",
     "category": "ঐচ্ছিক ছুটি — বৌদ্ধ ধর্ম",
     "summary": "বৌদ্ধ বর্ষাবাসের সমাপ্তির সঙ্গে সম্পর্কিত এই দিনে ভিক্ষু ও গৃহীরা ধর্মীয় আচার পালন করেন।",
     "wiki": "https://en.wikipedia.org/wiki/Pavarana"},
    {"start": "2026-11-08", "end": "2026-11-08", "name": "শ্যামা পূজা / কালী পূজা",
     "category": "ঐচ্ছিক ছুটি — হিন্দু ধর্ম",
     "summary": "কালী দেবীর উপাসনা, প্রদীপ জ্বালানো ও নানা ধর্মীয় আচারসহ শ্যামা বা কালী পূজা পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Kali_Puja"},
    {"start": "2026-12-24", "end": "2026-12-24", "name": "বড়দিনের আগের দিন",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "বড়দিনের আগের সন্ধ্যা ও দিনটি অনেক খ্রিস্টান পরিবারে গির্জার অনুষ্ঠান ও পারিবারিক উদ্‌যাপনের মাধ্যমে পালিত হয়।",
     "wiki": "https://en.wikipedia.org/wiki/Christmas_Eve"},
    {"start": "2026-12-26", "end": "2026-12-26", "name": "বড়দিনের পরের দিন",
     "category": "ঐচ্ছিক ছুটি — খ্রিস্টান ধর্ম",
     "summary": "২০২৬ সালের সরকারি সূচিতে বড়দিনের পরের দিন খ্রিস্টান কর্মচারীদের ঐচ্ছিক ছুটি হিসেবে তালিকাভুক্ত।",
     "wiki": "https://en.wikipedia.org/wiki/Christmas"}
]

def _date_for_event(event: dict, year: int) -> tuple[date, date] | None:
    if "annual" in event:
        month, day = (int(part) for part in event["annual"].split("-"))
        try:
            event_date = date(year, month, day)
        except ValueError:
            return None
        return event_date, event_date
    start = date.fromisoformat(event["start"])
    end = date.fromisoformat(event.get("end", event["start"]))
    if start.year <= year <= end.year:
        if start.year < year:
            start = date(year, 1, 1)
        if end.year > year:
            end = date(year, 12, 31)
        return start, end
    return None

def holidays_for_year(year: int) -> list[dict]:
    """Return holiday events relevant to a Gregorian year, sorted by date."""
    result = []
    for event in HOLIDAYS:
        span = _date_for_event(event, year)
        if span is None:
            continue
        item = dict(event)
        item["start_date"], item["end_date"] = span
        result.append(item)
    result.sort(key=lambda item: (item["start_date"], item["name"]))
    return result

def holidays_for_date(target: date) -> list[dict]:
    """Return all holiday/optional-leave records overlapping a given day."""
    return [
        event for event in holidays_for_year(target.year)
        if event["start_date"] <= target <= event["end_date"]
    ]

def is_holiday(target: date) -> bool:
    return bool(holidays_for_date(target))
