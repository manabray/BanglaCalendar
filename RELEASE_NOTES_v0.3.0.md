# বাংলা ক্যালেন্ডার v0.3.0 — Windows, Linux ও macOS

**Manab Ray-এর উদ্যোগে, AI-এর সহায়তায় তৈরি একটি ওপেন-সোর্স বাংলা ক্যালেন্ডার।**

এই সংস্করণে Windows ও macOS desktop bundle-এর পাশাপাশি Linux-এর জন্য single-file AppImage যুক্ত করা হয়েছে।

## নতুন ও উন্নত সুবিধা
- Windows 10/11-এর জন্য `BanglaCalendar.exe`।
- Linux x86_64-এর জন্য `BanglaCalendar-x86_64.AppImage`; `linuxdeploy` দিয়ে binary-এর shared-library dependency ও desktop metadata bundle করে তৈরি। একটি ফাইল ডাউনলোড করে executable permission দিয়ে চালানো যায়।
- macOS Apple Silicon (arm64) ও Intel (x86_64)-এর জন্য আলাদা `.app` bundle।
- ক্যালেন্ডারের নিচের তথ্য-লাইন নির্বাচিত তারিখের কার্ডে রাখা হয়েছে, যাতে ছোট স্ক্রিনে লেখা কাটা না যায়।
- অ্যাপের পরিচিতি অংশে Manab Ray এবং AI-এর সহায়তার স্বচ্ছ কৃতিত্ব।
- বাংলা তারিখ, ঘড়ি, ছয় ঋতু, বাংলাদেশের ছুটির তালিকা, উইকিপিডিয়া-ভিত্তিক সার-সংক্ষেপ, তারিখ রূপান্তর এবং ব্যক্তিগত দিবসের সুবিধা বহাল।

## ডাউনলোড
- **Windows:** `BanglaCalendar.exe`
- **Linux x86_64:** `BanglaCalendar-x86_64.AppImage`
- **macOS Apple Silicon:** `BanglaCalendar-macOS-arm64.zip`
- **macOS Intel:** `BanglaCalendar-macOS-x86_64.zip`

## Linux AppImage চালানো
```bash
chmod +x BanglaCalendar-x86_64.AppImage
./BanglaCalendar-x86_64.AppImage
```

AppImage-টি Ubuntu 22.04-এ build করা হয়। Linux distribution ও system library-র পার্থক্যের কারণে কিছু সিস্টেমে অতিরিক্ত compatibility dependency প্রয়োজন হতে পারে। এই release-এ Linux ARM64 binary নেই।

## macOS নোট
macOS bundle-এর জন্য আলাদা Apple Developer ID signing ও notarization করা হয়নি। প্রথমবার চালু করতে Gatekeeper-এর সতর্কতা এলে app-এ Control-click করে **Open** নির্বাচন করতে হতে পারে।

## AI-সহায়তার কৃতিত্ব
প্রকল্পের ধারণা, নির্দেশনা, সিদ্ধান্ত, যাচাই ও রক্ষণাবেক্ষণ: **Manab Ray**। কোড, পরীক্ষা, নথি, UI এবং build workflow তৈরিতে **OpenAI ChatGPT-সহ AI-এর সহায়তা** নেওয়া হয়েছে। এটি মানুষ ও AI-এর সহযোগিতায় তৈরি প্রকল্প।

**লাইসেন্স:** অ্যাপের কোড MIT; উইকিপিডিয়া-ভিত্তিক বিবরণ সংশ্লিষ্ট attribution/CC BY-SA শর্তসহ।
