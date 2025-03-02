#!/usr/bin/env python3
"""
Script to create a self-installing package for SKYNET Invoice Generator
"""

import os
import zipfile
import datetime

def create_package():
    """Create a ZIP package with all necessary files."""
    # Get the current date for the filename
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    # Define the output filename
    output_filename = f"SKYNET_Invoice_Generator_Self_Installing_{today}.zip"
    
    # List of files to include in the package
    files_to_include = [
        "app.py",
        "invoice_template.html",
        "requirements.txt",
        "run_invoice_generator.py",
        "Run_Invoice_Generator.bat",
        "Run_Invoice_Generator.command",
        "README_INSTALLER.md"
    ]
    
    # Create the ZIP file
    print(f"Creating package: {output_filename}")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add each file to the ZIP
        for file in files_to_include:
            if os.path.exists(file):
                print(f"Adding: {file}")
                zipf.write(file)
            else:
                print(f"Warning: {file} not found, skipping")
    
    print(f"\nPackage created successfully: {output_filename}")
    print(f"Size: {os.path.getsize(output_filename) / (1024*1024):.2f} MB")
    print("\nThis package includes:")
    print("- The SKYNET Invoice Generator application")
    print("- A launcher that will automatically install dependencies")
    print("- Batch and shell scripts for easy launching")
    print("- Documentation and instructions")

if __name__ == "__main__":
    create_package() 