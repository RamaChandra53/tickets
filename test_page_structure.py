"""
Quick script to inspect page structure and test logic
"""
import time
from playwright.sync_api import sync_playwright

URL = "https://in.bookmyshow.com/movies/hyderabad/dhurandhar-the-revenge/buytickets/ET00490584/"
TARGET_DATE = "20260326"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        locale="en-IN"
    )
    
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    time.sleep(3)
    
    print("\n=== PAGE STRUCTURE INSPECTION ===\n")
    
    # Check for date buttons
    print("1️⃣  Looking for date selector elements...")
    
    # Try different selectors
    date_buttons = page.locator("button, [role='button'], li, div").filter(has_text="26").all()
    print(f"   Found {len(date_buttons)} elements with '26'")
    
    # Look for all li elements
    all_li = page.locator("li").all()
    print(f"   Total <li> elements: {len(all_li)}")
    
    # Print first 10 li elements
    print("\n2️⃣  First 10 <li> elements:")
    for i, li in enumerate(all_li[:10]):
        try:
            text = li.inner_text()
            classes = li.get_attribute("class") or ""
            print(f"   [{i}] Classes: {classes[:50]}")
            print(f"       Text: {text[:80]}")
        except:
            pass
    
    # Look for date picker / calendar
    print("\n3️⃣  Looking for date picker container...")
    date_container = page.locator("[class*='date'], [class*='Date'], [class*='calendar'], [class*='Calendar']").first
    if date_container:
        print(f"   Found date container")
        text = date_container.inner_text()
        print(f"   Content: {text[:200]}")
    
    # Check what happens when we click
    print("\n4️⃣  Attempting to interact with dates...")
    
    # Try finding clickable date element for 26
    try:
        elem_26 = None
        for li in all_li:
            try:
                text = li.inner_text()
                if "26" in text and "MAR" in text:
                    elem_26 = li
                    print(f"   ✅ Found element for 26 MAR")
                    print(f"   Text: {text}")
                    print(f"   Classes: {li.get_attribute('class')}")
                    print(f"   Is disabled: {'disabled' in (li.get_attribute('class') or '').lower()}")
                    
                    # Try clicking it
                    if li.is_visible():
                        print(f"   Element is visible, attempting click...")
                        li.click()
                        time.sleep(2)
                        print(f"   ✅ Clicked successfully")
                        
                        # Check URL change
                        new_url = page.url
                        print(f"   Current URL: {new_url}")
                    break
            except:
                pass
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check page URL and content after interaction
    print("\n5️⃣  Checking page state after interaction...")
    print(f"   URL: {page.url}")
    
    # Look for booking status text
    booking_status = page.locator("text=/book|available|sold|open/i").first
    if booking_status:
        print(f"   Booking status: {booking_status.inner_text()}")
    
    browser.close()

print("\n=== INSPECTION COMPLETE ===\n")
