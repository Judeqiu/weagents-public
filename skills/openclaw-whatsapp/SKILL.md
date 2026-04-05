---
name: openclaw-whatsapp
description: Connect OpenClaw AI agent to WhatsApp for receiving and responding to messages. Use when setting up WhatsApp integration for OpenClaw, configuring WhatsApp Web bridge, managing WhatsApp bot authentication, or troubleshooting WhatsApp connectivity issues. Works with VPS deployments via SSH using remote-ops skill.
---

# OpenClaw WhatsApp Integration

Connect your OpenClaw AI agent to WhatsApp using WhatsApp Web. Receive messages from WhatsApp and have OpenClaw respond intelligently.

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  WhatsApp   │────▶│ whatsapp-web │────▶│  OpenClaw   │
│   Mobile    │     │    .js       │     │   Gateway   │
└─────────────┘     └──────────────┘     └─────────────┘
                              │                  │
                              └──────────────────┘
                                    Response
```

## Prerequisites

- OpenClaw installed and running on VPS (see `openclaw-vps-setup` skill)
- Node.js 18+ on the VPS
- WhatsApp app on your phone (for QR scan)
- SSH access to the VPS (see `remote-ops` skill)

## Quick Setup (5 Minutes)

### Step 1: Install WhatsApp Bridge on VPS

```bash
ssh your-vps << 'INSTALL'
# Create directory for WhatsApp bridge
mkdir -p ~/.openclaw/whatsapp-bridge
cd ~/.openclaw/whatsapp-bridge

# Initialize npm project
npm init -y

# Install dependencies
npm install whatsapp-web.js qrcode-terminal axios

# Create auth directory
mkdir -p auth
INSTALL
```

### Step 2: Copy Bridge Script

Copy `scripts/whatsapp-bridge.js` to `~/.openclaw/whatsapp-bridge/` on the VPS.

```bash
scp scripts/whatsapp-bridge.js your-vps:~/.openclaw/whatsapp-bridge/
```

### Step 3: Configure Environment

```bash
ssh your-vps << 'CONFIG'
cd ~/.openclaw/whatsapp-bridge

# Create .env file
cat > .env << 'EOF'
# OpenClaw Gateway URL (default: http://localhost:3000)
OPENCLAW_GATEWAY_URL=http://localhost:3000

# Security: Only allow these phone numbers (with country code)
# Format: 65912345678 (Singapore), 86138xxxxxxxx (China)
ALLOWED_NUMBERS=65912345678,65987654321

# Optional: Block specific numbers
BLOCKED_NUMBERS=

# Debug mode (true/false)
DEBUG=false
EOF

# Secure the file
chmod 600 .env
CONFIG
```

### Step 4: Run and Scan QR Code

```bash
ssh your-vps -t "cd ~/.openclaw/whatsapp-bridge && node whatsapp-bridge.js"
```

**First time only:** A QR code will appear in the terminal. Scan it with WhatsApp on your phone:
1. Open WhatsApp → Settings → Linked Devices
2. Tap "Link a Device"
3. Scan the QR code shown in terminal

### Step 5: Run as Service (Recommended)

```bash
ssh your-vps << 'SERVICE'
# Create systemd user service
cat > ~/.config/systemd/user/openclaw-whatsapp.service << 'EOF'
[Unit]
Description=OpenClaw WhatsApp Bridge
After=openclaw-gateway.service

[Service]
Type=simple
WorkingDirectory=%h/.openclaw/whatsapp-bridge
ExecStart=/usr/bin/node %h/.openclaw/whatsapp-bridge/whatsapp-bridge.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user daemon-reload
systemctl --user enable openclaw-whatsapp
systemctl --user start openclaw-whatsapp

# Check status
systemctl --user status openclaw-whatsapp
SERVICE
```

## Usage

Once connected, any message sent to your WhatsApp number from an allowed phone number will be:
1. Received by the WhatsApp bridge
2. Forwarded to OpenClaw gateway
3. Processed by OpenClaw AI
4. Response sent back via WhatsApp

### Test the Connection

Send a message to your WhatsApp number:
```
Hello, what can you do?
```

You should receive an AI-generated response from OpenClaw.

## Managing the Bridge

### View Logs
```bash
ssh your-vps "journalctl --user -u openclaw-whatsapp -f"
```

### Restart Bridge
```bash
ssh your-vps "systemctl --user restart openclaw-whatsapp"
```

### Stop Bridge
```bash
ssh your-vps "systemctl --user stop openclaw-whatsapp"
```

### Update Allowed Numbers

Edit the `.env` file:
```bash
ssh your-vps "nano ~/.openclaw/whatsapp-bridge/.env"
# Then restart
ssh your-vps "systemctl --user restart openclaw-whatsapp"
```

## Security Configuration

### Allowlist (Recommended)

Only allow specific phone numbers:
```bash
# In .env file
ALLOWED_NUMBERS=65912345678,86138xxxxxxxx
```

Phone number format:
- Include country code (no + or 00)
- Singapore: `65912345678`
- China: `86138xxxxxxxx`
- US: `14155552671`

### Open Mode (Not Recommended)

Allow any WhatsApp user:
```bash
# In .env file
ALLOWED_NUMBERS=*
```

## Troubleshooting

### QR Code Not Showing

```bash
# Run in foreground to see output
ssh your-vps -t "cd ~/.openclaw/whatsapp-bridge && node whatsapp-bridge.js"

