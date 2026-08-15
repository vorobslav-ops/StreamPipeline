#!/bin/bash
cd "$(dirname "$0")"

echo "========================================"
echo "  StreamPipeline Linux Initialization   "
echo "========================================"

# 1. Install system-level audio dependencies dynamically
echo "[SYSTEM] Checking for required audio hardware drivers (PortAudio)..."
if command -v apt >/dev/null; then
    echo "[SYSTEM] Detected Debian/Ubuntu/Pop!_OS system. Installing libportaudio2..."
    sudo apt update && sudo apt install -y libportaudio2
elif command -v pacman >/dev/null; then
    echo "[SYSTEM] Detected Arch/CachyOS system. Installing portaudio..."
    sudo pacman -Sy --needed --noconfirm portaudio
elif command -v dnf >/dev/null; then
    echo "[SYSTEM] Detected Fedora/RHEL system. Installing portaudio..."
    sudo dnf install -y portaudio
else
    echo "[WARNING] Unrecognized package manager. You may need to install 'portaudio' manually."
fi

# 2. Setup Python Virtual Environment
echo "[SYSTEM] Verifying Python Virtual Environment..."
if [ ! -d "venv" ]; then
    echo "[SETUP] First time setup detected. Building environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Install Python dependencies
echo "[SYSTEM] Installing/Updating Python libraries..."
pip install -r requirements.txt

# 4. Install Playwright browsers (for API bypass)
echo "[SYSTEM] Verifying Headless Browsers..."
playwright install chromium --with-deps

# 5. Launch the Command Center
echo "[SYSTEM] Launching Command Center..."
python3 src/gui_app.py