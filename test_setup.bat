@echo off
REM ============================================
REM  Test Ticket Checker Setup
REM ============================================

echo.
echo Testing Ticket Checker Setup...
echo.

setlocal enabledelayedexpansion

set PYTHON=C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe
set SCRIPT_PATH=d:\All\RC\Tech\Projects\I learn by doing\tickets_pw.py
set SCRIPT_DIR=d:\All\RC\Tech\Projects\I learn by doing

echo Step 1: Checking Python installation...
if exist "%PYTHON%" (
    echo ✅ Python found: %PYTHON%
) else (
    echo ❌ Python NOT found!
    echo Please install Python or update the path in this script.
    pause
    exit /b 1
)

echo.
echo Step 2: Checking required files...
if exist "%SCRIPT_PATH%" (
    echo ✅ Script found: %SCRIPT_PATH%
) else (
    echo ❌ Script NOT found!
    pause
    exit /b 1
)

echo.
echo Step 3: Running single check...
echo ============================================
echo.

cd /d "%SCRIPT_DIR%"

REM Set credentials
set TELEGRAM_BOT_TOKEN=8751397217:AAFCGohUQ61NBJG0BDDaXNHW9PkTn09g7CU
set TELEGRAM_CHAT_ID=6117735395

REM Run once
"%PYTHON%" "%SCRIPT_PATH%" once

echo.
echo ============================================
echo.

if %errorLevel% equ 0 (
    echo ✅ TEST SUCCESSFUL!
    echo.
    echo The ticket checker works correctly.
    echo.
    echo Check alert_state.json:
    if exist "alert_state.json" (
        echo.
        type alert_state.json
        echo.
    )
    echo.
    echo Next step: Run setup_scheduler.bat (or install_service.bat)
) else (
    echo ❌ TEST FAILED!
    echo.
    echo Error occurred. Check the output above for details.
)

echo.
pause
