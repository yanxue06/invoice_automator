#!/bin/bash

echo "Creating updated Windows package with all dependencies..."

# Create directory if it doesn't exist
mkdir -p windows_package_fixed

# Copy necessary files
cp app.py windows_package_fixed/
cp invoice_template.html windows_package_fixed/

# Create .env.example file
cat > windows_package_fixed/.env.example << EOL
company_name="Your Company Name"
company_address="Your Company Address"
company_phone="Your Phone Number"
company_email="Your Email"
EOL

# Create requirements.txt with ALL dependencies
cat > windows_package_fixed/requirements.txt << EOL
jinja2
xhtml2pdf
reportlab
pillow
python-dotenv
EOL

# Create batch file
cat > windows_package_fixed/Run_SKYNET_Invoice_Generator.bat << EOL
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

REM Check if .env file exists, if not create from example
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit the .env file with your company information.
    notepad .env
)

echo Installing required packages...
python -m pip install -r requirements.txt

echo.
echo Starting SKYNET Invoice Generator...
echo.
python app.py
pause
EOL

# Create README.txt
cat > windows_package_fixed/README.txt << EOL
SKYNET Invoice Generator - Windows Installation Guide
====================================================

Prerequisites:
-------------
1. Python 3.8 or newer (https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

Installation and Usage:
---------------------
1. Extract all files from this ZIP package to a folder on your computer
2. Double-click the "Run_SKYNET_Invoice_Generator.bat" file
3. The first time you run it, the script will:
   - Install required dependencies
   - Create a .env file for your company information
   - Open the .env file for you to edit with your company details
4. The application will start automatically after setup

Troubleshooting:
--------------
- If you see "ModuleNotFoundError: No module named 'dotenv'":
  Run the batch file again, it will install the missing module

- If you see "No module named 'tkinter'":
  You need to reinstall Python and select the "tcl/tk and IDLE" option during installation

- If you have any other issues, please contact technical support

Note: The first run may take a few minutes to install all required packages.
EOL

# Create ZIP file
rm -f SKYNET_Invoice_Generator_Windows_Fixed.zip
zip -r SKYNET_Invoice_Generator_Windows_Fixed.zip windows_package_fixed

echo "Windows package created: SKYNET_Invoice_Generator_Windows_Fixed.zip"
echo "Send this updated package to your boss." 