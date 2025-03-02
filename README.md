# SKYNET Invoice Generator

A professional invoice generation application built with Python and Tkinter. This application allows users to create, customize, and save invoices as PDF files.

## Features

- User-friendly GUI for entering invoice details
- Add multiple items with descriptions, quantities, and prices
- Automatic calculation of subtotals, taxes, and totals
- Professional PDF output with company branding
- Cross-platform compatibility (macOS and Windows)

## Screenshots

(Add screenshots here)

## Installation

### Prerequisites

- Python 3.8 or higher
- Required Python packages (installed automatically):
  - tkinter
  - jinja2
  - xhtml2pdf
  - reportlab
  - pillow

### Environment Setup

1. Copy the `.env.example` file to a new file named `.env`
2. Edit the `.env` file with your company information:
   ```
   company_name="Your Company Name"
   company_address="Your Company Address"
   company_phone="Your Phone Number"
   company_email="Your Email"
   ```

### For Developers

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/skynet-invoice-generator.git
   cd skynet-invoice-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

### For End Users

#### macOS
- Download the latest macOS release
- Extract the ZIP file
- Move the application to your Applications folder
- Double-click to run

#### Windows
- Download the latest Windows release
- Extract the ZIP file
- Follow the instructions in README.txt

## Building from Source

### macOS

```bash
# Install PyInstaller
pip install pyinstaller

# Build the application
pyinstaller app_final.spec
```

### Windows

```bash
# Install PyInstaller
pip install pyinstaller

# Build the application
pyinstaller --onefile --windowed --add-data "invoice_template.html;." --name "SKYNET Invoice Generator" app.py
```

## Project Structure

- `app.py`: Main application code
- `invoice_template.html`: HTML template for PDF generation
- `app_final.spec`: PyInstaller specification for building the executable
- `prepare_windows_package.sh`: Script to create Windows distribution package

## License

(Add your license information here)

## Acknowledgments

- ReportLab and xhtml2pdf for PDF generation
- Jinja2 for HTML templating 