import os
import shutil
import threading
import time
import customtkinter as ctk
from tkinter import filedialog
from dotenv import load_dotenv

# Import workers
import discord_worker
import twitter_worker
import audio_worker
import obs_worker
import obs_backup_worker
import kick_worker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
X_COOKIES_PATH = os.path.join(CONFIG_DIR, "x_cookies.json")
CREDENTIALS_PATH = os.path.join(CONFIG_DIR, "credentials.env")
KICK_COOKIES_PATH = os.path.join(CONFIG_DIR, "kick_cookies.json")

load_dotenv(CREDENTIALS_PATH)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StreamPipelineApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StreamPipeline Command Center")
        self.geometry("750x700")
        self.resizable(False, False)

        self.selected_video_path = ""
        self.mic_tester = audio_worker.NoiseGateTester()

        # --- TAB NAVIGATION ---
        self.tabview = ctk.CTkTabview(self, width=710, height=630)
        self.tabview.pack(padx=20, pady=20)

        self.tab_text = self.tabview.add("Text Broadcast")
        self.tab_video = self.tabview.add("Video Clip Pipeline")
        self.tab_mic = self.tabview.add("Mic Calibration")
        self.tab_obs = self.tabview.add("OBS Remote")
        self.tab_sync = self.tabview.add("Metadata Sync")

        self.setup_text_tab()
        self.setup_video_tab()
        self.setup_mic_tab()
        self.setup_obs_tab()
        self.setup_sync_tab()

        self.status_label = ctk.CTkLabel(self, text="System Ready", font=("Arial", 12, "italic"))
        self.status_label.pack(side="bottom", pady=5)

    def update_status(self, text):
        self.status_label.configure(text=text)

    # --- TAB 1: TEXT BROADCAST UI ---
    def setup_text_tab(self):
        label = ctk.CTkLabel(self.tab_text, text="Instant Text Broadcast (Discord & X)", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        self.text_input = ctk.CTkTextbox(self.tab_text, width=650, height=250)
        self.text_input.pack(pady=10)
        self.text_input.insert("0.0", "Type your broadcast update or Kick live link here...")

        self.btn_send_text = ctk.CTkButton(self.tab_text, text="Dispatch Text Everywhere", command=self.trigger_text_broadcast)
        self.btn_send_text.pack(pady=15)

    def trigger_text_broadcast(self):
        message = self.text_input.get("0.0", "end").strip()
        if not message:
            self.update_status("Error: Message box is empty!")
            return

        self.update_status("Dispatching text broadcast...")
        self.btn_send_text.configure(state="disabled")
        threading.Thread(target=self._text_worker, args=(message,), daemon=True).start()

    def _text_worker(self, message):
        try:
            discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if discord_webhook:
                discord_worker.share_link(discord_webhook, message)
            twitter_worker.post_tweet_via_browser(message, X_COOKIES_PATH)
            self.update_status("Success: Text dispatched everywhere!")
            self.text_input.delete("0.0", "end")
        except Exception as e:
            self.update_status(f"Error: {e}")
        finally:
            self.btn_send_text.configure(state="normal")

    # --- TAB 2: VIDEO PIPELINE UI ---
    def setup_video_tab(self):
        label = ctk.CTkLabel(self.tab_video, text="Short-Form Video Deployment", font=("Arial", 16, "bold"))
        label.pack(pady=5)

        self.btn_select_file = ctk.CTkButton(self.tab_video, text="Select .mp4 Clip File", fg_color="gray", command=self.select_file)
        self.btn_select_file.pack(pady=10)

        self.file_label = ctk.CTkLabel(self.tab_video, text="No video selected", font=("Arial", 11))
        self.file_label.pack(pady=2)

        self.title_input = ctk.CTkEntry(self.tab_video, width=650, placeholder_text="Video Title...")
        self.title_input.pack(pady=8)

        self.desc_input = ctk.CTkTextbox(self.tab_video, width=650, height=120)
        self.desc_input.pack(pady=8)
        self.desc_input.insert("0.0", "Video description and hashtags (#wowclassic)...")

        self.btn_send_video = ctk.CTkButton(self.tab_video, text="Deploy Video Pipeline", command=self.trigger_video_pipeline)
        self.btn_send_video.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 Video Files", "*.mp4")])
        if file_path:
            self.selected_video_path = file_path
            self.file_label.configure(text=os.path.basename(file_path))
            self.btn_select_file.configure(fg_color="green")

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
            discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if discord_webhook:
                discord_worker.share_link(discord_webhook, full_payload)
            twitter_worker.post_tweet_via_browser(f"{title}\n\nhttps://kick.com/yourchannel", X_COOKIES_PATH)
            
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

    # --- TAB 3: MIC CALIBRATION UI ---
    def setup_mic_tab(self):
        label = ctk.CTkLabel(self.tab_mic, text="Hardware Noise Gate Calibration", font=("Arial", 16, "bold"))
        label.pack(pady=10)
        
        desc = ctk.CTkLabel(self.tab_mic, text="Find the perfect threshold where PC fans vanish but your voice passes through.\nUse this number in your streaming software.", font=("Arial", 12))
        desc.pack(pady=5)

        self.btn_toggle_mic = ctk.CTkButton(self.tab_mic, text="Start Mic Preview (Listen)", fg_color="darkred", hover_color="red", command=self.toggle_mic_preview)
        self.btn_toggle_mic.pack(pady=20)

        self.threshold_label = ctk.CTkLabel(self.tab_mic, text="Gate Threshold: 2.0%", font=("Arial", 14))
        self.threshold_label.pack(pady=5)

        self.slider = ctk.CTkSlider(self.tab_mic, from_=0, to=10, number_of_steps=100, command=self.on_slider_move)
        self.slider.set(2)
        self.slider.pack(pady=10)

    def on_slider_move(self, value):
        actual_threshold = value / 100.0
        self.threshold_label.configure(text=f"Gate Threshold: {value:.1f}%")
        if self.mic_tester.is_running:
            self.mic_tester.update_threshold(actual_threshold)

    def toggle_mic_preview(self):
        if not self.mic_tester.is_running:
            try:
                current_threshold = self.slider.get() / 100.0
                self.mic_tester.start(current_threshold)
                self.btn_toggle_mic.configure(text="Stop Mic Preview", fg_color="green", hover_color="darkgreen")
                self.update_status("Mic preview active. Speak into the microphone.")
            except Exception as e:
                self.update_status(f"Audio Error: {e}")
        else:
            self.mic_tester.stop()
            self.btn_toggle_mic.configure(text="Start Mic Preview (Listen)", fg_color="darkred", hover_color="red")
            self.update_status("Mic preview stopped.")

    # --- TAB 4: OBS REMOTE UI ---
    def setup_obs_tab(self):
        # Quick Actions
        label = ctk.CTkLabel(self.tab_obs, text="OBS Studio Control", font=("Arial", 16, "bold"))
        label.pack(pady=5)

        self.btn_save_replay = ctk.CTkButton(self.tab_obs, text="Save Replay Buffer", fg_color="purple", hover_color="darkmagenta", command=self.trigger_save_replay)
        self.btn_save_replay.pack(pady=5)

        self.btn_toggle_mute = ctk.CTkButton(self.tab_obs, text="Toggle Mic Mute", fg_color="darkorange", hover_color="orange", command=self.trigger_toggle_mute)
        self.btn_toggle_mute.pack(pady=5)
        
        # Disaster Recovery
        separator1 = ctk.CTkFrame(self.tab_obs, height=2, width=650, fg_color="gray30")
        separator1.pack(pady=10)

        dr_label = ctk.CTkLabel(self.tab_obs, text="Disaster Recovery", font=("Arial", 14, "bold"))
        dr_label.pack(pady=2)

        self.btn_backup = ctk.CTkButton(self.tab_obs, text="Backup OBS Settings", fg_color="teal", hover_color="darkcyan", command=self.trigger_backup)
        self.btn_backup.pack(pady=5)

        self.btn_restore = ctk.CTkButton(self.tab_obs, text="Restore Latest Backup", fg_color="darkred", hover_color="red", command=self.trigger_restore)
        self.btn_restore.pack(pady=5)

        # --- NEW: 1-CLICK GO-LIVE SEQUENCE ---
        separator2 = ctk.CTkFrame(self.tab_obs, height=2, width=650, fg_color="gray30")
        separator2.pack(pady=10)
        
        go_live_label = ctk.CTkLabel(self.tab_obs, text="Automated Go-Live Sequence", font=("Arial", 14, "bold"))
        go_live_label.pack(pady=2)
        
        self.golive_input = ctk.CTkEntry(self.tab_obs, width=650, placeholder_text="Enter your Going Live announcement for X & Discord here...")
        self.golive_input.pack(pady=5)
        
        self.countdown_label = ctk.CTkLabel(self.tab_obs, text="Timer: 00:00", font=("Arial", 18, "bold"), text_color="yellow")
        self.countdown_label.pack(pady=5)

        self.btn_golive = ctk.CTkButton(self.tab_obs, text="EXECUTE GO-LIVE (3-Minute Timer)", fg_color="green", hover_color="darkgreen", command=self.trigger_golive)
        self.btn_golive.pack(pady=5)
        
    # --- TAB 5: METADATA SYNC UI ---
    def setup_sync_tab(self):
        label = ctk.CTkLabel(self.tab_sync, text="Cross-Platform Metadata Sync", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        desc = ctk.CTkLabel(self.tab_sync, text="Update your stream title and game category across all platforms instantly.", font=("Arial", 12))
        desc.pack(pady=5)

        self.sync_title_input = ctk.CTkEntry(self.tab_sync, width=650, placeholder_text="New Stream Title...")
        self.sync_title_input.pack(pady=15)

        self.sync_category_input = ctk.CTkEntry(self.tab_sync, width=650, placeholder_text="Category (e.g., World of Warcraft)")
        self.sync_category_input.pack(pady=15)

        self.btn_sync_meta = ctk.CTkButton(self.tab_sync, text="Sync Metadata Across Platforms", fg_color="blue", hover_color="darkblue", command=self.trigger_sync_meta)
        self.btn_sync_meta.pack(pady=20)

    def trigger_sync_meta(self):
        title = self.sync_title_input.get().strip()
        category = self.sync_category_input.get().strip()
        
        if not title or not category:
            self.update_status("Error: You must provide both a title and a category!")
            return
            
        self.btn_sync_meta.configure(state="disabled")
        self.update_status("Syncing metadata across network...")
        threading.Thread(target=self._sync_worker, args=(title, category), daemon=True).start()

    def _sync_worker(self, title, category):
        try:
            # Sync to Kick
            self.update_status(f"Updating Kick: [{category}] {title}...")
            kick_worker.sync_kick_metadata(title, category, KICK_COOKIES_PATH)
            
            # (Future: Add YouTube sync here)
            
            self.update_status("Success: Stream metadata synchronized!")
            self.sync_title_input.delete(0, "end")
            self.sync_category_input.delete(0, "end")
        except Exception as e:
            self.update_status(f"Sync Error: {e}")
        finally:
            self.btn_sync_meta.configure(state="normal")


    # --- OBS ACTION TRIGGERS ---
    def trigger_save_replay(self):
        threading.Thread(target=self._obs_replay_worker, daemon=True).start()

    def _obs_replay_worker(self):
        try:
            worker = obs_worker.OBSWorker()
            worker.save_replay()
            self.update_status("Success: Replay Buffer saved!")
        except Exception as e:
            self.update_status(f"OBS Error: Could not save buffer. ({e})")

    def trigger_toggle_mute(self):
        threading.Thread(target=self._obs_mute_worker, daemon=True).start()

    def _obs_mute_worker(self):
        try:
            worker = obs_worker.OBSWorker()
            worker.toggle_mic_mute("Mic/Aux") 
            self.update_status("Success: Mic mute toggled!")
        except Exception as e:
            self.update_status(f"OBS Error: Check Mic name or connection. ({e})")
            
    # --- DISASTER RECOVERY TRIGGERS ---
    def trigger_backup(self):
        self.update_status("Generating local OBS backup...")
        threading.Thread(target=self._backup_worker, daemon=True).start()
        
    def _backup_worker(self):
        try:
            manager = obs_backup_worker.OBSBackupManager()
            filename = manager.backup()
            self.update_status(f"Success: OBS backed up to {filename}")
        except Exception as e:
            self.update_status(f"Backup Error: {e}")
            
    def trigger_restore(self):
        self.update_status("Restoring OBS configurations from latest backup...")
        threading.Thread(target=self._restore_worker, daemon=True).start()
        
    def _restore_worker(self):
        try:
            manager = obs_backup_worker.OBSBackupManager()
            filename = manager.restore()
            self.update_status(f"Success: Restored settings from {filename}. Restart OBS to see changes.")
        except Exception as e:
            self.update_status(f"Restore Error: {e}")

    # --- GO-LIVE SEQUENCE TRIGGER ---
    def trigger_golive(self):
        announcement = self.golive_input.get().strip()
        if not announcement:
            self.update_status("Error: You must type a Go-Live announcement first!")
            return
            
        self.btn_golive.configure(state="disabled")
        self.update_status("Initiating 1-Click Go-Live Sequence...")
        threading.Thread(target=self._golive_worker, args=(announcement,), daemon=True).start()

    def _golive_worker(self, announcement):
        try:
            worker = obs_worker.OBSWorker()
            starting_scene = os.getenv("OBS_STARTING_SCENE", "Starting Soon")
            live_scene = os.getenv("OBS_LIVE_SCENE", "Live")

            # 1. Start the actual stream in OBS
            self.update_status("Starting OBS Stream...")
            worker.start_stream()

            # 2. Switch to Starting Soon
            self.update_status(f"Switching to '{starting_scene}' scene...")
            worker.change_scene(starting_scene)

            # 3. Fire the Text Broadcasts
            self.update_status("Broadcasting to X and Discord...")
            discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if discord_webhook:
                discord_worker.share_link(discord_webhook, announcement)
            twitter_worker.post_tweet_via_browser(announcement, X_COOKIES_PATH)

            # 4. GUI Countdown Timer (3 Minutes = 180 seconds)
            for remaining in range(180, 0, -1):
                mins, secs = divmod(remaining, 60)
                self.countdown_label.configure(text=f"Timer: {mins:02d}:{secs:02d}")
                time.sleep(1)

            # 5. Timer hits zero: Unmute mic and switch to Live
            self.update_status(f"Timer complete! Switching to '{live_scene}'...")
            worker.unmute_mic("Mic/Aux")
            worker.change_scene(live_scene)
            
            self.countdown_label.configure(text="LIVE!")
            self.update_status("Sequence complete. You are live.")

        except Exception as e:
            self.update_status(f"Sequence Error: {e}")
        finally:
            self.btn_golive.configure(state="normal")
            self.golive_input.delete(0, "end")

if __name__ == "__main__":
    app = StreamPipelineApp()
    app.mainloop()
