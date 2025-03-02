@echo off
echo SKYNET Invoice Generator - Setup and Launch
echo ==========================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or newer from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check if pip is available
python -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not available. Please ensure Python is installed correctly.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install -r requirements.txt

echo.
echo Starting SKYNET Invoice Generator...
echo.
python app.py
pause
