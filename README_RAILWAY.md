# Railway Deployment Guide — Ticket Checker 🚀

Deploy `tickets_lite.py` to Railway for 24/7 remote monitoring with Telegram notifications.

---

## Prerequisites

### 1. Telegram Bot Setup

1. Open Telegram and message **[@BotFather](https://t.me/botfather)**
2. Send `/newbot` and follow the prompts to create your bot
3. Copy the **bot token** (looks like `123456:ABC-DEF...`)
4. Start a chat with your new bot, then visit:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
5. Send any message to your bot, then refresh the URL above
6. Copy your **chat ID** from the `"id"` field in the response

---

## Railway Deployment

### Step 1: Create a Railway Account

Go to [railway.app](https://railway.app) and sign up (GitHub login recommended).

### Step 2: Create a New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub account
4. Select the `RamaChandra53/tickets` repository

### Step 3: Configure Environment Variables

In your Railway project dashboard:

1. Click on your service
2. Go to the **"Variables"** tab
3. Add the following variables:

| Variable | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |

### Step 4: Deploy

Railway automatically detects the `Procfile` and deploys the worker. Your app will start running immediately after the environment variables are set.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Telegram bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | ✅ Yes | Your Telegram user or group chat ID |

> ⚠️ **Never commit your actual credentials to the repository.** Use Railway's Variables tab to set secrets securely.

---

## Monitoring

### View Logs

In the Railway dashboard:
1. Click on your service
2. Go to the **"Logs"** tab
3. You will see real-time output like:
   ```
   [2026-03-25 18:00:00] 🚀 Ticket Checker started — 2026-03-25 18:00:00
   [2026-03-25 18:00:00] Monitoring 5 date(s): 20260326, 20260327, ...
   [2026-03-25 18:00:01] Fetching page...
   [2026-03-25 18:00:02] 🔒 20260326 — LOCKED
   [2026-03-25 18:00:02] No new available dates
   [2026-03-25 18:00:02] Next check in 60s...
   ```

### Service Health

- Railway restarts the worker automatically if it crashes
- Check the **"Metrics"** tab for CPU and memory usage
- The app uses ~30–50 MB RAM (well within Railway's free tier limit of 512 MB)

---

## Troubleshooting

### No Telegram notifications received

- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set correctly in Railway Variables
- Make sure you have sent at least one message to your bot before deploying
- Check Railway logs for `❌ Telegram error:` messages

### Service keeps restarting

- Check Railway logs for Python errors or missing dependencies
- Ensure `requirements.txt` is present in the repository root
- Confirm the `Procfile` contains: `worker: python tickets_lite.py`

### Dates not found / unknown status

- BookMyShow may have updated their HTML structure
- Check Railway logs for `❓ ... UNKNOWN (class: ...)` messages
- Update the CSS class names in `tickets_lite.py` (`eoEOHj` / `hzcALk`) to match the current site

---

## Local Testing

Before deploying, test the app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variable template
cp .env.example .env

# Edit .env with your actual credentials
# TELEGRAM_BOT_TOKEN=your_actual_token
# TELEGRAM_CHAT_ID=your_actual_chat_id

# Run a single check
python tickets_lite.py once

# Run continuously (Ctrl+C to stop)
python tickets_lite.py
```

---

## File Overview

| File | Purpose |
|---|---|
| `tickets_lite.py` | Main application — unified lightweight scraper with Telegram alerts |
| `requirements.txt` | Python dependencies for Railway |
| `Procfile` | Tells Railway how to start the worker |
| `.env.example` | Template for required environment variables |

---

## Why `tickets_lite.py` for Railway?

| Feature | `tickets_lite.py` |
|---|---|
| Memory usage | ~30–50 MB |
| Startup time | 1–2 seconds |
| Railway free tier | ✅ Compatible (well under 512 MB limit) |
| Dependencies | requests, beautifulsoup4, python-dotenv |
| Credentials | Environment variables only |
| Venue filter | ✅ Configurable via `VENUE_FILTER` |
| Browser required | ❌ None — pure HTTP requests |
