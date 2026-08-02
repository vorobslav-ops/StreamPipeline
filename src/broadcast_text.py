import os
import requests
from dotenv import load_dotenv

# Import the new custom browser-automation worker
import twitter_worker 

# Set paths based on your Pop!_OS directory structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DIR = os.path.join(BASE_DIR, "watch_folder", "text_only")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "credentials.env")
X_COOKIES_PATH = os.path.join(BASE_DIR, "config", "x_cookies.json")

# Load your existing Webhook keys
load_dotenv(CONFIG_PATH)

def push_discord(message):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("[ERROR] Discord Webhook URL not found in credentials.env")
        return
        
    response = requests.post(webhook, json={"content": message})
    if response.status_code == 204:
        print("[SUCCESS] Dispatched to Discord.")
    else:
        print(f"[ERROR] Discord failed: {response.status_code}")

def push_x(message):
    # Route the payload through our headless browser bypass instead of the paid API
    twitter_worker.post_tweet_via_browser(message, X_COOKIES_PATH)

def run_broadcast():
    print("[SYSTEM] Scanning for text broadcasts...")
    
    # Safety check in case the directory was accidentally deleted
    if not os.path.exists(TEXT_DIR):
        print(f"[ERROR] Text directory missing at {TEXT_DIR}")
        return
        
    files = os.listdir(TEXT_DIR)
    txt_files = [f for f in files if f.endswith('.txt')]
    
    if not txt_files:
        print("[INFO] No text files found to broadcast.")
        return

    for txt_file in txt_files:
        file_path = os.path.join(TEXT_DIR, txt_file)
        
        # Read the message payload
        with open(file_path, 'r', encoding='utf-8') as f:
            message = f.read().strip()
            
        if message:
            print(f"\n[BROADCASTING] Payload: '{message}'")
            push_discord(message)
            push_x(message)
        
        # System purification: clean up the file so it doesn't broadcast twice
        os.remove(file_path)
        print(f"[PIPELINE] Cleared {txt_file}.")

if __name__ == "__main__":
    run_broadcast()
