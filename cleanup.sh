#!/bin/bash

# Cleanup script for SKYNET Invoice Generator project
echo "Cleaning up project directory..."

# Create a build directory if it doesn't exist
mkdir -p build

# Move build artifacts to build directory
mv -f *.spec build/ 2>/dev/null
mv -f build/ dist/ __pycache__/ build/ 2>/dev/null

# Create a backup directory if it doesn't exist
mkdir -p backup

# Move ZIP files to backup directory
mv -f *.zip backup/ 2>/dev/null

# Remove any PyInstaller temporary files
rm -rf __pycache__/ 2>/dev/null
rm -f *.pyc 2>/dev/null

# List the final project structure
echo "Final project structure:"
ls -la

echo "Cleanup complete!" 