#!/bin/bash
cd "$(dirname "$0")"

echo "[SYSTEM] Initializing StreamPipeline for Linux..."

if [ ! -d "venv" ]; then
    echo "[SETUP] First time setup detected. Building environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium --with-deps
else
    source venv/bin/activate
fi

echo "[SYSTEM] Launching Command Center..."
python3 src/gui_app.py