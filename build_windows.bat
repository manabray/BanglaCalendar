@echo off
setlocal
cd /d "%~dp0"
echo Building Bangla Calendar for Windows...
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher not found. Install Python 3.10+ from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
py -3 -m pip install --upgrade pyinstaller
if errorlevel 1 goto failed
py -3 -m PyInstaller --clean --onefile --windowed --name BanglaCalendar bangla_calendar.py
if errorlevel 1 goto failed
echo Build complete: %CD%\dist\BanglaCalendar.exe
explorer "%CD%\dist"
pause
exit /b 0
:failed
echo Build failed. Review the error above.
pause
exit /b 1
