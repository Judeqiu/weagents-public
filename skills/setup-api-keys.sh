#!/bin/bash
# Setup API Keys for Financial Skills MCP Integration
# Usage: ./setup-api-keys.sh

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     Financial Skills - API Key Setup                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ENV_FILE="/Users/zhengqingqiu/projects/weagents/.env"

echo "This script will help you set up API keys for financial data."
echo ""

# Check if .env exists
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠ .env file already exists at $ENV_FILE${NC}"
    read -p "Do you want to update it? (y/n): " update_env
    if [ "$update_env" != "y" ]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "Step 1/5: Massive/Polygon API Key (REQUIRED)"
echo "────────────────────────────────────────"
echo "This is the most important key. It provides stock prices and market data."
echo "Get your free key at: https://polygon.io/ (now Massive)"
echo ""
read -p "Enter your Polygon API key (starts with pk_): " polygon_key

if [ -z "$polygon_key" ]; then
    echo -e "${RED}✗ No key provided. You must set POLYGON_API_KEY to use market data.${NC}"
    echo "You can add it later by editing $ENV_FILE"
fi

echo ""
echo "Step 2/5: SEC API Key (Recommended)"
echo "────────────────────────────────────"
echo "Provides structured SEC filings. Free alternative available."
echo "Get key at: https://sec-api.io/ (or press Enter to skip)"
echo ""
read -p "Enter your SEC API key (optional): " sec_key

echo ""
echo "Step 3/5: FRED API Key (Optional)"
echo "──────────────────────────────────"
echo "Provides economic data (GDP, inflation, interest rates)."
echo "Get free key at: https://fred.stlouisfed.org/ (or press Enter to skip)"
echo ""
read -p "Enter your FRED API key (optional): " fred_key

echo ""
echo "Step 4/5: NewsAPI Key (Optional)"
echo "─────────────────────────────────"
echo "Provides financial news."
echo "Get free key at: https://newsapi.org/ (or press Enter to skip)"
echo ""
read -p "Enter your NewsAPI key (optional): " news_key

echo ""
echo "Step 5/5: Alpaca API (Optional)"
echo "────────────────────────────────"
echo "Alternative market data source."
echo "Get free keys at: https://alpaca.markets/ (or press Enter to skip)"
echo ""
read -p "Enter your Alpaca API Key ID (optional): " alpaca_key
if [ -n "$alpaca_key" ]; then
    read -p "Enter your Alpaca Secret Key: " alpaca_secret
fi

# Create .env file
echo ""
echo "Creating configuration file..."
echo ""

cat > "$ENV_FILE" << EOF
# Financial Skills MCP - API Configuration
# Generated: $(date)
# =========================================

# REQUIRED: Market Data (Polygon.io)
# Get free key: https://polygon.io/ (now Massive)
POLYGON_API_KEY=${polygon_key}

# RECOMMENDED: SEC Filings (sec-api.io)
# Alternative: Use official EDGAR (no key needed)
SEC_API_KEY=${sec_key}
SEC_USER_AGENT=FinancialSkills User

# OPTIONAL: Economic Data (FRED)
# Get free key: https://fred.stlouisfed.org/
FRED_API_KEY=${fred_key}

# OPTIONAL: Financial News
# Get free key: https://newsapi.org/
NEWS_API_KEY=${news_key}

# OPTIONAL: Alternative Market Data (Alpaca)
# Get free keys: https://alpaca.markets/
ALPACA_API_KEY=${alpaca_key}
ALPACA_SECRET_KEY=${alpaca_secret}

# Production/Advanced (requires paid subscriptions)
# VISIBLE_ALPHA_API_KEY=
# PITCHBOOK_API_KEY=
# EARNINGS_WHISPERS_KEY=
EOF

echo -e "${GREEN}✓ Configuration file created at $ENV_FILE${NC}"

# Set secure permissions
chmod 600 "$ENV_FILE"
echo -e "${GREEN}✓ File permissions set (readable only by you)${NC}"

