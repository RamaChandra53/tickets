# ✅ Ticket Checker - FIXED & WORKING

## What Was Fixed

### The Core Issue
The script wasn't detecting available dates correctly because:
- ❌ Was looking for `<li>` elements (breadcrumb navigation)
- ❌ Was checking wrong CSS classes that were dynamically generated
- ❌ Wasn't clicking through to date-specific pages

### The Solution
✅ Now uses the **parent container ID** to find dates:
- Each date has a parent `<div id="20260326">` 
- Checks the **parent's CSS class** to determine availability:
  - `eoEOHj` = **AVAILABLE** (bookings open!) ✅
  - `hzcALk` = **NOT AVAILABLE** (coming soon) 🔒

## How It Works Now

```
[23:59:28] 🎉 20260326 BOOKINGS OPEN! ✅       ← Detects when 26 is available
[23:59:28] 20260327 not open yet ❌             ← Correctly shows 27 as locked
[23:59:28] 20260328 not open yet ❌             ← Correctly shows 28 as locked
```

## Setup

### 1. Run the Script
```bash
python tickets_pw.py
```

Or double-click: `run_tickets.bat`

### 2. Configure Telegram (Optional but Recommended)
This will send you instant notifications when bookings open.

**Get Your Credentials:**
1. Create a Telegram bot: [@BotFather](https://t.me/BotFather)
2. Get your chat ID: [@userinfobot](https://t.me/userinfobot)

**Set Environment Variables:**

**Windows PowerShell:**
```powershell
$env:TELEGRAM_BOT_TOKEN = "your_bot_token_here"
$env:TELEGRAM_CHAT_ID = "your_chat_id_here"
```

**Windows Command Prompt:**
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
python tickets_pw.py
```

**Or create a `.env` file:**
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Customize Dates/Movie
Edit `tickets_pw.py`:
```python
URL = "https://in.bookmyshow.com/..."  # Change movie

TARGET_DATES = [
    "20260326",  # Format: YYYYMMDD
    "20260327",
    "20260328"
]

CHECK_INTERVAL = 60  # Check every 60 seconds
```

## Features

✅ **Accurate Detection** - Checks parent container class pattern  
✅ **No Duplicates** - Remembers which dates already alerted (`alert_state.json`)  
✅ **Smart Status Tracking** - Shows OPEN ✅ or LOCKED 🔒 for each date  
✅ **Instant Notifications** - Telegram alerts when bookings open  
✅ **Continuous Monitoring** - Checks every 60 seconds (configurable)  
✅ **Graceful Shutdown** - Press Ctrl+C to stop cleanly  

## What Gets Saved

- **alert_state.json** - Tracks which dates have been announced (prevents duplicate alerts)

## To Stop

Press `Ctrl+C` in the terminal

## Troubleshooting

**"No bookings available yet..."**
- This is normal - checking every 60 seconds
- Wait for 27 or 28 to show availability

**"Telegram credentials not configured"**
- Alerts will print to console but not send via Telegram
- Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to enable

**"Container NOT found"**
- Movie page changed structure
- Need to re-inspect HTML (run test scripts to debug)

## Files

- `tickets_pw.py` - Main script (FIXED)
- `TICKETS_README.md` - Documentation
- `SETUP_GUIDE.md` - This file
- `run_tickets.bat` - Quick launcher for Windows
- `alert_state.json` - Alert history (auto-created)

---

**Status: ✅ FULLY WORKING & TESTED**
