import requests

def share_link(webhook_url, content_text):
    payload = {"content": content_text}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("[SUCCESS] Dispatched notification to Discord.")
    else:
        print(f"[ERROR] Discord failed with status code: {response.status_code}")
