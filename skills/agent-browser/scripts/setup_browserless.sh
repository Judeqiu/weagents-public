#!/bin/bash
# Setup Browserless API token for agent-browser skill
# This script configures the BROWSERLESS_TOKEN environment variable

set -e

# The Browserless API token
DEFAULT_TOKEN="2U3jFeWFupLKhCm4dbca95a8ad82b31439c5729ffafec1f0e"

echo "==================================="
echo "Browserless API Setup"
echo "==================================="
echo ""

# Check if token is already set
if [ -n "$BROWSERLESS_TOKEN" ]; then
    echo "BROWSERLESS_TOKEN is already set."
    echo "Current token: ${BROWSERLESS_TOKEN:0:10}..."
    echo ""
    read -p "Do you want to update it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Current token preserved."
        exit 0
    fi
fi

# Set the token
export BROWSERLESS_TOKEN="$DEFAULT_TOKEN"

echo "Setting up Browserless API token..."
echo ""

# Add to shell profile
SHELL_PROFILE=""
if [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.profile" ]; then
    SHELL_PROFILE="$HOME/.profile"
fi

if [ -n "$SHELL_PROFILE" ]; then
    # Remove old token if exists
    if grep -q "BROWSERLESS_TOKEN" "$SHELL_PROFILE" 2>/dev/null; then
        sed -i '/BROWSERLESS_TOKEN/d' "$SHELL_PROFILE"
    fi
    
    # Add new token
    echo "" >> "$SHELL_PROFILE"
    echo "# Browserless API configuration (added by agent-browser skill)" >> "$SHELL_PROFILE"
    echo "export BROWSERLESS_TOKEN=\"$DEFAULT_TOKEN\"" >> "$SHELL_PROFILE"
    echo "export BROWSERLESS_REGION=\"sfo\"  # Options: sfo, lon, ams" >> "$SHELL_PROFILE"
    
    echo "✓ Token added to: $SHELL_PROFILE"
fi

# Also add to OpenClaw environment if available
if [ -d "$HOME/.openclaw" ]; then
    # Create a local env file for OpenClaw
    cat > "$HOME/.openclaw/.browserless_env" << ENVEOF
# Browserless API configuration
export BROWSERLESS_TOKEN="$DEFAULT_TOKEN"
export BROWSERLESS_REGION="sfo"
ENVEOF
    echo "✓ Token saved to: ~/.openclaw/.browserless_env"
    
    # Add to AGENTS.md if it exists
    if [ -f "$HOME/.openclaw/workspace/AGENTS.md" ]; then
        if ! grep -q "BROWSERLESS_TOKEN" "$HOME/.openclaw/workspace/AGENTS.md" 2>/dev/null; then
            echo "" >> "$HOME/.openclaw/workspace/AGENTS.md"
            echo "## Browserless API Configuration" >> "$HOME/.openclaw/workspace/AGENTS.md"
            echo "Token is configured in ~/.openclaw/.browserless_env" >> "$HOME/.openclaw/workspace/AGENTS.md"
            echo "Source it with: source ~/.openclaw/.browserless_env" >> "$HOME/.openclaw/workspace/AGENTS.md"
            echo "✓ Reference added to AGENTS.md"
        fi
    fi
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Token configured: ${DEFAULT_TOKEN:0:15}..."
echo ""
echo "To use Browserless:"
echo "  1. Restart your shell or run: source $SHELL_PROFILE"
echo "  2. Test with: browserless_helper.sh status"
echo "  3. Take screenshot: browserless_helper.sh screenshot --url https://example.com"
echo ""
echo "Available regions:"
echo "  - sfo: US West (San Francisco) - default"
echo "  - lon: Europe UK (London)"
echo "  - ams: Europe (Amsterdam)"
echo ""
echo "Change region: export BROWSERLESS_REGION=lon"
