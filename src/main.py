import os, shutil, time
from dotenv import load_dotenv
import discord_worker, twitter_worker, youtube_worker, tiktok_worker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "watch_folder", "input")
PROCESSING_DIR = os.path.join(BASE_DIR, "watch_folder", "processing")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

load_dotenv(os.path.join(CONFIG_DIR, "credentials.env"))

def parse_metadata(meta_path):
    with open(meta_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    title = lines[0].strip() if lines else "New Gameplay Clip"
    desc = "".join(lines[1:]).strip() if len(lines) > 1 else ""
    return title, desc

def run():
    # Ensure folders exist before scanning
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(PROCESSING_DIR, exist_ok=True)

    print("[SYSTEM] Scanning watch_folder/input...")
    files = os.listdir(INPUT_DIR)
    videos = [f for f in files if f.endswith('.mp4')]
    
    for video in videos:
        base_name = os.path.splitext(video)[0]
        meta_file = f"{base_name}.txt"
        
        if meta_file in files:
            src_vid, src_meta = os.path.join(INPUT_DIR, video), os.path.join(INPUT_DIR, meta_file)
            work_vid, work_meta = os.path.join(PROCESSING_DIR, video), os.path.join(PROCESSING_DIR, meta_file)
            
            shutil.move(src_vid, work_vid)
            shutil.move(src_meta, work_meta)
            
            title, description = parse_metadata(work_meta)
            
            # YouTube
            # youtube_worker.upload_short(os.path.join(CONFIG_DIR, "client_secrets.json"), work_vid, title, description)
            
            # TikTok
            # tiktok_worker.upload_to_tiktok(work_vid, description)

            # Discord
            discord_worker.share_link(os.getenv("DISCORD_WEBHOOK_URL"), f"**{title}**\n\n{description}\n\nLive at: https://kick.com/yourchannel")
            
            os.remove(work_vid)
            os.remove(work_meta)
            print(f"[PIPELINE] Task {base_name} cleared.")

if __name__ == "__main__":
    run()
