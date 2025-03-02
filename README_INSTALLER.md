# SKYNET Invoice Generator - Self-Installing Package

This package includes a launcher that will automatically install all required dependencies and run the SKYNET Invoice Generator application.

## Requirements

- Python 3.6 or higher must be installed on your system
- Internet connection (for the first run to download dependencies)

## Installation & Running

### Windows Users:

1. Extract the ZIP file to any location on your computer
2. Double-click on `Run_Invoice_Generator.bat`
3. The launcher will check for required dependencies and install them if needed
4. Once the setup is complete, the application will start automatically

### macOS Users:

1. Extract the ZIP file to any location on your computer
2. Open Terminal and navigate to the extracted folder
3. Make the launcher script executable by running: `chmod +x Run_Invoice_Generator.command`
4. Double-click on `Run_Invoice_Generator.command` or run it from Terminal
5. The launcher will check for required dependencies and install them if needed
6. Once the setup is complete, the application will start automatically

## Troubleshooting

- If you encounter any issues with the automatic installation, you can manually install the required packages:
  ```
  pip install -r requirements.txt
  ```
  
- If the application doesn't start after installation, try running it directly:
  ```
  python app.py
  ```

- Make sure the `invoice_template.html` file is in the same directory as the application

## What This Application Does

- Creates professional invoices with your company information
- Allows adding multiple line items with descriptions, quantities, and prices
- Automatically calculates subtotals, GST, and total amounts
- Saves invoices as PDF files to your desktop

## Support

If you encounter any issues, please contact your system administrator or IT department. 