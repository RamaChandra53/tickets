@echo off
REM Quick start script for tickets_pw.py

echo.
echo ========================================
echo  Ticket Availability Checker
echo ========================================
echo.

REM Set Telegram credentials
set TELEGRAM_BOT_TOKEN=8751397217:AAFCGohUQ61NBJG0BDDaXNHW9PkTn09g7CU
set TELEGRAM_CHAT_ID=6117735395

echo Credentials loaded. Starting checker...
echo.

REM Run the script with correct Python
"C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe" "%~dp0tickets_pw.py"

pause
