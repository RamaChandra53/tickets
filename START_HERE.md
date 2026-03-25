# 🎟️ BookMyShow Ticket Checker - Complete Setup Guide

**Status:** ✅ **READY TO DEPLOY**

---

## 📌 TL;DR (Too Long; Didn't Read)

**Your question:** How do I deploy without keeping terminal/laptop on?

**Answer:** 
1. Right-click `setup_scheduler.bat`
2. Select "Run as administrator"
3. Done! Runs every hour automatically

**When bookings open:** Get Telegram notification 📱

---

## 📚 Documentation (Read in Order)

| # | File | Purpose |
|---|------|---------|
| 1️⃣ | **DEPLOYMENT_SUMMARY.md** | 👈 START HERE - Overview of all options |
| 2️⃣ | **QUICK_START.md** | Which deployment option should you use? |
| 3️⃣ | **DEPLOYMENT_GUIDE.md** | Detailed step-by-step for each option |
| 4️⃣ | **SETUP_GUIDE.md** | How to configure the script |

---

## 🚀 Quick Setup (Recommended)

### Windows Task Scheduler
**Setup time:** 2 minutes  
**Cost:** Free  
**Runs:** Every hour  

```bash
Right-click: setup_scheduler.bat
Select: Run as administrator
```

---

## 🔧 Main Scripts

| File | Purpose | Use When |
|------|---------|----------|
| **tickets_pw.py** | Main checker | Core functionality |
| **tickets_lite.py** | Lightweight (HTTP) | Won't work (blocked by BookMyShow) |
| **run_tickets.bat** | Manual launcher | Testing/debugging |

---

## ⚙️ Setup/Deployment Scripts

| File | Purpose |
|------|---------|
| **setup_scheduler.bat** | ⭐ Easiest - Auto setup Task Scheduler |
| **install_service.bat** | Advanced - Setup Windows Service (requires NSSM) |
| **test_setup.bat** | Verify everything works |

---

## 📂 State Files (Auto-created)

| File | Purpose |
|------|---------|
| **alert_state.json** | Tracks which dates already alerted |

---

## 3️⃣ Deployment Options

### Option 1: Windows Task Scheduler ⭐ (RECOMMENDED)
- **Setup:** 2 minutes
- **Cost:** Free
- **Runs:** Every hour
- **Best for:** Most users
- **Setup:** `setup_scheduler.bat`

### Option 2: Windows Service (Better)
- **Setup:** 15 minutes
- **Cost:** Free
- **Runs:** 24/7 when PC on
- **Best for:** Always-on PC
- **Setup:** `install_service.bat` (requires NSSM)

### Option 3: Cloud Deployment (Professional)
- **Setup:** 10 minutes
- **Cost:** ~$5-7/month
- **Runs:** 24/7 always
- **Best for:** 24/7 monitoring without PC
- **Details:** See DEPLOYMENT_GUIDE.md

---

## ✅ What It Does

1. **Checks BookMyShow** every hour (configurable)
2. **Detects availability** for March 26, 27, 28 (configurable)
3. **Sends Telegram notification** instantly
4. **Prevents duplicates** using alert_state.json

---

## 📱 Telegram Notification

When tickets available, you receive:
```
🎟️ TICKET BOOKING OPENED!

📅 26/3/2026 - BOOKINGS NOW OPEN!

🔗 Book now: https://in.bookmyshow.com/...
```

---

## 🎯 Getting Started

### Step 1: Choose Your Deployment
- **I want simplest:** Task Scheduler (Option 1)
- **I want always-on:** Windows Service (Option 2)
- **I want 24/7 without PC:** Cloud (Option 3)

### Step 2: Read Documentation
- Open `DEPLOYMENT_SUMMARY.md`
- Choose your option
- Follow setup steps

### Step 3: Run Setup
- Run the appropriate `.bat` file
- Select "Run as administrator"
- Done!

### Step 4: Test
- Run `test_setup.bat`
- Verify it works
- Check `alert_state.json`

---

## 🔍 Features

✅ Accurate ticket detection  
✅ Instant Telegram alerts  
✅ No duplicate notifications  
✅ Automatic hourly checks  
✅ No terminal needed  
✅ Minimal CPU/memory usage  
✅ Configurable dates and frequency  

---

## ⚡ The Fastest Way (2 minutes)

```
1. Right-click setup_scheduler.bat
2. Select "Run as administrator"
3. Press Enter
4. ✅ Done! Checker runs every hour
```

---

## 📞 Troubleshooting

**Doesn't run?**
- Check Task Scheduler → TicketChecker → Right-click → Run
- Verify PC was on at scheduled time

**No notification?**
- Check `alert_state.json`
- Verify Telegram credentials
- Run `test_setup.bat`

**Need help?**
- Read `DEPLOYMENT_GUIDE.md`
- Check `SETUP_GUIDE.md`
- See `QUICK_START.md`

---

## 📖 Complete File List

### Documentation
- `README_DEPLOYMENT.md` - Index and quick reference
- `DEPLOYMENT_SUMMARY.md` - Overview of options
- `QUICK_START.md` - Decision guide
- `DEPLOYMENT_GUIDE.md` - Detailed setup
- `SETUP_GUIDE.md` - Configuration help
- `TICKETS_README.md` - Feature reference

### Scripts
- `tickets_pw.py` - Main checker (Playwright)
- `tickets_lite.py` - Lightweight (HTTP only)
- `run_tickets.bat` - Manual launcher

### Setup Tools
- `setup_scheduler.bat` - Auto-setup Task Scheduler
- `install_service.bat` - Auto-setup Windows Service
- `test_setup.bat` - Verify setup

### State Files
- `alert_state.json` - Alert history (auto-created)

---

## 🎬 Next Steps

1. **Right now:** Open `DEPLOYMENT_SUMMARY.md`
2. **In 2 minutes:** Run `setup_scheduler.bat`
3. **Then:** Wait for first hourly run or manually trigger
4. **Finally:** Get Telegram notification when tickets available

---

## ✨ Result

✅ Automatic ticket monitoring 24/7  
✅ No terminal visible  
✅ Instant notifications  
✅ Zero maintenance  

---

**You're all set! Good luck with ticket booking! 🎟️**

---

**Version:** 1.0  
**Last Updated:** 2026-03-25  
**Status:** ✅ Production Ready
