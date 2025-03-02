@echo off
echo Starting SKYNET Invoice Generator...
python run_invoice_generator.py
if %ERRORLEVEL% NEQ 0 (
    echo Error running the application.
    echo Please make sure Python is installed on your system.
    echo You can download Python from https://www.python.org/downloads/
    pause
) 