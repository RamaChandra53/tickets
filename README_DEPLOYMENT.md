# 🎟️ Ticket Checker - Complete Setup

**Status: ✅ READY TO USE**

---

## 🚀 Quick Start (Choose One)

### Option A: Simple (Recommended)
```bash
Right-click: setup_scheduler.bat
Select: Run as administrator
```
✅ Runs every hour automatically  
✅ Free, no extra software needed  
✅ 2 minutes to setup  

### Option B: Advanced (Always On)
```bash
1. Download NSSM: https://nssm.cc/download
2. Extract to: C:\nssm
3. Right-click: install_service.bat
4. Select: Run as administrator
```
✅ Runs 24/7 when PC is on  
✅ Auto-starts on boot  
✅ 15 minutes to setup  

### Option C: Professional (True 24/7)
See: **DEPLOYMENT_GUIDE.md** → Cloud section

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.md** | Decision guide - which option to choose |
| **SETUP_GUIDE.md** | How to configure the script |
| **DEPLOYMENT_GUIDE.md** | All deployment options in detail |

---

## 🔧 Scripts

| File | Purpose |
|------|---------|
| **tickets_pw.py** | Main script (uses Playwright) ⭐ |
| **tickets_lite.py** | Lightweight version (blocked by BookMyShow) |
| **run_tickets.bat** | Manual launcher (for testing) |
| **setup_scheduler.bat** | Auto-setup Task Scheduler |
| **install_service.bat** | Auto-setup Windows Service |

---

## 💾 State Files

| File | Purpose |
|------|---------|
| **alert_state.json** | Stores which dates already alerted |

---

## ✅ Features

✅ Detects ticket availability automatically  
✅ Sends Telegram notifications  
✅ No duplicate alerts  
✅ No terminal needed  
✅ Runs on schedule  

---

## 🎯 What It Does

1. **Checks BookMyShow** every hour (configurable)
2. **Detects availability** for dates 26, 27, 28 March (configurable)
3. **Sends Telegram** alert immediately
4. **Prevents duplicates** using alert_state.json

---

## 🔔 Telegram Alert

When tickets available, you get:
```
🎟️ TICKET BOOKING OPENED!

📅 26/3/2026 - BOOKINGS NOW OPEN!

🔗 Book now: https://in.bookmyshow.com/...
```

---

## 🛠️ Setup Checklist

- [ ] Choose deployment option (see QUICK_START.md)
- [ ] Run appropriate setup script
- [ ] Test first run
- [ ] Verify Telegram notification works
- [ ] Done!

---

## 📞 Troubleshooting

**Task doesn't run?**
→ See DEPLOYMENT_GUIDE.md → Troubleshooting

**No Telegram notification?**
→ Check alert_state.json for last update

**Website blocked (403)?**
→ Using Playwright (built-in to tickets_pw.py)

---

## 📖 Getting Help

1. **Choose deployment:** Read QUICK_START.md
2. **Setup issues:** See DEPLOYMENT_GUIDE.md
3. **Script questions:** Read SETUP_GUIDE.md
4. **How it works:** View tickets_pw.py code

---

## 🎬 Next Steps

1. Open **QUICK_START.md**
2. Choose your deployment method
3. Run the setup script
4. Test it
5. Get notifications! 🎉

---

**Questions?** All documentation is in markdown files.  
**Just double-click:** setup_scheduler.bat (easiest option)

---

Last updated: 2026-03-25  
Status: ✅ Fully functional
