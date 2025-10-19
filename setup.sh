#!/bin/bash

# Setup script for ILP Assignment 4
# Creates virtual environment and installs essential dependencies

echo "Setting up ILP Assignment 4 environment..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Please run this script from the Assignment-4 directory."
    exit 1
fi

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing essential dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "   source venv/bin/activate"
echo ""
echo "To generate figures, run:"
echo "   python create_figures.py"
echo ""
echo "To deactivate when done, run:"
echo "   deactivate"
echo ""