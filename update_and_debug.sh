#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo " StreamPipeline Diagnostic & Repair Tool"
echo "=========================================="

echo "[1/4] Checking GitHub for core code updates..."
git pull origin main

echo "[2/4] Forcing dependency updates..."
source venv/bin/activate
pip install --upgrade -r requirements.txt
playwright install chromium --with-deps

echo "[3/4] Verifying security configurations..."
if [ ! -f "config/credentials.env" ]; then
    echo "[WARNING] config/credentials.env is missing!"
fi
if [ ! -f "config/x_cookies.json" ]; then
    echo "[WARNING] config/x_cookies.json is missing!"
fi

echo "[4/4] Launching GUI in Debug Mode. Saving output to crash_log.txt..."
python3 src/gui_app.py > crash_log.txt 2>&1

echo "[SYSTEM] Application closed. Check crash_log.txt for detailed error reports."
sleep 10