# API Keys & Configuration Guide

Complete list of API keys needed for MCP integration and how to configure them.

---

## Quick Reference: Required Keys

### Free Tier (Development)
| Service | Key Name | Cost | Required For |
|---------|----------|------|--------------|
| Massive (formerly Polygon.io) | `POLYGON_API_KEY` | Free (5/min) | Stock prices, historical data |
| SEC EDGAR | None | Free | Company filings |
| SEC Enhanced | `SEC_API_KEY` | $0-85/mo | Better structured data |
| FRED | `FRED_API_KEY` | Free | Economic indicators |
| NewsAPI | `NEWS_API_KEY` | Free (100/day) | Financial news |

### Paid Tier (Production)
| Service | Key Name | Cost | Required For |
|---------|----------|------|--------------|
| Polygon Pro | `POLYGON_API_KEY` | $49/mo | Unlimited API calls |
| Alpaca | `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` | Free | Real-time data |
| Visible Alpha | `VISIBLE_ALPHA_API_KEY` | $$$ | Analyst estimates |
| PitchBook | `PITCHBOOK_API_KEY` | $$$ | M&A transactions |
| Earnings Whispers | `EARNINGS_WHISPERS_KEY` | $19/mo | Earnings calendar |

---

## Detailed Configuration

### 1. Polygon.io API Key (RECOMMENDED - START HERE)

**What it provides:**
- Real-time and historical stock prices
- Company profiles and financial data
- 5 API calls/minute (free tier)
- Unlimited calls (paid tier)

**How to get it:**

1. Go to https://polygon.io/ (Massive)
2. Click "Get Started"
3. Create a free account
4. Navigate to Dashboard → API Keys
5. Copy your API key (starts with "pk_")

**Configure it:**

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, or ~/.bash_profile)
export POLYGON_API_KEY="pk_your_key_here"

# Or set for current session only
export POLYGON_API_KEY="pk_your_key_here"

# Verify it's set
echo $POLYGON_API_KEY
```

**Test it works:**

```bash
curl "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?apiKey=$POLYGON_API_KEY"
```

**Expected output:**
```json
{
  "ticker": "AAPL",
  "results": [{
    "c": 185.64,
    "h": 186.50,
    "l": 184.20,
    "o": 184.80,
    "v": 52438921
  }]
}
```

---

### 2. SEC API Key (Optional - Enhanced Data)

**What it provides:**
- Structured SEC filings
- Financial statements (standardized)
- Insider trading data
- Better than raw EDGAR

**How to get it:**

1. Go to https://sec-api.io/
2. Click "Get API Key"
3. Create account
4. Copy your API key

**Configure it:**

```bash
export SEC_API_KEY="your_sec_api_key_here"
export SEC_USER_AGENT="YourName your@email.com"
```

**Alternative (Free - Official EDGAR):**
No API key needed! Just rate limits (10 requests/second).

---

### 3. Alpaca API Key (Optional - Real-time)

**What it provides:**
- Real-time market data
- Historical data
- Unlimited free tier

**How to get it:**

1. Go to https://alpaca.markets/
2. Click "Get Started"
3. Create account (paper trading is free)
4. Go to Dashboard → API Keys
5. Copy both API Key ID and Secret Key

**Configure it:**

```bash
export ALPACA_API_KEY="PKyour_key_here"
export ALPACA_SECRET_KEY="your_secret_here"
```

---

### 4. FRED API Key (Economic Data)

**What it provides:**
- GDP, CPI, unemployment
- Interest rates
- Industry data
- Completely free

**How to get it:**

1. Go to https://fred.stlouisfed.org/
2. Click "My Account" → "API Keys"
3. Request API key (instant approval)
4. Copy your key

**Configure it:**

```bash
export FRED_API_KEY="your_fred_key_here"
```

---

### 5. NewsAPI Key (News & Sentiment)

**What it provides:**
- Financial news articles
- 100 requests/day (free)

**How to get it:**

1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Create free account
4. Copy your key

**Configure it:**

```bash
export NEWS_API_KEY="your_newsapi_key_here"
```

---

## Complete Environment Setup

### Option 1: Direct Environment Variables

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Financial Skills MCP Configuration
# =================================

# Market Data (Polygon - REQUIRED)
export POLYGON_API_KEY="pk_your_polygon_key_here"

# Alternative Market Data (Alpaca - Optional)
export ALPACA_API_KEY="PKyour_alpaca_key"
export ALPACA_SECRET_KEY="your_alpaca_secret"

# SEC Filings (Optional but recommended)
export SEC_API_KEY="your_sec_api_key_here"
export SEC_USER_AGENT="YourName your@email.com"

# Economic Data (FRED - Optional)
export FRED_API_KEY="your_fred_key_here"

# News (NewsAPI - Optional)
export NEWS_API_KEY="your_newsapi_key_here"

# For production/advanced features:
# export VISIBLE_ALPHA_API_KEY="your_key"
# export PITCHBOOK_API_KEY="your_key"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: .env File (Recommended for Development)

Create file `/Users/zhengqingqiu/projects/weagents/.env`:

```bash
# Copy this file to .env and fill in your keys
# DO NOT commit .env to git!

