@echo off
REM ============================================
REM  Setup Ticket Checker in Windows Task Scheduler
REM ============================================

setlocal enabledelayedexpansion

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script must run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

set PYTHON=C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe
set SCRIPT_PATH=d:\All\RC\Tech\Projects\I learn by doing\tickets_pw.py
set TASK_NAME=TicketChecker

echo.
echo ============================================
echo  Setting up Windows Task Scheduler
echo ============================================
echo.

REM Delete existing task if present
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

echo Creating task: %TASK_NAME%
echo Script: %SCRIPT_PATH%
echo.

REM Create the task to run every hour
schtasks /create /tn "%TASK_NAME%" /tr "%PYTHON% %SCRIPT_PATH%" /sc hourly /every 1 /f

if %errorLevel% equ 0 (
    echo.
    echo ============================================
    echo SUCCESS! Task created in Task Scheduler
    echo ============================================
    echo.
    echo Task Details:
    echo   Name: %TASK_NAME%
    echo   Frequency: Every hour
    echo   Script: %SCRIPT_PATH%
    echo.
    echo The task will:
    echo   - Run automatically every hour
    echo   - Check for available tickets
    echo   - Send Telegram notification if found
    echo.
    echo To modify the task:
    echo   1. Open Task Scheduler (search in Windows)
    echo   2. Find "%TASK_NAME%"
    echo   3. Right-click Properties to change schedule
    echo.
    echo To remove the task:
    echo   schtasks /delete /tn "%TASK_NAME%" /f
    echo.
) else (
    echo ERROR: Could not create task scheduler entry
    echo Please run this script as Administrator
)

pause
