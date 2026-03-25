# 🎯 Quick Deployment Decision Guide

## Your Goal: Run checker without keeping terminal/laptop on

---

## 📊 Comparison Table

| Method | Setup Time | Cost | Runs 24/7 | Requires PC On | Best For |
|--------|-----------|------|----------|--------|----------|
| **Task Scheduler** | 2 min | Free | ❌ No | ✅ Yes | Hourly checks |
| **Windows Service** | 15 min | Free | ✅ Yes | ✅ Yes | Always on (when PC is on) |
| **Cloud (Railway)** | 10 min | $5/mo | ✅ Yes | ❌ No | True 24/7 monitoring |

---

## 🎯 Choose Your Setup

### A) "I'll keep my PC on and want simple" 
→ **Use: Task Scheduler** ✅
- Runs every hour automatically
- No terminal needed
- Simple 2-minute setup
- **Run:** `setup_scheduler.bat` (as admin)

### B) "My PC is always on, I want it always checking"
→ **Use: Windows Service** ✅✅
- Runs 24/7 when PC is on
- Auto-starts on boot
- Runs in background silently
- **Requires:** Download NSSM first (free)
- **Run:** `install_service.bat` (as admin)

### C) "I want true 24/7 even if my PC is off"
→ **Use: Cloud (Railway.app)** ✅✅✅
- Runs 24/7 always
- No PC needed
- Professional setup
- **Cost:** ~$5/month
- **Requires:** GitHub account (free)
- **See:** DEPLOYMENT_GUIDE.md for full steps

---

## 🚀 Recommended for You: Task Scheduler

**Why?**
- ✅ Fastest setup (2 minutes)
- ✅ Free (no cost)
- ✅ Simple (no learning curve)
- ✅ Works (runs every hour)
- ⚠️ Only if you keep PC on

**Setup:**
```
1. Right-click: setup_scheduler.bat
2. Select: "Run as administrator"
3. Press Enter
4. Done!
```

**What happens:**
- Runs every hour automatically
- Checks for available tickets
- Sends Telegram notification if found
- No terminal/console visible

---

## 📱 After Setup, You'll Get:

✅ Telegram notification when tickets available
✅ No need to check manually
✅ Automatic checking every hour
✅ Alert saved to `alert_state.json`

---

## 🛠️ How to Modify Schedule

Once set up via Task Scheduler:

1. Open Windows Start Menu
2. Search: "Task Scheduler"
3. Find: "TicketChecker"
4. Right-click → Properties
5. Change "Triggers" tab:
   - **Every 30 minutes** = More frequent checks
   - **Every 2 hours** = Less frequent (saves PC resources)
   - **At 10:00 AM daily** = Once per day

---

## 🔧 Troubleshooting

**Task doesn't run?**
- Check: Task Scheduler → TicketChecker → Right-click → Run
- Should see browser open briefly

**No Telegram notification?**
- Check: `alert_state.json` file
- Should show `{"20260326": true}` if triggered

**Service won't start?**
- Ensure PC has good internet
- Restart the service: Services app → TicketChecker → Restart

---

## 📞 Support

**Questions?** Check these files:
- `DEPLOYMENT_GUIDE.md` - Full deployment guide
- `SETUP_GUIDE.md` - How the script works
- `tickets_pw.py` - The main script

**Files you have:**
- `tickets_pw.py` - Main checker (Playwright)
- `tickets_lite.py` - Lightweight version (blocked by BookMyShow)
- `run_tickets.bat` - Manual launcher
- `setup_scheduler.bat` - Auto setup Task Scheduler
- `install_service.bat` - Auto setup Windows Service

---

## Next Steps

**Do this now:**

1. **Choose your option:**
   - Task Scheduler (simplest) → Run `setup_scheduler.bat`
   - Windows Service (always-on) → Download NSSM, run `install_service.bat`
   - Cloud (true 24/7) → See DEPLOYMENT_GUIDE.md

2. **Test:**
   - Wait for first scheduled run
   - Or manually trigger in Task Scheduler
   - Check `alert_state.json` for results

3. **Verify Telegram:**
   - When bookings available → Check phone for notification
   - Should get: "🎟️ Booking Opened!"

---

Good luck! You've got this! 🎟️