# Required
POLYGON_API_KEY=pk_your_key_here

# Optional
SEC_API_KEY=your_sec_key_here
SEC_USER_AGENT=YourName your@email.com
ALPACA_API_KEY=PKyour_key_here
ALPACA_SECRET_KEY=your_secret_here
FRED_API_KEY=your_fred_key_here
NEWS_API_KEY=your_newsapi_key_here
```

Load it:
```bash
# Add to ~/.bashrc:
export $(grep -v '^#' /Users/zhengqingqiu/projects/weagents/.env | xargs)

# Or manually:
source /Users/zhengqingqiu/projects/weagents/.env
```

### Option 3: MCP Configuration File

Create file `~/.mcp/config.json`:

```json
{
  "servers": {
    "market-data": {
      "env": {
        "POLYGON_API_KEY": "${POLYGON_API_KEY}",
        "ALPACA_API_KEY": "${ALPACA_API_KEY}",
        "ALPACA_SECRET_KEY": "${ALPACA_SECRET_KEY}"
      }
    },
    "sec-edgar": {
      "env": {
        "SEC_API_KEY": "${SEC_API_KEY}",
        "SEC_USER_AGENT": "${SEC_USER_AGENT}"
      }
    },
    "economic-data": {
      "env": {
        "FRED_API_KEY": "${FRED_API_KEY}"
      }
    },
    "news-sentiment": {
      "env": {
        "NEWS_API_KEY": "${NEWS_API_KEY}"
      }
    }
  }
}
```

---

## Remote VM Configuration

Since you deployed to the remote VM, configure keys there:

### Step 1: SSH to Remote
```bash
ssh weagents
```

### Step 2: Create Environment File
```bash
cat > /opt/agents/ono-assistant/.env << 'EOF'
# Financial Skills API Keys
POLYGON_API_KEY=pk_your_key_here
SEC_API_KEY=your_sec_key_here
SEC_USER_AGENT=YourName your@email.com
FRED_API_KEY=your_fred_key_here
NEWS_API_KEY=your_newsapi_key_here
EOF
```

### Step 3: Load Environment in Agent
Add to agent startup script or systemd service:
```bash
# In /opt/agents/ono-assistant/.env
set -a
source /opt/agents/ono-assistant/.env
set +a
```

### Step 4: Test on Remote
```bash
ssh weagents "source /opt/agents/ono-assistant/.env && python3 -c 'import os; print(os.getenv(\"POLYGON_API_KEY\", \"NOT SET\"))'"
```

---

## Minimal Configuration (Free Tier)

For basic functionality, you only need **ONE** key:

```bash
export POLYGON_API_KEY="pk_your_key_here"
```

That's it! Everything else works with fallbacks or free alternatives.

---

## Testing All Keys

Create test script `test-api-keys.sh`:

```bash
#!/bin/bash

echo "Testing API Keys Configuration"
echo "==============================="
echo ""

# Test Polygon
if [ -n "$POLYGON_API_KEY" ]; then
    echo "✓ POLYGON_API_KEY is set"
    response=$(curl -s "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?apiKey=$POLYGON_API_KEY" | head -1)
    if echo "$response" | grep -q "results"; then
        echo "  ✓ Polygon API is working"
    else
        echo "  ✗ Polygon API test failed"
    fi
