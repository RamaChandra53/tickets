"""
Capture REAL class names and determine the availability pattern
"""
import time
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
    
    # Get all divs
    all_divs = page.query_selector_all("div")
    
    print("\n" + "="*70)
    print("REAL CLASS NAMES FOR EACH DATE")
    print("="*70)
    
    for target_day in [26, 27, 28, 29, 30, 31]:
        for div in all_divs:
            try:
                text = div.inner_text().strip()
                if text == str(target_day):
                    classes = div.get_attribute("class") or ""
                    print(f"Day {target_day}: {classes}")
                    break
            except:
                pass
    
    # Now check: is there a pattern for which dates are available?
    # Let me look at the parent container or siblings
    print("\n" + "="*70)
    print("CHECKING IF DATES ARE CLICKABLE")
    print("="*70)
    
    for target_day in [26, 27, 28]:
        for div in all_divs:
            try:
                text = div.inner_text().strip()
                if text == str(target_day):
                    is_visible = div.is_visible()
                    is_enabled = div.is_enabled()
                    is_disabled = div.is_disabled() if hasattr(div, 'is_disabled') else False
                    
                    # Check parent
                    parent = div.evaluate("e => e.parentElement.className")
                    
                    # Check if clickable
                    try:
                        div.click(timeout=100)
                        clickable = True
                    except:
                        clickable = False
                    
                    print(f"Day {target_day}:")
                    print(f"  Visible: {is_visible}")
                    print(f"  Enabled: {is_enabled}")
                    print(f"  Clickable: {clickable}")
                    print(f"  Parent class: {parent}")
                    
                    break
            except Exception as e:
                pass
    
    browser.close()

print("\n" + "="*70 + "\n")
