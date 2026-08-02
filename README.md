# StreamPipeline Command Center

A zero-cost, local Python GUI that automates the distribution of gaming clips and text updates to X (Twitter), Discord, TikTok, and YouTube Shorts. Built to bypass paid SaaS API tiers using direct headless browser automation.

## 🤖 The Origin Story

I used Google's Gemini AI to do the heavy lifting and write the code. 

Why does this exist? Pure pragmatism. I wanted a way to distribute my stream clips, but I absolutely refuse to pay monthly subscriptions for social media tools or X's API paywalls. This pipeline is just a custom workaround—designed with AI, built for free, and shared so you can use it too.

## ⚡ Features

* **Cross-Platform UI:** Built with CustomTkinter for a sleek dark-mode interface.
* **API Paywall Bypass:** Uses Playwright browser session injection to post directly to X without paying per-tweet fees.
* **1-Click Launchers:** Automated setup scripts that build the environment for both Windows and Linux OS.
* **Self-Healing:** Includes a built-in diagnostic bash script to force-update dependencies and pull the latest code.

## 🛠️ How to Install and Run

1. Download or clone this repository to your local machine.
2. Navigate to the `config/` directory. 
3. Remove the `.example` extensions from the two configuration files and input your specific Discord Webhook URL and exported X browser cookies.
4. **On Windows:** Double-click `launch_windows.bat`.
5. **On Linux (Pop!_OS / Ubuntu):** Open terminal, grant execution rights via `chmod +x launch_linux.sh`, and run `./launch_linux.sh`.

*(Note: On first launch, the scripts will automatically generate a localized Python virtual environment and download all required dependencies before opening the interface.)*

## ☕ Support the Project

If this tool helped you bypass a paywall, save time, or grow your stream, consider dropping a tip. 

**Donate via PayPal:** [paypal.me/remkiraops](https://paypal.me/remkiraops)