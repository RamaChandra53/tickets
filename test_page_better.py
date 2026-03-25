"""
Better page inspection - find the actual date selector
"""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://in.bookmyshow.com/movies/hyderabad/dhurandhar-the-revenge/buytickets/ET00490584/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
    )
    
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    time.sleep(5)
    
    print("\n" + "="*60)
    print("DETAILED PAGE INSPECTION")
    print("="*60)
    
    # Get ALL buttons on page
    print("\n🔍 Finding all BUTTONS on page...")
    buttons = page.query_selector_all("button")
    print(f"   Total buttons: {len(buttons)}")
    
    date_buttons = []
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text()
            if any(d in text for d in ["26", "27", "28", "MAR"]):
                classes = btn.get_attribute("class") or ""
                disabled = btn.is_disabled()
                date_buttons.append({
                    "index": i,
                    "text": text[:50],
                    "class": classes[:100],
                    "disabled": disabled
                })
                print(f"   [{i}] Text: '{text}' | Disabled: {disabled}")
        except:
            pass
    
    if date_buttons:
        print(f"\n   ✅ Found {len(date_buttons)} date-related buttons!")
    
    # Get ALL divs with "26" or "27" or "28"
    print("\n🔍 Finding divs with dates...")
    divs = page.query_selector_all("div")
    date_divs = []
    for div in divs:
        try:
            text = div.inner_text()
            if text in ["26", "27", "28"]:
                classes = div.get_attribute("class") or ""
                data_attr = div.get_attribute("data-date") or ""
                onclick = div.get_attribute("onclick") or ""
                date_divs.append({
                    "text": text,
                    "class": classes[:80],
                    "data": data_attr,
                    "onclick": onclick[:80]
                })
                print(f"   Found: {text} | Class: {classes[:60]}")
        except:
            pass
    
    # Try to find by data attributes
    print("\n🔍 Looking for date picker container...")
    containers = page.query_selector_all("[class*='calendar'], [class*='date-picker'], [class*='slot']")
    print(f"   Found {len(containers)} potential containers")
    
    # Check for specific date elements
    print("\n🔍 Direct search for '26' in page...")
    all_text = page.locator("*").all()
    found_26 = 0
    for elem in all_text[:50]:  # Check first 50 elements
        try:
            text = elem.inner_text()
            if text.strip() == "26":
                found_26 += 1
                classes = elem.get_attribute("class") or ""
                tag = elem.evaluate("e => e.tagName")
                print(f"   {tag}: '{text}' | Classes: {classes[:60]}")
        except:
            pass
    
    # Check page body HTML for patterns
    print("\n🔍 Searching page HTML for date patterns...")
    body_html = page.content()
    
    if "20260326" in body_html:
        print("   ✅ Date '20260326' found in HTML!")
    if "data-date" in body_html:
        print("   ✅ 'data-date' attribute found!")
    if "2026-03-26" in body_html:
        print("   ✅ Date '2026-03-26' found in HTML!")
    
    # Save page source for analysis
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(body_html)
    print("\n   📁 Page HTML saved to 'page_source.html'")
    
    # Print any clickable date elements
    print("\n🔍 Looking for clickable date elements...")
    clickable = page.query_selector_all("[role='button'], [onclick], a[href*='date'], a[href*='2026']")
    for i, elem in enumerate(clickable[:20]):
        try:
            text = elem.inner_text()[:30]
            href = elem.get_attribute("href") or ""
            if any(x in text or any(y in href for y in ["26", "27", "28", "2026"]) for x in ["26", "27", "28", "MAR"]):
                print(f"   [{i}] Text: {text} | Href: {href[:60]}")
        except:
            pass
    
    browser.close()

print("\n" + "="*60)
print("✅ INSPECTION COMPLETE - Check page_source.html for details")
print("="*60 + "\n")
