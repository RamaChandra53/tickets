"""
Unified Ticket Checker — Lightweight, Railway-ready
Uses HTTP requests + BeautifulSoup (no browser required).
Sends Telegram notifications when BookMyShow bookings open.

Usage:
  python tickets_lite.py          # continuous monitoring (default)
  python tickets_lite.py once     # single check then exit (cron/Lambda)

Environment variables (see .env.example):
  TELEGRAM_BOT_TOKEN   — Telegram bot token from @BotFather
  TELEGRAM_CHAT_ID     — Your Telegram user/group chat ID
"""
import signal
import sys
import time
import json
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG  — edit these to match your event
# ─────────────────────────────────────────────

# BookMyShow buy-tickets page URL
URL = "https://in.bookmyshow.com/movies/hyderabad/dhurandhar-the-revenge/buytickets/ET00490584/"

# Dates to monitor (YYYYMMDD format)
TARGET_DATES = [
    "20260326",
    "20260327",
    "20260328",
    "20260329",
    "20260330",
]

# Optional: only alert for shows at this venue (set to "" to disable)
VENUE_FILTER = "ALLU Cinemas"

# How often to check, in seconds
CHECK_INTERVAL = 60

# ─────────────────────────────────────────────
# TELEGRAM  — loaded from environment variables
# ─────────────────────────────────────────────

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ─────────────────────────────────────────────
# STATE FILE  — tracks which dates already alerted
# ─────────────────────────────────────────────

ALERT_FILE = "alert_state.json"

# ─────────────────────────────────────────────


def log(msg):
    """ISO-timestamped log line (flush=True keeps Railway logs streaming)."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}", flush=True)


# ── TELEGRAM ─────────────────────────────────

def send_telegram(msg):
    """Send a message via Telegram. Returns True on success."""
    if not BOT_TOKEN or not CHAT_ID:
        log("⚠️  Telegram credentials not configured — set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10,
        )
        response.raise_for_status()
        log(f"✅ Telegram sent: {msg[:60]}...")
        return True
    except requests.RequestException as e:
        log(f"❌ Telegram error: {e}")
        return False


# ── STATE PERSISTENCE ────────────────────────

def load_state():
    """Load alert state from file to avoid duplicate notifications."""
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log(f"⚠️  Error loading state: {e}")
    return {}


def save_state(state):
    """Save alert state (best-effort — Railway filesystem is ephemeral)."""
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        log(f"⚠️  Could not save state (ephemeral filesystem?): {e}")


# ── PAGE FETCH ───────────────────────────────

def fetch_page():
    """Fetch the BookMyShow page HTML with browser-like headers and retries."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    session = requests.Session()
    session.headers.update(headers)

    for attempt in range(1, 4):
        try:
            response = session.get(URL, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt < 3:
                log(f"⚠️  Attempt {attempt} failed: {e} — retrying...")
                time.sleep(2)
            else:
                log(f"❌ Failed to fetch page after 3 attempts: {e}")
                return None


# ── HTML PARSING ─────────────────────────────

def parse_dates(html):
    """
    Parse page HTML to determine availability of each target date.

    BookMyShow marks date containers with:
      class containing "eoEOHj" → bookings OPEN
      class containing "hzcALk" → bookings LOCKED / not yet open

    Returns a dict: {"20260326": "available" | "locked" | "not_found" | "unknown"}
    """
    if not html:
        return {}

    try:
        soup = BeautifulSoup(html, "html.parser")
        availability = {}

        for date in TARGET_DATES:
            container = soup.find(id=date)

            if not container:
                log(f"  {date} — container not found on page")
                availability[date] = "not_found"
                continue

            classes_str = " ".join(container.get("class", []))

            if "eoEOHj" in classes_str:
                log(f"  ✅ {date} — AVAILABLE")
                availability[date] = "available"
            elif "hzcALk" in classes_str:
                log(f"  🔒 {date} — LOCKED")
                availability[date] = "locked"
            else:
                log(f"  ❓ {date} — UNKNOWN class: {classes_str[:60]}")
                availability[date] = "unknown"

        return availability

    except Exception as e:
        log(f"❌ Error parsing HTML: {e}")
        return {}


# ── BOOKING CHECK ────────────────────────────

def check_bookings():
    """
    Fetch the page and return a list of newly-available dates that
    haven't already triggered an alert.
    """
    state = load_state()
    available = []

    log("Fetching page...")
    html = fetch_page()
    if not html:
        return available

    log("Parsing dates...")
    availability = parse_dates(html)

    for date, status in availability.items():
        if state.get(date):
            log(f"  {date} — already alerted, skipping")
            continue
        if status == "available":
            log(f"🎉 {date} — BOOKINGS OPEN!")
            available.append(date)
            state[date] = True

    save_state(state)
    return available


# ── ALERT ────────────────────────────────────

def send_alerts(available_dates):
    """Build and send a Telegram alert for all newly-available dates."""
    if not available_dates:
        return False

    msg = "🎟️ TICKET BOOKING OPENED!\n\n"
    for date in available_dates:
        day = int(date[6:8])
        month = int(date[4:6])
        year = date[:4]
        msg += f"📅 {day}/{month}/{year} — BOOKINGS NOW OPEN!\n"

    if VENUE_FILTER:
        msg += f"\n🏢 Venue: {VENUE_FILTER}"

    msg += f"\n\n🔗 Book now: {URL}"

    return send_telegram(msg)


# ── RUN MODES ────────────────────────────────

def run_once():
    """Run a single availability check and send alerts if needed."""
    log("🔍 Checking ticket availability...")

    available = check_bookings()

    if available:
        send_alerts(available)
        log(f"✅ Found {len(available)} newly-available date(s)")
        return True

    log("No new available dates")
    return False


def run_continuous():
    """Run continuous monitoring with graceful SIGTERM/SIGINT shutdown."""
    log(f"🚀 Ticket Checker started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Monitoring {len(TARGET_DATES)} date(s): {', '.join(TARGET_DATES)}")
    if VENUE_FILTER:
        log(f"Venue filter: {VENUE_FILTER}")
    log(f"Check interval: {CHECK_INTERVAL}s | Telegram configured: {bool(BOT_TOKEN and CHAT_ID)}")
    log("─" * 60)

    def _shutdown(signum, frame):
        log("⏹️  Received shutdown signal — stopping gracefully")
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    try:
        while True:
            try:
                run_once()
                log(f"Next check in {CHECK_INTERVAL}s...\n")
                time.sleep(CHECK_INTERVAL)
            except SystemExit:
                raise
            except Exception as e:
                log(f"❌ Error in check loop: {e}")
                time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        log("⏹️  Stopped")


# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        run_once()
    else:
        run_continuous()
