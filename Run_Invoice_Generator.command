#!/bin/bash
# Make this script executable with: chmod +x Run_Invoice_Generator.command

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Starting SKYNET Invoice Generator..."
python3 run_invoice_generator.py

if [ $? -ne 0 ]; then
    echo "Error running the application."
    echo "Please make sure Python is installed on your system."
    echo "You can download Python from https://www.python.org/downloads/"
    read -p "Press Enter to exit..."
fi 