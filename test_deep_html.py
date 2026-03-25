"""
Deep dive into HTML structure - check for disabled/aria attributes
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
    
    print("\n" + "="*70)
    print("CHECKING ATTRIBUTES FOR AVAILABILITY")
    print("="*70)
    
    all_divs = page.query_selector_all("div")
    
    for target_day in [26, 27, 28]:
        for div in all_divs:
            try:
                text = div.inner_text().strip()
                if text == str(target_day):
                    # Get the outer HTML
                    outer_html = div.evaluate("e => e.outerHTML")
                    
                    # Get all attributes
                    attrs = div.evaluate("""e => {
                        const result = {};
                        for (let attr of e.attributes) {
                            result[attr.name] = attr.value;
                        }
                        return result;
                    }""")
                    
                    # Check parent
                    parent_html = div.evaluate("e => e.parentElement.outerHTML.substring(0, 300)")
                    
                    print(f"\nDay {target_day}:")
                    print(f"  Element HTML: {outer_html[:200]}")
                    print(f"  Attributes: {attrs}")
                    print(f"  Parent HTML: {parent_html}")
                    
                    # Check if disabled or aria-disabled
                    disabled = div.get_attribute("disabled")
                    aria_disabled = div.get_attribute("aria-disabled")
                    data_disabled = div.get_attribute("data-disabled")
                    
                    print(f"  disabled attr: {disabled}")
                    print(f"  aria-disabled: {aria_disabled}")
                    print(f"  data-disabled: {data_disabled}")
                    
                    break
            except Exception as e:
                print(f"Error: {e}")
                pass
    
    # Also check if maybe we need to look at buttons instead
    print("\n" + "="*70)
    print("CHECKING ALL BUTTONS")
    print("="*70)
    
    buttons = page.query_selector_all("button")
    for i, btn in enumerate(buttons[:10]):
        try:
            text = btn.inner_text()[:50]
            classes = btn.get_attribute("class") or ""
            disabled = btn.is_disabled()
            print(f"Button {i}: '{text}' | Disabled: {disabled}")
        except:
            pass
    
    # Check if dates are in a form or specific container
    print("\n" + "="*70)
    print("LOOKING FOR INTERACTIVE DATE CONTAINER")
    print("="*70)
    
    page_html = page.content()
    
    # Look for data-date or onclick handlers
    if "data-date" in page_html:
        print("✅ Found: data-date attributes")
    if "onClick" in page_html or "onclick" in page_html:
        print("✅ Found: onclick handlers")
    if "aria-label" in page_html:
        print("✅ Found: aria-label attributes")
    
    # Save full page for manual inspection
    with open("full_page.html", "w", encoding="utf-8") as f:
        f.write(page_html)
    print("\n📁 Full page saved to full_page.html")
    
    browser.close()

print("\n" + "="*70 + "\n")
