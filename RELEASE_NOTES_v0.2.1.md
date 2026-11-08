# বাংলা ক্যালেন্ডার v0.2.1

Windows ও Linux-এর জন্য বিনামূল্যের ওপেন-সোর্স বাংলা ক্যালেন্ডারের আপডেট।

## নতুন ও উন্নত সুবিধা
- ক্যালেন্ডারের নিচের তথ্য-লাইন এখন নির্বাচিত তারিখের কার্ডের ভেতরে রাখা হয়েছে, যাতে ছোট স্ক্রিনেও লেখা কাটা না যায়।
- ছোট স্ক্রিনে উইন্ডোর উচ্চতা ও ন্যূনতম উচ্চতা আরও ভালোভাবে মানিয়ে নেওয়া হয়েছে।
- Windows-এর জন্য `BanglaCalendar.exe`।
- Linux x86_64-এর জন্য standalone PyInstaller executable-সহ `BanglaCalendar-Linux-x86_64.tar.gz`; archive-এ চালানোর script ও Linux নির্দেশিকা রয়েছে।
- আগের সংস্করণের বাংলা/ইংরেজি তারিখ, ডিজিটাল ঘড়ি, ছয় ঋতু, ছুটির তথ্য, তারিখ রূপান্তর ও ব্যক্তিগত দিবসের সুবিধা বহাল।

## Windows
Release asset থেকে `BanglaCalendar.exe` ডাউনলোড করে চালান। Python লাগবে না।

## Linux (x86_64)
`BanglaCalendar-Linux-x86_64.tar.gz` Extract করুন এবং Terminal থেকে:

```bash
./run-banglacalendar.sh
```

প্যাকেজটি Ubuntu 22.04 runner-এ build করা হয়েছে। অন্য Linux distribution-এ system library-এর পার্থক্যের কারণে অতিরিক্ত dependency লাগতে পারে। ARM64 এই release-এর আওতায় নেই।

## যাচাই
Release workflow-এ Windows ও Ubuntu 22.04—দুই পরিবেশেই calendar test চালিয়ে তারপর binary তৈরি করা হবে।

**লাইসেন্স:** অ্যাপের কোড MIT; উইকিপিডিয়া-ভিত্তিক সংক্ষিপ্ত বিবরণ সংশ্লিষ্ট attribution/CC BY-SA শর্তসহ।
