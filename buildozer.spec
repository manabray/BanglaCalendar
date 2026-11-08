[app]

title = BanglaCalendar
package.name = banglacalendar
package.domain = org.manabray

source.dir = .
source.include_exts = py,kv,atlas,png,jpg,jpeg,ttf,otf,json,txt
source.exclude_dirs = .git,.github,.buildozer,bin,build,dist,tests,__pycache__

version = 0.3.0

# Android uses the dedicated touch-first Kivy entry point (main.py).
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

# Android 6+; arm64 is the primary target and armeabi-v7a keeps older devices usable.
android.minapi = 23
android.api = 35
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.debug_artifact = apk
android.release_artifact = aab

# No network permission is needed for calendar calculation; links open in the browser.
android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
