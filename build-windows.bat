@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python 3 was not found. Install Python 3.10 or newer, then run this file again.
    pause
    exit /b 1
)

py -3 -m pip install --upgrade pyinstaller
if errorlevel 1 goto :failed

py -3 build.py
if errorlevel 1 goto :failed

echo.
echo Build complete: dist\OptiStore.exe
echo Copy OptiStore.exe to any Windows PC and double-click it to start.
pause
exit /b 0

:failed
echo.
echo Build failed. Check the error above and try again.
pause
exit /b 1
