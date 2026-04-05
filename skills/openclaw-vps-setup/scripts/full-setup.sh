#!/bin/bash
# full-setup.sh - Complete OpenClaw setup with Kimi + Telegram
# Usage: KIMI_API_KEY=xxx TELEGRAM_TOKEN=xxx TELEGRAM_USER_ID=xxx ./full-setup.sh

set -e

echo "🚀 OpenClaw VPS Setup - Full"
echo "=============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration from environment
KIMI_API_KEY="${KIMI_API_KEY:-}"
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-}"
TELEGRAM_USER_ID="${TELEGRAM_USER_ID:-}"

# Prompt for missing values
if [ -z "$KIMI_API_KEY" ]; then
    echo -e "${YELLOW}Enter your Kimi API Key:${NC}"
    read -s KIMI_API_KEY
    echo ""
fi

if [ -z "$KIMI_API_KEY" ]; then
    echo -e "${RED}Error: KIMI_API_KEY is required${NC}"
    exit 1
fi

echo -e "${BLUE}Configuration:${NC}"
echo "  Kimi API Key: ${KIMI_API_KEY:0:10}..."
if [ -n "$TELEGRAM_TOKEN" ]; then
    echo "  Telegram Token: ${TELEGRAM_TOKEN:0:10}..."
    echo "  Telegram User ID: ${TELEGRAM_USER_ID:-'(will allow all)'}"
fi

# Step 1: Install NVM
echo ""
echo -e "${YELLOW}[1/8] Installing NVM...${NC}"
if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
echo -e "${GREEN}✓ NVM ready${NC}"

# Step 2: Install Node.js 22
echo -e "${YELLOW}[2/8] Installing Node.js 22...${NC}"
nvm install 22
nvm use 22
nvm alias default 22
echo -e "${GREEN}✓ Node.js $(node -v)${NC}"

# Step 3: Install pnpm
echo -e "${YELLOW}[3/8] Installing pnpm...${NC}"
if ! command -v pnpm &> /dev/null; then
    curl -fsSL https://get.pnpm.io/install.sh | sh -
fi
export PNPM_HOME="$HOME/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
echo -e "${GREEN}✓ pnpm $(pnpm -v)${NC}"

# Step 4: Install OpenClaw
echo -e "${YELLOW}[4/8] Installing OpenClaw CLI...${NC}"
pnpm add -g openclaw
echo -e "${GREEN}✓ OpenClaw $(openclaw --version)${NC}"

# Step 5: Initial Setup
echo -e "${YELLOW}[5/8] Running OpenClaw setup...${NC}"
openclaw setup
openclaw config set gateway.mode local
openclaw config set agents.defaults.model.primary "kimi-coding/k2p5"
echo -e "${GREEN}✓ OpenClaw configured${NC}"

# Step 6: Configure Credentials
echo -e "${YELLOW}[6/8] Setting up credentials...${NC}"

# Create .env file
cat > ~/.openclaw/.env << EOF
KIMI_API_KEY=$KIMI_API_KEY
EOF

if [ -n "$TELEGRAM_TOKEN" ]; then
    echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN" >> ~/.openclaw/.env
fi

chmod 600 ~/.openclaw/.env

# Create auth profile
cat > ~/.openclaw/auth-profiles.json << EOF
{
  "default": {
    "provider": "kimi-coding",
    "apiKey": "$KIMI_API_KEY"
  }
}
EOF
chmod 600 ~/.openclaw/auth-profiles.json

# Secure credentials directory
chmod 700 ~/.openclaw
mkdir -p ~/.openclaw/credentials
chmod 700 ~/.openclaw/credentials

echo -e "${GREEN}✓ Credentials configured${NC}"

# Step 7: Telegram Configuration (if token provided)
if [ -n "$TELEGRAM_TOKEN" ]; then
    echo -e "${YELLOW}[7/8] Configuring Telegram...${NC}"
    
    openclaw config set channels.telegram.enabled true
    openclaw config set channels.telegram.botToken "$TELEGRAM_TOKEN"
    openclaw config set channels.telegram.dmPolicy "allowlist"
    openclaw config set channels.telegram.groupPolicy "allowlist"
    
    if [ -n "$TELEGRAM_USER_ID" ]; then
        # Note: OpenClaw CLI might need direct JSON edit for arrays
        echo -e "${YELLOW}Note: Set allowFrom to [$TELEGRAM_USER_ID] in ~/.openclaw/openclaw.json${NC}"
    fi
    
    # Test bot
    BOT_INFO=$(curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getMe")
    if echo "$BOT_INFO" | grep -q '"ok":true'; then
        BOT_NAME=$(echo "$BOT_INFO" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✓ Telegram bot @$BOT_NAME connected${NC}"
    else
        echo -e "${RED}⚠ Telegram token invalid${NC}"
    fi
else
    echo -e "${YELLOW}[7/8] Skipping Telegram (no token provided)${NC}"
fi

# Step 8: Install and Start Service
echo -e "${YELLOW}[8/8] Installing gateway service...${NC}"

# Enable linger (critical: keeps services running after SSH logout/disconnect)
echo -e "${YELLOW}  → Enabling linger for service persistence...${NC}"
sudo loginctl enable-linger $USER

openclaw gateway install
systemctl --user daemon-reload
systemctl --user start openclaw-gateway
systemctl --user enable openclaw-gateway
sleep 3

# Verify
if systemctl --user is-active --quiet openclaw-gateway; then
    echo -e "${GREEN}✓ Gateway service running${NC}"
else
    echo -e "${RED}✗ Gateway failed to start${NC}"
    echo "Check logs: journalctl --user -u openclaw-gateway -n 20"
    exit 1
fi

echo ""
echo "=============================="
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo "  Check status:  openclaw status"
echo "  Health check:  openclaw health"
echo "  View logs:     journalctl --user -u openclaw-gateway -f"
echo ""
echo -e "${BLUE}Dashboard Access:${NC}"
echo "  1. Create tunnel: ssh -L 18789:localhost:18789 user@your-vps-ip"
echo "  2. Get URL:       openclaw dashboard --no-open"
echo "  3. Open browser:  http://localhost:18789/#token=YOUR_TOKEN"
echo ""
echo -e "${BLUE}Telegram:${NC}"
if [ -n "$TELEGRAM_TOKEN" ]; then
    echo "  Message your bot to start chatting!"
    echo "  Get your user ID: curl -s \"https://api.telegram.org/bot${TELEGRAM_TOKEN:0:10}.../getUpdates\""
else
    echo "  To add Telegram later, see: openclaw config --help"
fi
