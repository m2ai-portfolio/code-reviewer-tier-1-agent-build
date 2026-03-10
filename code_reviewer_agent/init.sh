#!/bin/bash
# Code Reviewer Agent - Setup Script

set -e

echo "=== Code Reviewer Agent - Setup ==="

# Check Python version
python3 --version

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies using python -m pip
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    venv/bin/python -m pip install -q --upgrade pip
    venv/bin/python -m pip install -q -r requirements.txt
fi

echo "=== Setup Complete ==="
echo "Run: venv/bin/python -m pytest tests/ -v"
