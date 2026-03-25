"""
Lightweight Ticket Checker - No Playwright Required
Uses HTTP requests + BeautifulSoup for minimal resource usage
Suitable for deployment to Railway, AWS Lambda, Heroku, or local server
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
# CONFIG
# ─────────────────────────────────────────────

URL = "https://in.bookmyshow.com/movies/hyderabad/dhurandhar-the-revenge/buytickets/ET00490584/"

TARGET_DATES = [
    "20260326",
    "20260327",
    "20260328"
]

CHECK_INTERVAL = 60  # seconds

# Telegram credentials — set via environment variables (see .env.example)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ALERT_FILE = "alert_state.json"

# ─────────────────────────────────────────────

def log(msg):
    """Print timestamped message (ISO timestamp for Railway log readability)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}", flush=True)


def send_telegram(msg):
    """Send message via Telegram"""
    if not BOT_TOKEN or not CHAT_ID:
        log("⚠️  Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url, 
            data={"chat_id": CHAT_ID, "text": msg}, 
            timeout=10
        )
        response.raise_for_status()
        log(f"✅ Telegram sent: {msg[:50]}...")
        return True
    except requests.RequestException as e:
        log(f"❌ Telegram error: {e}")
        return False


def load_state():
    """Load alert state from file to avoid duplicates"""
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log(f"⚠️  Error loading state: {e}")
            return {}
    return {}


def save_state(state):
    """Save alert state to file (best-effort — ephemeral on Railway)"""
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        log(f"⚠️  Could not save state (ephemeral filesystem?): {e}")


def fetch_page():
    """Fetch page content with proper headers and session"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-IN,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        
        # Try multiple times with retries
        for attempt in range(3):
            try:
                response = session.get(URL, timeout=15)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                if attempt < 2:
                    log(f"⚠️  Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(2)
                else:
                    raise
    
    except requests.RequestException as e:
        log(f"❌ Failed to fetch page after retries: {e}")
        return None


def parse_dates(html):
    """
    Parse HTML to find date availability
    Returns dict: {"20260326": "available", "20260327": "locked", ...}
    """
    if not html:
        return {}
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        availability = {}
        
        for date in TARGET_DATES:
            # Find the date container by ID
            container = soup.find(id=date)
            
            if not container:
                log(f"{date} container not found")
                availability[date] = "not_found"
                continue
            
            # Get the class to determine availability
            classes = container.get('class', [])
            classes_str = ' '.join(classes) if classes else ""
            
            # Check class pattern:
            # eoEOHj = AVAILABLE
            # hzcALk = NOT AVAILABLE
            if "eoEOHj" in classes_str:
                status = "available"
                log(f"✅ {date} - AVAILABLE (class: eoEOHj)")
            elif "hzcALk" in classes_str:
                status = "locked"
                log(f"❌ {date} - LOCKED (class: hzcALk)")
            else:
                status = "unknown"
                log(f"❓ {date} - UNKNOWN (class: {classes_str[:50]})")
            
            availability[date] = status
        
        return availability
    
    except Exception as e:
        log(f"❌ Error parsing HTML: {e}")
        return {}


def check_bookings():
    """
    Check for available bookings
    Returns: list of available dates
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
            log(f"{date} already alerted, skipping...")
            continue
        
        if status == "available":
            log(f"🎉 {date} BOOKINGS OPEN!")
            available.append(date)
            state[date] = True
    
    save_state(state)
    return available


def send_alerts(available_dates):
    """Send alerts for available dates"""
    if not available_dates:
        return False
    
    msg = "🎟️ TICKET BOOKING OPENED!\n\n"
    for date in available_dates:
        day = int(date[-2:])
        month = int(date[4:6])
        year = date[:4]
        msg += f"📅 {day}/{month}/{year} - BOOKINGS NOW OPEN!\n"
    
    msg += f"\n🔗 Book now: {URL}"
    
    return send_telegram(msg)


def run_once():
    """Run check once and send alerts"""
    log("🔍 Checking ticket availability...")
    
    available = check_bookings()
    
    if available:
        send_alerts(available)
        log(f"✅ Found {len(available)} available date(s)")
        return True
    else:
        log("No new available dates")
        return False


def run_continuous():
    """Run continuous monitoring loop with graceful shutdown support"""
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log(f"🚀 Ticket Checker started on Railway — {start_time}")
    log(f"Monitoring {len(TARGET_DATES)} date(s): {', '.join(TARGET_DATES)}")
    log(f"Check interval: {CHECK_INTERVAL}s | Telegram configured: {bool(BOT_TOKEN and CHAT_ID)}")
    log("Press Ctrl+C to stop\n")

    def _shutdown(signum, frame):
        log("⏹️  Received shutdown signal — stopping gracefully")
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    try:
        while True:
            try:
                run_once()
                log(f"Next check in {CHECK_INTERVAL} seconds...\n")
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
        # Run once and exit (good for cron/lambda)
        run_once()
    else:
        # Continuous monitoring
        run_continuous()
