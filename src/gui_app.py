import os
import shutil
import threading
import customtkinter as ctk
from tkinter import filedialog
from dotenv import load_dotenv

# Import workers
import discord_worker
import twitter_worker
import audio_worker
import obs_worker  # <-- NEW OBS WORKER

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
X_COOKIES_PATH = os.path.join(CONFIG_DIR, "x_cookies.json")
CREDENTIALS_PATH = os.path.join(CONFIG_DIR, "credentials.env")

load_dotenv(CREDENTIALS_PATH)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StreamPipelineApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StreamPipeline Command Center")
        self.geometry("750 x 550")
        self.resizable(False, False)

        self.selected_video_path = ""
        
        # Initialize the audio tester backend
        self.mic_tester = audio_worker.NoiseGateTester()

        # --- TAB NAVIGATION ---
        self.tabview = ctk.CTkTabview(self, width=710, height=480)
        self.tabview.pack(padx=20, pady=20)

        self.tab_text = self.tabview.add("Text Broadcast")
        self.tab_video = self.tabview.add("Video Clip Pipeline")
        self.tab_mic = self.tabview.add("Mic Calibration")
        self.tab_obs = self.tabview.add("OBS Remote") # <-- NEW TAB

        self.setup_text_tab()
        self.setup_video_tab()
        self.setup_mic_tab()
        self.setup_obs_tab()

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
        label = ctk.CTkLabel(self.tab_obs, text="OBS Studio Control", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        desc = ctk.CTkLabel(self.tab_obs, text="Execute actions instantly over local WebSocket.", font=("Arial", 12))
        desc.pack(pady=5)

        self.btn_save_replay = ctk.CTkButton(self.tab_obs, text="Save Replay Buffer", fg_color="purple", hover_color="darkmagenta", command=self.trigger_save_replay)
        self.btn_save_replay.pack(pady=20)

        self.btn_toggle_mute = ctk.CTkButton(self.tab_obs, text="Toggle Mic Mute", fg_color="darkorange", hover_color="orange", command=self.trigger_toggle_mute)
        self.btn_toggle_mute.pack(pady=10)

    def trigger_save_replay(self):
        self.update_status("Transmitting Replay Buffer command to OBS...")
        threading.Thread(target=self._obs_replay_worker, daemon=True).start()

    def _obs_replay_worker(self):
        try:
            worker = obs_worker.OBSWorker()
            worker.save_replay()
            self.update_status("Success: Replay Buffer saved!")
        except Exception as e:
            # If the user forgot to start the buffer in OBS, the WebSocket catches the error
            self.update_status(f"OBS Error: Could not save buffer. Is it running? ({e})")

    def trigger_toggle_mute(self):
        self.update_status("Toggling Mic hardware mute...")
        threading.Thread(target=self._obs_mute_worker, daemon=True).start()

    def _obs_mute_worker(self):
        try:
            worker = obs_worker.OBSWorker()
            # "Mic/Aux" is the default name in OBS; if you renamed it, update it here.
            worker.toggle_mic_mute("Mic/Aux") 
            self.update_status("Success: Mic mute toggled!")
        except Exception as e:
            self.update_status(f"OBS Error: Check Mic name or connection. ({e})")

if __name__ == "__main__":
    app = StreamPipelineApp()
    app.mainloop()