# Check for errors
ssh your-vps "cat ~/.openclaw/whatsapp-bridge/.wwebjs_auth/session-*/Default/Preferences 2>/dev/null || echo 'No session yet'"
```

### Session Expired / Need to Re-authenticate

```bash
# Clear auth data and re-scan
ssh your-vps << 'RESET'
cd ~/.openclaw/whatsapp-bridge
systemctl --user stop openclaw-whatsapp
rm -rf .wwebjs_auth
systemctl --user start openclaw-whatsapp
RESET
```

### Bridge Connected but No Response

```bash
# Check if OpenClaw gateway is running
ssh your-vps "systemctl --user status openclaw-gateway"

# Check gateway health
ssh your-vps "curl -s http://localhost:3000/health"

# Check bridge logs
ssh your-vps "journalctl --user -u openclaw-whatsapp -n 50"
```

### Message Not Being Forwarded

Check debug logs:
```bash
ssh your-vps << 'DEBUG'
cd ~/.openclaw/whatsapp-bridge
systemctl --user stop openclaw-whatsapp
DEBUG=true node whatsapp-bridge.js
DEBUG
```

### Phone Number Format Issues

WhatsApp phone numbers must:
- Include country code
- Not include + or 00 prefix
- Not include spaces or dashes

Correct: `65912345678`
Incorrect: `+65 9123 4568` or `0065912345678`

## Scripts Reference

| Script | Purpose | Location |
|--------|---------|----------|
| `whatsapp-bridge.js` | Main bridge script | `~/.openclaw/whatsapp-bridge/` |
| `setup-whatsapp.sh` | Automated setup | `scripts/` |

## Architecture

The WhatsApp bridge acts as a middleware:

1. **WhatsApp Web** (`whatsapp-web.js`)
   - Connects to WhatsApp servers via WhatsApp Web protocol
   - Receives incoming messages
   - Sends responses back

2. **OpenClaw Gateway** (REST API)
   - Bridge POSTs messages to `/v1/messages`
   - Gateway processes with AI
   - Response returned in HTTP response

3. **Session Persistence**
   - Authentication stored in `.wwebjs_auth/`
   - No need to scan QR after first setup
   - Session survives restarts

## File Locations

On the VPS:
```
~/.openclaw/whatsapp-bridge/
├── whatsapp-bridge.js    # Main script
├── .env                  # Configuration
├── .wwebjs_auth/         # Session data
├── package.json          # Node dependencies
└── node_modules/         # Installed packages
```

## Integration with remote-ops Skill

This skill works seamlessly with `remote-ops`:

```bash
# If using weagents server from remote-ops
ssh weagents "mkdir -p ~/.openclaw/whatsapp-bridge"
scp scripts/whatsapp-bridge.js weagents:~/.openclaw/whatsapp-bridge/
# Continue with setup...
```

## Multi-Number Setup

To run multiple WhatsApp numbers on one VPS:

```bash
ssh your-vps << 'MULTI'
# Create second instance
mkdir -p ~/.openclaw/whatsapp-bridge-2
cd ~/.openclaw/whatsapp-bridge-2
npm init -y
npm install whatsapp-web.js qrcode-terminal axios

# Copy and modify bridge script
sed 's/3000/3001/g' ../whatsapp-bridge/whatsapp-bridge.js > whatsapp-bridge.js

# Create .env with different settings
cat > .env << 'EOF'
OPENCLAW_GATEWAY_URL=http://localhost:3000
ALLOWED_NUMBERS=65999999999
SESSION_PREFIX=session2
EOF

# Run on different port or use pm2
MULTI
```

## Alternative: Using PM2

For better process management:

```bash
ssh your-vps << 'PM2'
npm install -g pm2

cd ~/.openclaw/whatsapp-bridge
pm2 start whatsapp-bridge.js --name openclaw-whatsapp
pm2 save
pm2 startup

# Monitor
pm2 logs openclaw-whatsapp
PM2
```

## See Also

- `openclaw-vps-setup` - Set up OpenClaw on VPS
- `remote-ops` - SSH operations to VPS
- `provisionclaw` - Complete OpenClaw provisioning
