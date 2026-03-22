#!/bin/bash
# Install script for Marketing Creator skill
# This script installs all required dependencies

set -e

echo "==================================="
echo "Marketing Creator - Installation"
echo "==================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo ""
    echo "⚠️  Warning: Not in a virtual environment."
    echo "   It's recommended to use a virtual environment:"
    echo "   python3 -m venv venv && source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install requirements
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Set up your API key in config.json"
echo "2. Run: python3 test_setup.py"
echo "3. Start generating: ./marketing.py --help"
echo ""
