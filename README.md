# tickets

A lightweight BookMyShow ticket availability checker that sends Telegram notifications when bookings open.

## 🚀 Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

**Quick start:**

1. Fork / clone this repo
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** → select this repo
3. In the **Variables** tab, set:
   - `TELEGRAM_BOT_TOKEN` — your bot token from [@BotFather](https://t.me/BotFather)
   - `TELEGRAM_CHAT_ID` — your Telegram chat/user ID
4. Railway auto-detects `railway.json` and starts the worker — **done!**

For detailed instructions see **[README_RAILWAY.md](README_RAILWAY.md)**.

## Local Development

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in your credentials
python tickets_lite.py once # single check
python tickets_lite.py      # continuous monitoring
```