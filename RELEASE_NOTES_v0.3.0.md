# বাংলা ক্যালেন্ডার v0.3.0 — Windows, Linux, macOS ও Android

**Manab Ray-এর উদ্যোগে, AI-এর সহায়তায় তৈরি একটি ওপেন-সোর্স বাংলা ক্যালেন্ডার।**

এই সংস্করণে Windows/Linux ডেস্কটপ অ্যাপের পাশাপাশি macOS desktop bundle এবং Android-এর জন্য touch-first Kivy interface যোগ করা হয়েছে।

## নতুন ও উন্নত সুবিধা
- macOS Apple Silicon (arm64) ও Intel (x86_64)-এর জন্য আলাদা `.app` bundle।
- Android ফোনের জন্য portrait-mode Kivy UI, touch-friendly calendar grid, month navigation, digital clock, ছয় ঋতু, তারিখের তথ্য এবং holiday/observance summary।
- Android UI ও desktop UI একই `calendar_core.py` এবং `holidays.py` ব্যবহার করে; বাংলা তারিখের হিসাবের নিয়ম অভিন্ন।
- ক্যালেন্ডারের নিচের তথ্য-লাইন নির্বাচিত তারিখের কার্ডে রাখা হয়েছে, যাতে ছোট স্ক্রিনে লেখা কাটা না যায়।
- অ্যাপের পরিচিতি অংশে Manab Ray এবং AI-এর সহায়তার স্বচ্ছ কৃতিত্ব।
- আগের Windows ও Linux build বহাল।

## ডাউনলোড
- **Windows:** `BanglaCalendar.exe`
- **Linux x86_64:** `BanglaCalendar-Linux-x86_64.tar.gz`
- **macOS Apple Silicon:** `BanglaCalendar-macOS-arm64.zip`
- **macOS Intel:** `BanglaCalendar-macOS-x86_64.zip`
- **Android:** `BanglaCalendar-Android-debug.apk`

## Android নোট
APK-টি debug/sideload build; Google Play Store-এর production release নয়। Play Store-এ প্রকাশের আগে release signing, AAB, app signing key, privacy/policy review এবং Play Console submission প্রয়োজন। Android ARM64 ও armeabi-v7a build করা হয়েছে।

## macOS নোট
macOS bundle-এর জন্য আলাদা Apple Developer ID signing ও notarization করা হয়নি। প্রথমবার চালু করতে Gatekeeper-এর সতর্কতা এলে app-এ Control-click করে **Open** নির্বাচন করতে হতে পারে।

## AI-সহায়তার কৃতিত্ব
প্রকল্পের ধারণা, নির্দেশনা, সিদ্ধান্ত, যাচাই ও রক্ষণাবেক্ষণ: **Manab Ray**। কোড, পরীক্ষা, নথি, UI এবং build workflow তৈরিতে **OpenAI ChatGPT-সহ AI-এর সহায়তা** নেওয়া হয়েছে। এটি মানুষ ও AI-এর সহযোগিতায় তৈরি প্রকল্প।

**লাইসেন্স:** অ্যাপের কোড MIT; উইকিপিডিয়া-ভিত্তিক বিবরণ সংশ্লিষ্ট attribution/CC BY-SA শর্তসহ।
