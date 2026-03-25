import requests
import time
import json
import sys
from datetime import datetime
import os

# ─────────────────────────────────────────────
# 🎯 MOVIE CONFIG
# ─────────────────────────────────────────────

EVENT_CODE = "ET00490584"
REGION_CODE = "HYD"

TARGET_DATES = [
    "20260326",
    "20260327",
    "20260328",
    "20260329",
    "20260330"
]

VENUE_FILTER = "ALLU Cinemas"
CHECK_INTERVAL_SECONDS = 60

# ─────────────────────────────────────────────
# 🤖 TELEGRAM CONFIG
# ─────────────────────────────────────────────

BOT_TOKEN = "8751397217:AAFCGohUQ61NBJG0BDDaXNHW9PkTn09g7CU"
CHAT_ID   = "6117735395"

# ─────────────────────────────────────────────




HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://in.bookmyshow.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

ALERT_FILE = "alert_sent.json"

# ─────────────────────────────────────────────

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── TELEGRAM ─────────────────────────────────

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })
    except Exception as e:
        log(f"Telegram error: {e}")


# ── FETCH ────────────────────────────────────

def fetch_showtimes(date):
    url = "https://in.bookmyshow.com/serv/getData"
    params = {
        "cmd": "QUICKBOOK",
        "type": "MT",
        "code": EVENT_CODE,
        "mtype": "M",
        "date": date,
        "regCode": REGION_CODE,
    }

    try:
        r = SESSION.get(url, params=params, timeout=15)
        

        print("RAW RESPONSE:", r.text[:200])
        
        return r.json()
    except:
        return None

# def is_valid(show):
#     combined = " ".join([
#         str(show.get("Dim", "")),
#         str(show.get("SoundName", "")),
#         str(show.get("Experience", ""))
#     ]).lower()

#     print("DEBUG FORMAT:", combined)

#     return "2d" in combined and (
#         "dolby" in combined or
#         "cinema dolby" in combined or
#         "dolby cinema" in combined
#     )
# def has_seats(show):
#     status = (show.get("ShowStatus", "") or "").upper()

#     return status in (
#         "OPEN",          # normal available
#         "QUICK",         # fast booking
#         "AVAILABLE",     # green
#         "FAST_FILLING"   # yellow
#     )
def is_valid(show):
    combined = " ".join([
        str(show.get("Dim", "")),
        str(show.get("SoundName", "")),
        str(show.get("Experience", ""))
    ]).lower()

    print("FORMAT:", combined)

    return "2d" in combined and "dolby" in combined


def has_seats(show):
    status = (show.get("ShowStatus", "") or "").upper()

    print("STATUS:", status)

    return status not in ("SOLD OUT", "LAPSED")


# ── ALERT MEMORY ─────────────────────────────

def load_alert_state():
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_alert_state(state):
    with open(ALERT_FILE, "w") as f:
        json.dump(state, f)


# ── CHECK ────────────────────────────────────
def check():
    state = load_alert_state()
    newly_found = []

    for date in TARGET_DATES:
        if state.get(date):
            continue

        data = fetch_showtimes(date)
        if not data:
            log(f"No data for {date}")
            continue

        print("RAW DATA KEYS:", data.keys())

        # Handle BOTH structures properly
        if "BookMyShow" in data:
            venues = data["BookMyShow"].get("OuterList", [])
        elif "ShowDetails" in data:
            venues = data.get("ShowDetails", [])
        else:
            print("UNKNOWN STRUCTURE:", data)
            continue

        print(f"Found {len(venues)} venues for {date}")

        for venue in venues:
            venue_name = venue.get("VenueName", "")
            print("VENUE:", venue_name)

            # TEMP: disable filter to debug
            # if VENUE_FILTER.lower() not in venue_name.lower():
            #     continue

            shows = venue.get("InnerList", [])

            # If no InnerList, treat venue itself as show
            if not shows:
                shows = [venue]

            for show in shows:
                print("SHOW RAW:", show)

                combined = " ".join([
                    str(show.get("Dim", "")),
                    str(show.get("SoundName", "")),
                    str(show.get("Experience", ""))
                ]).lower()

                status = (show.get("ShowStatus", "") or "").upper()

                print("→", venue_name, "|", show.get("ShowTime"), "|", combined, "|", status)

                # TEMP: remove filters completely
                if status:
                    newly_found.append((date, venue_name, show.get("ShowTime")))
                    state[date] = True
                    break

    save_alert_state(state)
    return newly_found


# ── MAIN LOOP ────────────────────────────────

def main():
    log("🚀 Started Telegram Seat Checker")
    

    while True:
        results = check()

        if results:
            msg = "🎟️ Seats Open!\n\n"

            for r in results:
                msg += f"📅 {r[0]} | 🏢 {r[1]} | ⏰ {r[2]}\n"

            msg += "\nBook Now: https://in.bookmyshow.com/"

            send_telegram(msg)
            log("Alert sent on Telegram ✅")
        else:
            log("No new seats...")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Stopped")
        sys.exit(0)
