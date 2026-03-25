import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

URL = "https://in.bookmyshow.com/movies/hyderabad/dhurandhar-the-revenge/buytickets/ET00490584/"

TARGET_DATES = [
    "20260326",
    "20260327",
    "20260328"
]

CHECK_INTERVAL = 60

# Load credentials from environment variables for security
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ALERT_FILE = "alert_state.json"
FIRST_RUN = False  # Set to False to use saved state (avoid duplicate alerts)

# ─────────────────────────────────────────────

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── TELEGRAM ─────────────────────────────────

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        log("⚠️  Telegram credentials not configured (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        log(f"❌ Telegram error: {e}")


# ── ALERT MEMORY ─────────────────────────────

def load_state():
    """Load alert state from file to avoid duplicate notifications."""
    if FIRST_RUN:
        return {}
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log(f"⚠️  Could not load state file: {e}")
            return {}
    return {}

def save_state(state):
    """Save alert state to file."""
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        log(f"❌ Could not save state file: {e}")


# ── MAIN CHECK ───────────────────────────────
def check(page):
    """Check for available booking dates on the page."""
    state = load_state()
    found = []

    try:
        page.goto(URL, wait_until="domcontentloaded")
        time.sleep(3)

        for date in TARGET_DATES:
            if state.get(date):
                log(f"{date} already alerted, skipping...")
                continue

            day = str(int(date[-2:]))
            log(f"Checking date: {day}")

            try:
                # Find the parent container by ID
                # The structure is: <div id="20260326" class="...">
                # CSS selector needs escaping for numeric IDs
                container = page.query_selector(f'[id="{date}"]')
                
                if not container:
                    log(f"{date} container NOT found on page ❌")
                    continue
                
                # Get the parent's class to determine availability
                parent_classes = container.get_attribute("class") or ""
                
                # Class patterns:
                # eoEOHj = AVAILABLE (seen on 26 when bookings are open)
                # hzcALk = NOT AVAILABLE (seen on future dates)
                # eLqqSC or other = different states
                
                is_available = "eoEOHj" in parent_classes
                
                log(f"DATE: {date} | PARENT CLASS: {parent_classes} | STATUS: {'OPEN ✅' if is_available else 'LOCKED 🔒'}")

                if not is_available:
                    log(f"{date} not open yet ❌")
                    continue

                # Booking is OPEN!
                log(f"🎉 {date} BOOKINGS OPEN! ✅")
                found.append((date, "BOOKING OPEN 🎟️", ""))
                state[date] = True

            except Exception as e:
                log(f"Error checking {date}: {e}")
                continue

        save_state(state)
    except Exception as e:
        log(f"❌ Page check error: {e}")

    return found

# ── MAIN LOOP ────────────────────────────────

def main():
    """Main loop to continuously check for available bookings."""
    log("🚀 Playwright Seat Checker Started")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-IN"
        )

        page = context.new_page()
        try:
            while True:
                try:
                    results = check(page)

                    if results:
                        msg = "🎟️ Booking Opened!\n\n"
                        for r in results:
                            msg += f"📅 {r[0]} | ⏰ {r[1]} | {r[2]}\n"

                        send_telegram(msg)
                        log("Alert sent ✅")
                    else:
                        log("No bookings available yet...")

                    time.sleep(CHECK_INTERVAL)
                except Exception as e:
                    log(f"❌ Check error: {e}")
                    time.sleep(10)
        except KeyboardInterrupt:
            log("⏹️  Stopped by user")
        finally:
            page.close()
            context.close()
            browser.close()
            log("🛑 Browser closed")


if __name__ == "__main__":
    main()