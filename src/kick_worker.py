import os
import json
import time
from playwright.sync_api import sync_playwright

def sync_kick_metadata(title, category, cookies_path):
    if not os.path.exists(cookies_path):
        raise Exception("Kick cookies file missing at config/kick_cookies.json.")

    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        try:
            with sync_playwright() as p:
                # headless=False is MANDATORY to bypass Kick's Cloudflare protection
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()

                # Inject cookies to bypass login
                with open(cookies_path, 'r') as f:
                    cookies = json.load(f)
                    for cookie in cookies:
                        if 'sameSite' in cookie:
                            val = cookie['sameSite']
                            if val is None or val in ['no_restriction', 'unspecified', '']:
                                cookie['sameSite'] = 'None'
                            else:
                                cookie['sameSite'] = str(val).capitalize()
                        if 'partitionKey' in cookie:
                            del cookie['partitionKey']

                context.add_cookies(cookies)
                page = context.new_page()

                # Navigate directly to the Creator Dashboard Stream settings
                page.goto("https://kick.com/dashboard/stream", wait_until="domcontentloaded", timeout=60000)

                # Wait for the Title input box to load, clear it, and type the new Title
                page.wait_for_selector('input[name="title"]', timeout=15000)
                page.fill('input[name="title"]', title)

                # Wait for the Category dropdown, clear it, and type the new Category (e.g., World of Warcraft)
                page.wait_for_selector('input[placeholder="Search category..."]', timeout=5000)
                page.fill('input[placeholder="Search category..."]', category)
                
                # Press Enter to select the top category result
                page.keyboard.press("Enter")

                # Click the Save button (using generic text matching for the save button)
                page.click('button:has-text("Save")')

                # Wait a few seconds to ensure the server registers the save before closing
                page.wait_for_timeout(4000)

                browser.close()
                return 

        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(5)
                
    raise Exception(f"Max retries reached on Kick update. Last error: {last_error}")
