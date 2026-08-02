@echo off
cd /d "%~dp0"

echo [SYSTEM] Initializing StreamPipeline for Windows...

IF NOT EXIST "venv\" (
    echo [SETUP] First time setup detected. Building environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    playwright install chromium
) ELSE (
    call venv\Scripts\activate.bat
)

echo [SYSTEM] Launching Command Center...
python src\gui_app.py
pause