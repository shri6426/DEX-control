@echo off
setlocal enabledelayedexpansion

title DEX Control - Windows Deck Server

echo ===================================================
echo             DEX CONTROL - WINDOWS DECK
echo ===================================================
echo.

:: 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.10+ from python.org and add it to PATH.
    pause
    exit /b 1
)

:: 2. Create virtual environment if it doesn't exist
if not exist ".venv\Scripts\python.exe" (
    echo [*] Creating Python virtual environment in .venv...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [*] Virtual environment created successfully.
)

:: 3. Install or update dependencies
echo [*] Checking dependencies...
.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Pip encountered an issue installing packages. Retrying...
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)

:: 4. Launch DEX Control server
echo.
echo [*] Cleaning any stale process on port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [*] Starting DEX Control server...
echo     Local PC:    http://127.0.0.1:5000
echo     iPad Safari: Check terminal output below for your direct Wi-Fi URL!
echo     Press Ctrl+C at any time to stop the server.
echo.

.\.venv\Scripts\python.exe app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] DEX Control server exited with error code %ERRORLEVEL%.
    pause
)

endlocal
