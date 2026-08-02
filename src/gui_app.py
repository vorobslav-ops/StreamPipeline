import os
import shutil
import threading
import customtkinter as ctk
from tkinter import filedialog
from dotenv import load_dotenv

# Import your existing worker modules
import discord_worker
import twitter_worker
# import youtube_worker
# import tiktok_worker

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
X_COOKIES_PATH = os.path.join(CONFIG_DIR, "x_cookies.json")
CREDENTIALS_PATH = os.path.join(CONFIG_DIR, "credentials.env")

load_dotenv(CREDENTIALS_PATH)

# Set UI Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StreamPipelineApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StreamPipeline Command Center")
        self.geometry("750 x 550")
        self.resizable(False, False)

        # Selected video file path storage
        self.selected_video_path = ""

        # --- TAB NAVIGATION ---
        self.tabview = ctk.CTkTabview(self, width=710, height=480)
        self.tabview.pack(padx=20, pady=20)

        self.tab_text = self.tabview.add("Text Broadcast")
        self.tab_video = self.tabview.add("Video Clip Pipeline")

        self.setup_text_tab()
        self.setup_video_tab()

        # Status Footer
        self.status_label = ctk.CTkLabel(self, text="System Ready", font=("Arial", 12, "italic"))
        self.status_label.pack(side="bottom", pady=5)

    # --- TAB 1: TEXT BROADCAST UI ---
    def setup_text_tab(self):
        label = ctk.CTkLabel(self.tab_text, text="Instant Text Broadcast (Discord & X)", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        self.text_input = ctk.CTkTextbox(self.tab_text, width=650, height=250)
        self.text_input.pack(pady=10)
        self.text_input.insert("0.0", "Type your broadcast update or Kick live link here...")

        self.btn_send_text = ctk.CTkButton(self.tab_text, text="Dispatch Text Everywhere", command=self.trigger_text_broadcast)
        self.btn_send_text.pack(pady=15)

    # --- TAB 2: VIDEO PIPELINE UI ---
    def setup_video_tab(self):
        label = ctk.CTkLabel(self.tab_video, text="Short-Form Video Deployment (TikTok, YouTube, Discord, X)", font=("Arial", 16, "bold"))
        label.pack(pady=5)

        # File Selector
        self.btn_select_file = ctk.CTkButton(self.tab_video, text="Select .mp4 Clip File", fg_color="gray", command=self.select_file)
        self.btn_select_file.pack(pady=10)

        self.file_label = ctk.CTkLabel(self.tab_video, text="No video selected", font=("Arial", 11))
        self.file_label.pack(pady=2)

        # Title Input
        self.title_input = ctk.CTkEntry(self.tab_video, width=650, placeholder_text="Video Title (used for YouTube Shorts)...")
        self.title_input.pack(pady=8)

        # Description Input
        self.desc_input = ctk.CTkTextbox(self.tab_video, width=650, height=120)
        self.desc_input.pack(pady=8)
        self.desc_input.insert("0.0", "Video description and hashtags (#wowclassic #gothic)...")

        self.btn_send_video = ctk.CTkButton(self.tab_video, text="Deploy Video Pipeline", command=self.trigger_video_pipeline)
        self.btn_send_video.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 Video Files", "*.mp4")])
        if file_path:
            self.selected_video_path = file_path
            self.file_label.configure(text=os.path.basename(file_path))
            self.btn_select_file.configure(fg_color="green")

    def update_status(self, text):
        self.status_label.configure(text=text)

    # --- ASYNCHRONOUS WORKER THREADS ---
    def trigger_text_broadcast(self):
        message = self.text_input.get("0.0", "end").strip()
        if not message:
            self.update_status("Error: Message box is empty!")
            return

        self.update_status("Dispatching text broadcast...")
        self.btn_send_text.configure(state="disabled")

        # Run in thread so GUI doesn't freeze during Playwright automation
        threading.Thread(target=self._text_worker, args=(message,), daemon=True).start()

    def _text_worker(self, message):
        try:
            # Discord
            discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if discord_webhook:
                discord_worker.share_link(discord_webhook, message)

            # X (Twitter)
            twitter_worker.post_tweet_via_browser(message, X_COOKIES_PATH)

            self.update_status("Success: Text dispatched everywhere!")
            self.text_input.delete("0.0", "end")
        except Exception as e:
            self.update_status(f"Error: {e}")
        finally:
            self.btn_send_text.configure(state="normal")

    def trigger_video_pipeline(self):
        if not self.selected_video_path:
            self.update_status("Error: No .mp4 video selected!")
            return

        title = self.title_input.get().strip()
        desc = self.desc_input.get("0.0", "end").strip()

        self.update_status("Deploying video across platforms...")
        self.btn_send_video.configure(state="disabled")

        threading.Thread(target=self._video_worker, args=(self.selected_video_path, title, desc), daemon=True).start()

    def _video_worker(self, video_path, title, desc):
        try:
            full_payload = f"**{title}**\n\n{desc}\n\nWatch live: https://kick.com/yourchannel"

            # Discord
            discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if discord_webhook:
                discord_worker.share_link(discord_webhook, full_payload)

            # X
            twitter_worker.post_tweet_via_browser(f"{title}\n\nhttps://kick.com/yourchannel", X_COOKIES_PATH)

            # YouTube / TikTok Workers can be un-commented here when keys/cookies are activated
            # youtube_worker.upload_short(...)
            # tiktok_worker.upload_to_tiktok(...)

            self.update_status("Success: Video deployment complete!")
            self.title_input.delete(0, "end")
            self.desc_input.delete("0.0", "end")
            self.file_label.configure(text="No video selected")
            self.btn_select_file.configure(fg_color="gray")
            self.selected_video_path = ""
        except Exception as e:
            self.update_status(f"Error: {e}")
        finally:
            self.btn_send_video.configure(state="normal")

if __name__ == "__main__":
    app = StreamPipelineApp()
    app.mainloop()
