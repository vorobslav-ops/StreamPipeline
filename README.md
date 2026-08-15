# StreamPipeline Command Center

A free, simple, 1-click app for streamers to automatically distribute clips and updates to Discord, X (Twitter), TikTok, and YouTube, while also controlling your mic and OBS studio—all without paying monthly fees.[cite: 49]

## ⚡ What Can It Do? (Features)

* **API Paywall Bypass:** Posts directly to X (Twitter) using a hidden browser session, so you never pay per-tweet API fees.[cite: 49]
* **Instant Text & Video Broadcast:** Send your "Going Live" links or `.mp4` game clips to multiple platforms at the exact same time.[cite: 49]
* **Cross-Platform Metadata Sync:** Update your Kick stream title and game category directly from the Command Center, using automated browsers to bypass Cloudflare bot-protection.
* **1-Click Go-Live Automation:** Type your announcement once. The app triggers your X/Discord broadcasts, switches OBS to your "Starting Soon" scene, runs a 3-minute timer, unmutes your hardware mic, and switches to your "Live" scene automatically.
* **Hardware Noise Gate Calibrator:** A built-in audio tool that helps you find the exact threshold to block your PC fan noise from your mic.[cite: 49]
* **OBS Disaster Recovery:** Instantly backup and restore your entire OBS Studio configuration, scenes, and widgets to a local `.zip` file.
* **OBS Studio Remote:** Save your Replay Buffer or mute your mic over your local network using OBS WebSockets.[cite: 49]
* **1-Click Setup:** You don't need to know how to code. Just run the launcher, and it builds itself.[cite: 49]

## 🛠️ Step-by-Step Setup Guide (For Casual Users)

### Step 1: Download the App
1. Click the green **Code** button at the top of this GitHub page and select **Download ZIP**.[cite: 49]
2. Extract the ZIP folder anywhere on your PC (like your Desktop).[cite: 49]

### Step 2: Configure Your Accounts
Open the `config` folder. You will see template files ending in `.example`. Remove the `.example` extension from their names and fill them in:[cite: 49]

* **`credentials.env`**: Open this in Notepad (or any text editor). Paste your Discord Webhook URL. If you want to use the OBS Remote tab, enable the WebSocket Server in OBS Studio (it defaults to port 4455), type your generated password in here, and set your exact OBS Scene names for the Go-Live macro.[cite: 49]
* **`x_cookies.json` & `kick_cookies.json`**: This is how the app securely posts to platforms without paid APIs. Use a free browser extension like "Cookie-Editor" to export your active session cookies from Twitter and Kick, and paste them into their respective files.[cite: 49]

### Step 3: Launch the Command Center
You do not need to install complex Python packages manually. The app will download everything it needs automatically.[cite: 49]

* **On Windows:** Double-click `launch_windows.bat`.[cite: 49]
* **On Linux (Pop!_OS / Ubuntu / CachyOS):** Open your terminal inside the StreamPipeline folder and run `./launch_linux.sh`. *(Note: It will automatically ask for your OS password to install the required hardware audio drivers for the Mic Calibrator).*[cite: 49]

**Important:** The very first time you launch it, the black terminal window will stay open for a few minutes while it downloads the background browsers and audio tools. Let it finish. Every time after that, the GUI will launch instantly.[cite: 49]

## 🚑 Troubleshooting

If something breaks, or if a new StreamPipeline update is released, just run the `update_and_debug.sh` file. It will automatically check GitHub for code updates, force-repair your required files, and generate a crash log if anything goes wrong.[cite: 49]

## ☕ Support the Project

If this tool helped you bypass a paywall, save time, or grow your stream, consider dropping a tip.[cite: 49]

**Donate via PayPal:** [paypal.me/remkiraops](https://paypal.me/remkiraops)[cite: 49]