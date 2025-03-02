#!/bin/bash

# Create windows package directory
mkdir -p windows_package

# Copy necessary files
cp app.py windows_package/
cp invoice_template.html windows_package/

# Create requirements.txt
cat > windows_package/requirements.txt << EOF
jinja2
xhtml2pdf
reportlab
pillow
EOF

# Create batch file to run the application
cat > windows_package/Run_SKYNET_Invoice_Generator.bat << EOF
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
EOF

# Create README.txt with instructions
cat > windows_package/README.txt << EOF
SKYNET Invoice Generator
========================

This application allows you to create professional invoices with your company branding.

Installation and Usage Instructions:
-----------------------------------

1. Make sure you have Python installed on your Windows computer
   - Download from https://www.python.org/downloads/windows/
   - During installation, check the box "Add Python to PATH"

2. Double-click the "Run_SKYNET_Invoice_Generator.bat" file
   - This will automatically install required packages and start the application
   - The first time you run it, Windows may show security warnings - click "More info" and "Run anyway"

3. Using the application:
   - Fill in the client information in the "BILL TO" section
   - Add items to the invoice using the "Add Item" button
   - Enter an invoice number
   - Click "Save Invoice" to generate a PDF on your desktop

Troubleshooting:
---------------
- If you see errors about missing modules, try running the batch file again
- If you have issues with tkinter, make sure you installed Python with the "tcl/tk and IDLE" option
- For any other issues, please contact technical support

EOF

# Create the ZIP file
rm -f SKYNET_Invoice_Generator_Windows.zip
zip -r SKYNET_Invoice_Generator_Windows.zip windows_package

echo "Windows package created: SKYNET_Invoice_Generator_Windows.zip" 