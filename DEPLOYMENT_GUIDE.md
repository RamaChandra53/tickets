# Deployment Options for Ticket Checker

Since BookMyShow blocks direct HTTP requests (403 Forbidden), we need a browser automation tool. Here are your deployment options:

## Option 1: Windows Task Scheduler (BEST for your case)
**Pros:** Free, no extra costs, runs automatically on your PC schedule  
**Cons:** PC must be on, only works when scheduled

**Setup:**
1. Open `Task Scheduler` (search in Windows)
2. Create Basic Task:
   - Name: "Ticket Checker"
   - Trigger: "Daily" at your preferred time (or every hour)
   - Action: Start program
   - Program: `C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe`
   - Arguments: `tickets_pw.py once` (or remove "once" for continuous)
   - Start in: `d:\All\RC\Tech\Projects\I learn by doing`

3. Test: Right-click task → Run

**Files needed:** `tickets_pw.py` (Playwright version)

---

## Option 2: Windows Service (BETTER - Always Running)
**Pros:** Runs 24/7 when PC is on, no terminal window  
**Cons:** Requires setup, PC must stay on

**Setup using NSSM (Non-Sucking Service Manager):**

1. Download NSSM: https://nssm.cc/download
2. Extract to: `C:\nssm`
3. Open PowerShell as Admin:
```powershell
cd C:\nssm\win64
.\nssm.exe install TicketChecker "C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe" `
  "d:\All\RC\Tech\Projects\I learn by doing\tickets_pw.py"
```

4. Start service:
```powershell
.\nssm.exe start TicketChecker
```

5. Check status: Services app → "TicketChecker"

**To remove service:**
```powershell
.\nssm.exe remove TicketChecker confirm
```

---

## Option 3: Cloud Deployment (BEST for 24/7)
**Pros:** Runs 24/7, no PC needed on, professional setup  
**Cons:** Costs money (~$5-10/month)

### A. AWS Lambda (Cheapest - $0.20/million requests)
**Problem:** Lambda doesn't allow Playwright/Chrome easily. Would need:
- AWS EC2 (Elastic Cloud Compute) instead
- Cost: ~$3-5/month

### B. Railway.app (Easiest Cloud)
**Cost:** Free tier available, then ~$5/month  
**Setup:**
1. Push code to GitHub
2. Connect Railway.app
3. Add environment variables (Telegram credentials)
4. Deploy!

### C. Render.com or Heroku Alternative
Similar to Railway, ~$7-10/month

### D. DigitalOcean ($4-6/month)
Basic VPS with automatic deployment

---

## RECOMMENDED APPROACH FOR YOU

**Immediate (works now):**
1. Use `tickets_pw.py` (Playwright version)
2. Set up Windows Task Scheduler to run it hourly
3. Or keep laptop on and run: `python tickets_pw.py`

**To avoid keeping laptop on:**
1. Set up as Windows Service (NSSM - free)
2. Your PC will run it automatically when you start it

**For true 24/7 (cloud):**
1. Use Railway.app or Render.com
2. Monthly cost: ~$5-7
3. Completely hands-off

---

## Quick Setup: Windows Task Scheduler

### Create a simpler runner script first:

**File: `run_once.bat`**
```batch
@echo off
cd "d:\All\RC\Tech\Projects\I learn by doing"
set TELEGRAM_BOT_TOKEN=8751397217:AAFCGohUQ61NBJG0BDDaXNHW9PkTn09g7CU
set TELEGRAM_CHAT_ID=6117735395
"C:\Users\Virija\AppData\Local\Programs\Python\Python314\python.exe" tickets_pw.py
```

### Then in Task Scheduler:
- Program: `C:\Windows\System32\cmd.exe`
- Arguments: `/c d:\All\RC\Tech\Projects\I learn by doing\run_once.bat`
- Trigger: Every 1 hour (or on schedule)

---

## Which Option Should You Use?

| Use Case | Recommendation |
|----------|-----------------|
| Quick checks when I'm around | Just run `python tickets_pw.py` |
| Check automatically hourly | Windows Task Scheduler |
| Check 24/7, PC always on | Windows Service (NSSM) |
| Check 24/7, PC can be off | Cloud (Railway.app ~$5/mo) |

---

## Testing Your Deployment

Before deploying, test:

```bash
# Test once
python tickets_pw.py once

# Test continuous (press Ctrl+C after 2 mins)
timeout /t 120 /nobreak
python tickets_pw.py
```

Check `alert_state.json` to verify alerts are being saved.

---

## Monitoring

To check if it's running:

**Task Scheduler:**
- View task history in Task Scheduler

**Windows Service:**
```powershell
Get-Service TicketChecker
```

**Logs:**
- Check `alert_state.json` for last update time
- Check console output (if running manually)

---

## Current Setup

✅ `tickets_pw.py` - Main script (uses Playwright)
✅ `run_tickets.bat` - Launch with credentials
✅ `tickets_lite.py` - Lightweight (BUT blocked by BookMyShow 403)

**Use:** `tickets_pw.py` (it's the only one that works with BookMyShow)