else
    echo "✗ POLYGON_API_KEY is NOT set"
fi

# Test SEC API
if [ -n "$SEC_API_KEY" ]; then
    echo "✓ SEC_API_KEY is set"
else
    echo "○ SEC_API_KEY is NOT set (optional)"
fi

# Test Alpaca
if [ -n "$ALPACA_API_KEY" ] && [ -n "$ALPACA_SECRET_KEY" ]; then
    echo "✓ Alpaca keys are set"
else
    echo "○ Alpaca keys are NOT set (optional)"
fi

# Test FRED
if [ -n "$FRED_API_KEY" ]; then
    echo "✓ FRED_API_KEY is set"
else
    echo "○ FRED_API_KEY is NOT set (optional)"
fi

# Test NewsAPI
if [ -n "$NEWS_API_KEY" ]; then
    echo "✓ NEWS_API_KEY is set"
else
    echo "○ NEWS_API_KEY is NOT set (optional)"
fi

echo ""
echo "==============================="
echo "Required for basic functionality: POLYGON_API_KEY"
echo "All others are optional enhancements"
```

Run it:
```bash
chmod +x test-api-keys.sh
./test-api-keys.sh
```

---

## Troubleshooting

### Key Not Working

**Problem:** `POLYGON_API_KEY not set` error

**Solution:**
```bash
# Check if set
echo $POLYGON_API_KEY

# If empty, set it
export POLYGON_API_KEY="pk_your_actual_key"

# Make permanent
echo 'export POLYGON_API_KEY="pk_your_actual_key"' >> ~/.bashrc
source ~/.bashrc
```

### Rate Limit Exceeded

**Problem:** `Rate limit exceeded` from Polygon

**Solution:**
- Wait 1 minute (free tier: 5 calls/min)
- Or upgrade to paid tier ($49/mo unlimited)
- Or implement caching (see MCP implementation guide)

### Key Expired

**Problem:** API returns `Invalid API key`

**Solution:**
1. Log into provider dashboard
2. Generate new key
3. Update your `.env` or shell profile
4. Reload configuration

---

## Security Best Practices

### ✅ DO:
- Store keys in environment variables
- Use `.env` files (not committed to git)
- Set file permissions: `chmod 600 .env`
- Rotate keys periodically
- Use different keys for dev/prod

### ❌ DON'T:
- Hardcode keys in scripts
- Commit keys to git
- Share keys in chat/messages
- Use production keys for development

### .gitignore Setup

Add to `.gitignore`:
```bash
# API Keys
.env
.env.local
.env.production
*.key
*.secret
```

---

## Key Rotation Schedule

| Environment | Rotation Frequency | How |
|-------------|-------------------|-----|
| Development | Every 6 months | Manual |
| Production | Every 3 months | Automated |
| Shared/Team | Every 1 month | Immediate if leaked |

---

## Cost Monitoring

### Set Up Alerts

**Polygon.io:**
- Dashboard shows usage
- Email alerts at 80% of limit

**Custom monitoring script:**
```bash
#!/bin/bash
# Add to cron (runs daily)

USAGE=$(curl -s "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?apiKey=$POLYGON_API_KEY" -w "%{http_code}" -o /dev/null)

if [ "$USAGE" == "429" ]; then
    echo "Rate limit hit!" | mail -s "Polygon API Alert" your@email.com
fi
```

---

## Summary

| Priority | Key | Provider | Cost | Setup Time |
|----------|-----|----------|------|------------|
| 🔴 Required | `POLYGON_API_KEY` | Polygon.io | Free | 5 min |
| 🟡 Recommended | `SEC_API_KEY` | sec-api.io | $85/mo | 5 min |
| 🟢 Optional | `FRED_API_KEY` | FRED | Free | 5 min |
| 🟢 Optional | `NEWS_API_KEY` | NewsAPI | Free | 5 min |
| 🔵 Advanced | `VISIBLE_ALPHA_API_KEY` | Visible Alpha | $$$ | Contact sales |
| 🔵 Advanced | `PITCHBOOK_API_KEY` | PitchBook | $$$ | Contact sales |

**Bottom line:** Start with just Polygon (free, 5 min setup), add others as needed.
