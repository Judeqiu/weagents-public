#!/bin/bash
# Agent Browser Installation Script for WeAgents
# This script installs agent-browser globally and downloads Chromium

set -e

echo "=== Installing Agent Browser for WeAgents ==="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/ or use nvm"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi

echo "✓ npm found: $(npm --version)"

# Install agent-browser globally
echo ""
echo "→ Installing agent-browser globally..."
npm install -g agent-browser

# Install Chromium
echo ""
echo "→ Downloading Chromium browser..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - install with dependencies
    agent-browser install --with-deps
else
    # macOS or other
    agent-browser install
fi

# Verify installation
echo ""
echo "→ Verifying installation..."
if command -v agent-browser &> /dev/null; then
    echo "✓ agent-browser installed successfully!"
    agent-browser --version 2>/dev/null || echo "  (version check skipped)"
else
    echo "⚠️ agent-browser command not found in PATH"
    echo "   You may need to add npm global bin to your PATH:"
    echo "   export PATH=\"\$(npm config get prefix)/bin:\$PATH\""
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Quick start:"
echo "  agent-browser open https://example.com"
echo "  agent-browser snapshot -i"
echo "  agent-browser close"
echo ""
echo "For more commands: agent-browser --help"
