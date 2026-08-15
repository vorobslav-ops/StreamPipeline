@echo off
cd /d "%~dp0"

echo ========================================
echo  StreamPipeline Windows Initialization   
echo ========================================

echo [SYSTEM] Verifying Python Virtual Environment...
IF NOT EXIST "venv\" (
    echo [SETUP] First time setup detected. Building environment...
    python -m venv venv
)

echo [SYSTEM] Activating environment...
call venv\Scripts\activate.bat

echo [SYSTEM] Installing/Updating Python libraries...
pip install -r requirements.txt

echo [SYSTEM] Verifying Headless Browsers...
playwright install chromium

echo [SYSTEM] Launching Command Center...
python src\gui_app.py
pause