# Add to shell profile
echo ""
echo "To use these keys, add this line to your shell profile (~/.bashrc or ~/.zshrc):"
echo ""
echo -e "${BLUE}export \$(grep -v '^#' $ENV_FILE | xargs)${NC}"
echo ""

read -p "Add this to your shell profile automatically? (y/n): " add_to_profile

if [ "$add_to_profile" = "y" ]; then
    SHELL_PROFILE=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_PROFILE="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_PROFILE="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_PROFILE="$HOME/.bash_profile"
    fi
    
    if [ -n "$SHELL_PROFILE" ]; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Financial Skills MCP Configuration" >> "$SHELL_PROFILE"
        echo "export \$(grep -v '^#' $ENV_FILE | xargs)" >> "$SHELL_PROFILE"
        echo -e "${GREEN}✓ Added to $SHELL_PROFILE${NC}"
        echo "Reload with: source $SHELL_PROFILE"
    else
        echo -e "${YELLOW}⚠ Could not find shell profile. Please add manually.${NC}"
    fi
fi

# Test Polygon key if provided
echo ""
if [ -n "$polygon_key" ]; then
    echo "Testing Polygon API key..."
    export POLYGON_API_KEY="$polygon_key"
    response=$(curl -s "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?apiKey=$POLYGON_API_KEY" | head -1)
    
    if echo "$response" | grep -q "results"; then
        echo -e "${GREEN}✓ Polygon API key is working!${NC}"
    else
        echo -e "${YELLOW}⚠ Polygon API test returned: $response${NC}"
        echo "Please verify your key at https://polygon.io/ (now Massive)"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! ✅                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary:"
echo "────────"

if [ -n "$polygon_key" ]; then
    echo -e "${GREEN}✓${NC} POLYGON_API_KEY configured"
else
    echo -e "${RED}✗${NC} POLYGON_API_KEY not set (REQUIRED for market data)"
fi

[ -n "$sec_key" ] && echo -e "${GREEN}✓${NC} SEC_API_KEY configured" || echo -e "○${NC} SEC_API_KEY not set (optional)"
[ -n "$fred_key" ] && echo -e "${GREEN}✓${NC} FRED_API_KEY configured" || echo -e "○${NC} FRED_API_KEY not set (optional)"
[ -n "$news_key" ] && echo -e "${GREEN}✓${NC} NEWS_API_KEY configured" || echo -e "○${NC} NEWS_API_KEY not set (optional)"
[ -n "$alpaca_key" ] && echo -e "${GREEN}✓${NC} Alpaca keys configured" || echo -e "○${NC} Alpaca keys not set (optional)"

echo ""
echo "Configuration file: $ENV_FILE"
echo ""
echo "Next steps:"
echo "1. Reload your shell: source ~/.bashrc (or ~/.zshrc)"
echo "2. Test the MCP integration"
echo "3. See API-KEYS-CONFIG.md for detailed documentation"
echo ""

# Optionally copy to remote VM
read -p "Deploy these keys to remote VM (weagents)? (y/n): " deploy_remote

if [ "$deploy_remote" = "y" ]; then
    echo ""
    echo "Deploying to remote VM..."
    
    # Test SSH connection
    if ssh -o ConnectTimeout=5 weagents "echo 'OK'" 2>/dev/null | grep -q "OK"; then
        # Copy .env to remote
        scp "$ENV_FILE" weagents:/opt/agents/ono-assistant/.env
        ssh weagents "chmod 600 /opt/agents/ono-assistant/.env"
        echo -e "${GREEN}✓ Keys deployed to remote VM${NC}"
        echo "Location: /opt/agents/ono-assistant/.env"
    else
        echo -e "${RED}✗ Could not connect to remote VM${NC}"
        echo "Deploy manually with:"
        echo "  scp $ENV_FILE weagents:/opt/agents/ono-assistant/.env"
    fi
fi

echo ""
echo "Done! 🎉"
