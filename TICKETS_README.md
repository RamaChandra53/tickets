# Ticket Availability Checker (Playwright)

A booking availability checker for BookMyShow that uses Playwright to monitor ticket availability and sends alerts via Telegram.

## Improvements Made

✅ **Security**: Removed hardcoded credentials, now uses environment variables  
✅ **Error Handling**: Replaced bare `except` clauses with specific exception handling  
✅ **Dependencies**: Removed unused `random` import  
✅ **Code Quality**: Added docstrings to all functions  
✅ **Robustness**: Enhanced error handling in check() and state management  
✅ **Logging**: Improved log messages with consistent emoji indicators  
✅ **Page Loading**: Added `wait_until="domcontentloaded"` for reliability  

## Setup

### 1. Install Dependencies
```bash
pip install playwright requests
python -m playwright install chromium
```

### 2. Configure Telegram (Optional)
To receive alerts, set environment variables:

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN = "your_bot_token"
$env:TELEGRAM_CHAT_ID = "your_chat_id"
```

**Windows (Command Prompt):**
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token
set TELEGRAM_CHAT_ID=your_chat_id
```

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

Or create a `.env` file and load before running.

### 3. Configure Target Dates
Edit `TARGET_DATES` in the script to monitor specific dates:
```python
TARGET_DATES = [
    "20260326",  # Format: YYYYMMDD
    "20260327",
    "20260328"
]
```

## Usage

```bash
python tickets_pw.py
```

The script will:
- Open a browser window and navigate to the booking page
- Check for availability every 60 seconds (configurable via `CHECK_INTERVAL`)
- Log availability status with timestamps
- Send Telegram alerts when dates become available
- Avoid duplicate alerts by tracking state in `alert_state.json`

## How It Works

1. **State Tracking**: Uses `alert_state.json` to remember which dates have been announced as available
2. **Date Matching**: Looks for dates in the format "WED\n25\nMAR" and extracts the day number
3. **Availability Check**: Inspects CSS classes for "disabled" or "past" indicators
4. **Notifications**: Sends formatted messages via Telegram if configured

## Stopping

Press `Ctrl+C` to gracefully stop the checker. The browser will close automatically.

## Notes

- Browser runs in non-headless mode (visible window) for debugging
- Includes anti-automation detection bypass flags
- User-Agent mimics standard Chrome browser
- Locale set to India (en-IN)
