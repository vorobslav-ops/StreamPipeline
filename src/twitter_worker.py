import os
import json
import time
from playwright.sync_api import sync_playwright

def post_tweet_via_browser(text, cookies_path):
    if not os.path.exists(cookies_path):
        raise Exception("X cookies file missing at config/x_cookies.json.")

    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        try:
            with sync_playwright() as p:
                # DIAGNOSTIC MODE: headless=False makes the browser visible on your screen
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()

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
                page.goto("https://x.com/compose/tweet", wait_until="domcontentloaded", timeout=60000)

                page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=15000)
                page.fill('[data-testid="tweetTextarea_0"]', text)

                page.click('[data-testid="tweetButton"]', force=True)

                page.wait_for_timeout(4000)

                browser.close()
                return 

        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(5)
                
    # If all 3 attempts fail, send the error back to the GUI
    raise Exception(f"Max retries reached. Last error: {last_error}")
