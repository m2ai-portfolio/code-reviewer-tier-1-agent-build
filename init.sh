#!/bin/bash
# Metroplex Academy - Code Reviewer Agent
# Development server startup script

set -e

echo "=== Code Reviewer Agent - Development Setup ==="

# Check Python version
python3 --version

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "=== Setup Complete ==="
echo "Virtual environment active. Run 'python -m pytest tests/' to run tests."
