@echo off
REM ============================================
REM  Install Ticket Checker as Windows Service
REM ============================================
REM  Requires NSSM (Non-Sucking Service Manager)
REM  Download from: https://nssm.cc/download
REM ============================================

setlocal enabledelayedexpansion

echo.
echo Checking for NSSM installation...

if not exist "C:\nssm\win64\nssm.exe" (
    echo.
    echo ERROR: NSSM not found at C:\nssm\win64\nssm.exe
    echo.
    echo Please download NSSM first:
    echo 1. Go to https://nssm.cc/download
    echo 2. Download the latest version
    echo 3. Extract to C:\nssm
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script must run as Administrator!
    echo.
    echo Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

set PYTHON=C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe
set SCRIPT_PATH=d:\All\RC\Tech\Projects\I learn by doing\tickets_pw.py
set SCRIPT_DIR=d:\All\RC\Tech\Projects\I learn by doing
set SERVICE_NAME=TicketChecker
set NSSM=C:\nssm\win64\nssm.exe

echo.
echo Installing %SERVICE_NAME% as Windows Service...
echo.

REM Set environment variables for the service
echo Setting credentials in Windows registry...
"%NSSM%" set %SERVICE_NAME% AppEnvironmentExtra TELEGRAM_BOT_TOKEN=8751397217:AAFCGohUQ61NBJG0BDDaXNHW9PkTn09g7CU
"%NSSM%" set %SERVICE_NAME% AppEnvironmentExtra TELEGRAM_CHAT_ID=6117735395

REM Install the service
echo Installing service...
"%NSSM%" install %SERVICE_NAME% "%PYTHON%" "%SCRIPT_PATH%"

if %errorLevel% equ 0 (
    echo.
    echo ============================================
    echo SUCCESS! Service installed.
    echo ============================================
    echo.
    echo Now starting the service...
    "%NSSM%" start %SERVICE_NAME%
    
    if %errorLevel% equ 0 (
        echo.
        echo SERVICE STARTED SUCCESSFULLY!
        echo.
        echo The ticket checker is now running as a Windows Service.
        echo It will start automatically when Windows boots.
        echo.
        echo Management:
        echo   - Start:  "%NSSM%" start %SERVICE_NAME%
        echo   - Stop:   "%NSSM%" stop %SERVICE_NAME%
        echo   - Remove: "%NSSM%" remove %SERVICE_NAME% confirm
        echo.
    ) else (
        echo ERROR: Could not start service
    )
) else (
    echo ERROR: Could not install service
)

pause
