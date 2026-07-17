@echo off
TITLE Cyber Sentry Launcher

echo ===================================================
echo Initializing Cyber Sentry Environment...
echo ===================================================

:: 1. Launch the Backend API Server in a separate window
echo Starting the Backend Server...
start "Cyber Sentry Backend" cmd /k ".\venv\Scripts\activate.bat && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

:: Give the server a couple of seconds to spin up before launching the UI
timeout /t 2 /nobreak >nul

:: 2. Launch the Standalone Desktop Application
echo Starting the Desktop App...
start "Cyber Sentry GUI" cmd /c ".\venv\Scripts\activate.bat && python app.py"

exit