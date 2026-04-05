#!/bin/bash
# minimal-setup.sh - Quick OpenClaw setup on VPS
# Usage: curl -fsSL https://your-domain.com/minimal-setup.sh | bash

set -e

echo "🚀 OpenClaw VPS Setup - Minimal"
echo "================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on supported OS
if ! command -v apt-get &> /dev/null && ! command -v yum &> /dev/null; then
    echo -e "${RED}Error: This script supports Ubuntu/Debian or RHEL/CentOS${NC}"
    exit 1
fi

# Step 1: Install NVM
echo -e "${YELLOW}[1/6] Installing NVM...${NC}"
if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
echo -e "${GREEN}✓ NVM installed${NC}"

# Step 2: Install Node.js 22
echo -e "${YELLOW}[2/6] Installing Node.js 22...${NC}"
nvm install 22
nvm use 22
nvm alias default 22
echo -e "${GREEN}✓ Node.js $(node -v) installed${NC}"

# Step 3: Install pnpm
echo -e "${YELLOW}[3/6] Installing pnpm...${NC}"
if ! command -v pnpm &> /dev/null; then
    curl -fsSL https://get.pnpm.io/install.sh | sh -
fi
export PNPM_HOME="$HOME/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
echo -e "${GREEN}✓ pnpm $(pnpm -v) installed${NC}"

# Step 4: Install OpenClaw
echo -e "${YELLOW}[4/6] Installing OpenClaw...${NC}"
pnpm add -g openclaw
echo -e "${GREEN}✓ OpenClaw $(openclaw --version) installed${NC}"

# Step 5: Setup OpenClaw
echo -e "${YELLOW}[5/6] Configuring OpenClaw...${NC}"
openclaw setup
openclaw config set gateway.mode local
echo -e "${GREEN}✓ OpenClaw configured${NC}"

# Step 6: Install and start gateway service
echo -e "${YELLOW}[6/6] Installing gateway service...${NC}"

# Enable linger (critical: keeps services running after SSH logout)
echo -e "${YELLOW}  → Enabling linger for service persistence...${NC}"
sudo loginctl enable-linger $USER

openclaw gateway install
systemctl --user start openclaw-gateway
systemctl --user enable openclaw-gateway
sleep 2
echo -e "${GREEN}✓ Gateway service installed and started${NC}"

echo ""
echo "================================"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Add your API key: echo 'KIMI_API_KEY=your-key' >> ~/.openclaw/.env"
echo "2. Set default model: openclaw config set agents.defaults.model.primary 'kimi-coding/k2p5'"
echo "3. Check status: openclaw status"
echo ""
echo "To access dashboard:"
echo "  ssh -L 18789:localhost:18789 user@your-vps-ip"
echo "  # Then open http://localhost:18789/ in your browser"
