import os
from tiktok_uploader.upload import TikTokUploader


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_PATH = os.path.join(BASE_DIR, "..", "config", "cookies.txt")

def upload_to_tiktok(video_path, description):
    try:
        uploader = TikTokUploader(cookies=COOKIE_PATH)
        failed = uploader.upload_videos(
            videos=[{'video': video_path, 'description': description}]
        )
        if not failed:
            print("[SUCCESS] Pushed to TikTok")
        else:
            print("[-] TikTok upload failed.")
    except Exception as e:
        print(f"[-] TikTok automation error: {e}")
