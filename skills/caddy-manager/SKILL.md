---
name: caddy-manager
description: Manage Caddy web server on Kai VM or localhost for deploying static websites with automatic HTTPS. Includes automatic OpenClaw agent dashboard generation. Handles installation, configuration, deployment, and troubleshooting.
---

# Caddy Manager - Web Server Deployment

Deploy static websites with automatic HTTPS using Caddy web server. Works on both Kai VM (remote) and localhost. **NEW**: Automatically generate a dashboard homepage for your OpenClaw agent.

## Quick Start

```bash
# Check if Caddy is installed
caddy version

# If not installed, run auto-install
# (see Installation section below)

# Quick serve current directory (temporary)
caddy file-server --browse

# Start Caddy with config
caddy run --config Caddyfile

# Generate OpenClaw dashboard homepage
./generate-openclaw-dashboard.sh
```

---

## Installation

### Auto-Detect & Install

```bash
# Check current status
caddy version 2>/dev/null || echo "Caddy not installed"

# Install based on platform
```

### macOS (Homebrew)

```bash
# Install
brew install caddy

# Start service
brew services start caddy

# Stop service
brew services stop caddy
```

### Ubuntu/Debian (Official)

```bash
# Install official Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Enable and start
sudo systemctl enable caddy
sudo systemctl start caddy
```

### Arch Linux

```bash
sudo pacman -S caddy
sudo systemctl enable caddy
sudo systemctl start caddy
```

### Manual (Any Platform)

```bash
# Download latest release
curl -Lo caddy.tar.gz "https://github.com/caddyserver/caddy/releases/latest/download/caddy_$(uname -s)_$(uname -m).tar.gz"
tar -xzf caddy.tar.gz caddy
sudo mv caddy /usr/local/bin/
sudo chmod +x /usr/local/bin/caddy
```

---

## OpenClaw Dashboard Homepage

Automatically generate a beautiful dashboard showing your OpenClaw agent information and installed skills.

### Quick Generate

```bash
# Download and run the generator
curl -fsSL https://raw.githubusercontent.com/Judeqiu/weagents/main/skills/caddy-manager/scripts/generate-dashboard.sh | bash

# Or if you have the skill installed
cd ~/.openclaw/workspace/skills/caddy-manager
./generate-dashboard.sh
```

### What It Generates

The dashboard displays:

| Section | Information |
|---------|-------------|
| **Agent Info** | Name, Model, Version, Status |
| **System** | Hostname, Uptime, Platform |
| **Skills** | All installed skills with descriptions |
| **Channels** | Connected channels (Telegram, WhatsApp, etc.) |
| **Quick Links** | Direct links to manage your agent |

### Example Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  🤖 OpenClaw Agent Dashboard                            │
│  Agent: weagent-001  |  Model: kimi-coding/k2p5        │
├─────────────────────────────────────────────────────────┤
│  📦 Installed Skills (12)                               │
│  ├── caddy-manager    - Manage Caddy web server        │
│  ├── skill-puller     - Download skills from GitHub    │
│  ├── web-browsing     - Browse websites with browser   │
│  └── ...                                               │
├─────────────────────────────────────────────────────────┤
│  🔌 Channels                                            │
│  ├── Telegram: ✅ Connected                            │
│  └── WhatsApp: ⏳ Pending                              │
└─────────────────────────────────────────────────────────┘
```

### Manual Generation Script

```bash
#!/bin/bash
# generate-dashboard.sh - Create OpenClaw agent homepage

set -e

# Detect environment
if [[ -f /etc/caddy/Caddyfile ]]; then
    WEB_ROOT="/var/www/welcome"
    SITES_DIR="/var/www/sites"
    CADDY_ENV="production"
else
    WEB_ROOT="./sites/dashboard"
    SITES_DIR="./sites"
    CADDY_ENV="local"
fi

# Create directories
mkdir -p "$WEB_ROOT"

# Detect OpenClaw paths
if [[ -d "$HOME/.openclaw" ]]; then
    OPENCLAW_DIR="$HOME/.openclaw"
elif [[ -d "/opt/weagents/.openclaw" ]]; then
    OPENCLAW_DIR="/opt/weagents/.openclaw"
else
    OPENCLAW_DIR=""
fi

# Extract agent info
AGENT_NAME="Unknown"
AGENT_MODEL="Unknown"
OPENCLAW_VERSION="Unknown"
SKILLS_COUNT=0
SKILLS_LIST=""

if [[ -n "$OPENCLAW_DIR" && -f "$OPENCLAW_DIR/openclaw.json" ]]; then
    AGENT_NAME=$(jq -r '.agents.default // "main"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null || echo "main")
    AGENT_MODEL=$(jq -r '.agents.defaults.model.primary // "Unknown"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null || echo "Unknown")
fi

OPENCLAW_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "Unknown")

# Get skills list
SKILLS_DIR=""
if [[ -d "$HOME/.openclaw/workspace/skills" ]]; then
    SKILLS_DIR="$HOME/.openclaw/workspace/skills"
elif [[ -d "$HOME/.openclaw/agents/main/skills" ]]; then
    SKILLS_DIR="$HOME/.openclaw/agents/main/skills"
fi

if [[ -n "$SKILLS_DIR" ]]; then
    SKILLS_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
fi

# Generate HTML
cat > "$WEB_ROOT/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Agent Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .info-item {
            padding: 16px;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .info-label {
            font-size: 0.85rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .info-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }
        .skills-list {
            display: grid;
            gap: 12px;
        }
        .skill-item {
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .skill-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .skill-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
        }
        .skill-info {
            flex: 1;
        }
        .skill-name {
            font-weight: 600;
            font-size: 1.05rem;
            margin-bottom: 4px;
        }
        .skill-desc {
            font-size: 0.9rem;
            color: #666;
            line-height: 1.4;
        }
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.7);
            margin-top: 40px;
        }
        .refresh-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 30px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
            backdrop-filter: blur(10px);
        }
        .refresh-btn:hover {
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.5);
        }
        @media (max-width: 600px) {
            .header h1 { font-size: 1.8rem; }
            .card { padding: 20px; }
            .info-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 OpenClaw Agent</h1>
            <p>Dashboard and System Overview</p>
        </div>

        <div class="card">
            <div class="card-title">📊 Agent Information</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Agent Name</div>
                    <div class="info-value">{{AGENT_NAME}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Model</div>
                    <div class="info-value">{{AGENT_MODEL}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Version</div>
                    <div class="info-value">{{OPENCLAW_VERSION}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Status</div>
                    <div class="info-value">
                        <span class="status-badge status-active">● Active</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🖥️ System Information</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Hostname</div>
                    <div class="info-value">{{HOSTNAME}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Platform</div>
                    <div class="info-value">{{PLATFORM}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Uptime</div>
                    <div class="info-value">{{UPTIME}}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Skills Installed</div>
                    <div class="info-value">{{SKILLS_COUNT}}</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">📦 Installed Skills ({{SKILLS_COUNT}})</div>
            <div class="skills-list">
                {{SKILLS_LIST}}
            </div>
        </div>

        <div style="text-align: center;">
            <a href="javascript:location.reload()" class="refresh-btn">🔄 Refresh Dashboard</a>
        </div>

        <div class="footer">
            <p>Generated on {{GENERATED_DATE}} | OpenClaw Agent Dashboard</p>
        </div>
    </div>
</body>
</html>
HTMLEOF

# Replace placeholders
HOSTNAME=$(hostname)
PLATFORM=$(uname -s)
UPTIME=$(uptime -p 2>/dev/null || uptime | awk -F',' '{print $1}')
GENERATED_DATE=$(date '+%Y-%m-%d %H:%M:%S')

sed -i "s|{{AGENT_NAME}}|$AGENT_NAME|g" "$WEB_ROOT/index.html"
sed -i "s|{{AGENT_MODEL}}|$AGENT_MODEL|g" "$WEB_ROOT/index.html"
sed -i "s|{{OPENCLAW_VERSION}}|$OPENCLAW_VERSION|g" "$WEB_ROOT/index.html"
sed -i "s|{{HOSTNAME}}|$HOSTNAME|g" "$WEB_ROOT/index.html"
sed -i "s|{{PLATFORM}}|$PLATFORM|g" "$WEB_ROOT/index.html"
sed -i "s|{{UPTIME}}|$UPTIME|g" "$WEB_ROOT/index.html"
sed -i "s|{{SKILLS_COUNT}}|$SKILLS_COUNT|g" "$WEB_ROOT/index.html"
sed -i "s|{{GENERATED_DATE}}|$GENERATED_DATE|g" "$WEB_ROOT/index.html"

# Generate skills list HTML
SKILLS_HTML=""
if [[ -n "$SKILLS_DIR" ]]; then
    for skill_md in "$SKILLS_DIR"/*/SKILL.md; do
        if [[ -f "$skill_md" ]]; then
            skill_name=$(basename "$(dirname "$skill_md")")
            skill_desc=$(grep -m1 "^description:" "$skill_md" 2>/dev/null | sed 's/description: //' | tr -d '"' || echo "No description")
            skill_emoji="📋"
            
            # Assign emoji based on skill name
            case "$skill_name" in
                *browser*|*web*) skill_emoji="🌐" ;;
                *caddy*|*server*|*web*) skill_emoji="🚀" ;;
                *skill*|*pull*) skill_emoji="🧩" ;;
                *search*|*find*) skill_emoji="🔍" ;;
                *download*|*file*) skill_emoji="📥" ;;
                *chat*|*message*) skill_emoji="💬" ;;
                *email*|*mail*) skill_emoji="📧" ;;
                *security*|*guard*) skill_emoji="🔒" ;;
                *deploy*|*install*) skill_emoji="⚙️" ;;
                *research*|*analysis*) skill_emoji="📊" ;;
                *finance*|*money*) skill_emoji="💰" ;;
                *shop*|*buy*) skill_emoji="🛒" ;;
            esac
            
            SKILLS_HTML="${SKILLS_HTML}
                <div class=\"skill-item\">
                    <div class=\"skill-icon\">$skill_emoji</div>
                    <div class=\"skill-info\">
                        <div class=\"skill-name\">$skill_name</div>
                        <div class=\"skill-desc\">$skill_desc</div>
                    </div>
                </div>"
        fi
    done
fi

if [[ -z "$SKILLS_HTML" ]]; then
    SKILLS_HTML='<div class="skill-item"><div class="skill-icon">⚠️</div><div class="skill-info"><div class="skill-name">No Skills Found</div><div class="skill-desc">No skills detected in the workspace directory.</div></div></div>'
fi

# Escape for sed
SKILLS_HTML_ESCAPED=$(echo "$SKILLS_HTML" | sed 's/[&/\]/\\&/g')
sed -i "s|{{SKILLS_LIST}}|$SKILLS_HTML_ESCAPED|g" "$WEB_ROOT/index.html"

echo "✅ Dashboard generated at: $WEB_ROOT/index.html"
echo "🌐 Access it at: http://localhost"

# Set permissions for production
if [[ "$CADDY_ENV" == "production" ]]; then
    sudo chown -R caddy:caddy "$WEB_ROOT"
    sudo chmod -R 755 "$WEB_ROOT"
    
    # Reload Caddy if running
    if systemctl is-active caddy &>/dev/null; then
        sudo systemctl reload caddy
        echo "🔄 Caddy reloaded"
    fi
fi
```

---

## Environment Detection

### Detect Running Environment

| Check | Kai VM | Localhost |
|-------|--------|-----------|
| Hostname | `vps-*` or `kai` | Your machine |
| Config Path | `/etc/caddy/Caddyfile` | `./Caddyfile` or `~/.config/caddy/Caddyfile` |
| Sites Dir | `/var/www/sites/` | `./sites/` or `~/sites/` |
| Service | systemd | brew / manual |

```bash
# Detect environment
if [[ -f /etc/caddy/Caddyfile ]] && systemctl is-active caddy &>/dev/null; then
    echo "Detected: Kai/Production (systemd)"
    CADDY_ENV="production"
    CADDY_CONFIG="/etc/caddy/Caddyfile"
    SITES_DIR="/var/www/sites"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    CADDY_ENV="local"
    CADDY_CONFIG="$(brew --prefix)/etc/caddy/Caddyfile"
    SITES_DIR="$HOME/sites"
else
    echo "Detected: Local/Linux"
    CADDY_ENV="local"
    CADDY_CONFIG="./Caddyfile"
    SITES_DIR="./sites"
fi
```

---

## Local Development Setup

### Initialize Local Caddy Project

```bash
# Create project structure
mkdir -p my-website/sites/myapp
cd my-website

# Create Caddyfile for local development
cat > Caddyfile << 'EOF'
{
    auto_https off
}

:8080 {
    root * ./sites/myapp
    file_server
    encode gzip
    templates
}

:8081 {
    respond "Health OK" 200
}
EOF

# Create sample index.html
mkdir -p sites/myapp
cat > sites/myapp/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Local Site</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    </style>
</head>
<body>
    <h1>Hello from Caddy!</h1>
    <p>Local development server running on :8080</p>
</body>
</html>
EOF

# Start Caddy
caddy run --config Caddyfile
```

### Local Caddyfile Templates

#### Basic Static Site (Local)

```caddyfile
{
    auto_https off
}

:8080 {
    root * ./public
    file_server
    encode gzip
}
```

#### Multiple Sites (Local)

```caddyfile
{
    auto_https off
}

:8080 {
    root * ./site-a
    file_server
    encode gzip
}

:8081 {
    root * ./site-b
    file_server
    encode gzip
}
```

#### SPA with API Proxy (Local)

```caddyfile
{
    auto_https off
}

:8080 {
    root * ./dist
    file_server
    try_files {path} {path}/ /index.html
    
    # Proxy API calls to backend
    reverse_proxy /api/* localhost:3000
}
```

---

## Production Deployment (Kai VM)

### Architecture

- **Caddy Version**: v2.x
- **Config**: `/etc/caddy/Caddyfile`
- **Sites Directory**: `/var/www/sites/`
- **Default Welcome**: `/var/www/welcome/`
- **Service**: `caddy` (systemd)

### Site Directory Structure

```
/var/www/sites/
├── example.com/           # Domain-based site
│   ├── Caddyfile          # Site-specific Caddy configuration
│   ├── index.html         # Site files
│   └── ...
└── myapp/                 # Path-based site
    └── index.html
```

### Production Commands

```bash
# Check Server Status
sudo systemctl status caddy --no-pager

# View Logs
sudo journalctl -u caddy --no-pager -n 50

# Reload Configuration
sudo caddy fmt --overwrite /etc/caddy/Caddyfile && sudo systemctl reload caddy

# Validate Configuration
sudo caddy validate --config /etc/caddy/Caddyfile
```

---

## Deployment Methods

### Method 1: Custom Domain (Auto HTTPS)

```bash
SITE_DOMAIN="mydomain.com"
SITES_DIR="/var/www/sites"  # Or "./sites" for local

# 1. Create site directory
sudo mkdir -p "$SITES_DIR/$SITE_DOMAIN"

# 2. Create site Caddyfile
sudo tee "$SITES_DIR/$SITE_DOMAIN/Caddyfile" << EOF
$SITE_DOMAIN {
    root * $SITES_DIR/$SITE_DOMAIN
    file_server
    encode gzip
}
EOF

# 3. Upload files to $SITES_DIR/$SITE_DOMAIN/

# 4. Set permissions (production only)
[[ "$CADDY_ENV" == "production" ]] && sudo chown -R caddy:caddy "$SITES_DIR/$SITE_DOMAIN"

# 5. Reload Caddy
if [[ "$CADDY_ENV" == "production" ]]; then
    sudo systemctl reload caddy
else
    caddy reload --config Caddyfile
fi
```

### Method 2: Path-Based (No Domain)

```bash
APP_NAME="myapp"
SITES_DIR="/var/www/sites"  # Or "./sites" for local

# 1. Create site directory
sudo mkdir -p "$SITES_DIR/$APP_NAME"

# 2. Add handler to main Caddyfile
if [[ "$CADDY_ENV" == "production" ]]; then
    sudo tee -a /etc/caddy/Caddyfile << EOF

handle_path /$APP_NAME/* {
    root * $SITES_DIR/$APP_NAME
    file_server
    encode gzip
}
EOF
    sudo caddy fmt --overwrite /etc/caddy/Caddyfile
    sudo systemctl reload caddy
else
    # For local, edit your Caddyfile manually or use port-based routing
    echo "Add to your Caddyfile:"
    echo ":8080/$APP_NAME/* {"
    echo "    root * $SITES_DIR/$APP_NAME"
    echo "    file_server"
    echo "}"
fi
```

### Method 3: Reverse Proxy

```bash
DOMAIN="api.example.com"
BACKEND_PORT=3000

sudo tee "$SITES_DIR/$DOMAIN/Caddyfile" << EOF
$DOMAIN {
    reverse_proxy localhost:$BACKEND_PORT
    encode gzip
}
EOF

sudo systemctl reload caddy
```

---

## Common Patterns

### Basic Static Site

```caddyfile
domain.com {
    root * /var/www/sites/domain.com
    file_server
    encode gzip
}
```

### SPA (Single Page Application)

```caddyfile
domain.com {
    root * /var/www/sites/domain.com
    file_server
    encode gzip
    try_files {path} {path}/ /index.html
}
```

### PHP Site (requires php-fpm)

```caddyfile
domain.com {
    root * /var/www/sites/domain.com
    encode gzip
    php_fastcgi unix//run/php/php8.1-fpm.sock
    file_server
}
```

### Redirect www to non-www

```caddyfile
www.domain.com {
    redir https://domain.com{uri} permanent
}

domain.com {
    root * /var/www/sites/domain.com
    file_server
}
```

---

## Site Management

### List Sites

```bash
# Production
ls -la /var/www/sites/

# Local
ls -la ./sites/
```

### Delete Site

```bash
SITE="mydomain.com"
SITES_DIR="/var/www/sites"  # Or "./sites"

# Remove site files
sudo rm -rf "$SITES_DIR/$SITE"

# Remove from main Caddyfile if path-based
# (edit /etc/caddy/Caddyfile manually)

# Reload
[[ "$CADDY_ENV" == "production" ]] && sudo systemctl reload caddy
```

### Deploy from Git

```bash
SITE="myapp"
REPO="https://github.com/user/repo.git"
SITES_DIR="/var/www/sites"

cd "$SITES_DIR"
sudo git clone "$REPO" "$SITE"
sudo chown -R caddy:caddy "$SITE"

# Or pull updates
cd "$SITES_DIR/$SITE" && sudo git pull

sudo systemctl reload caddy
```

---

## Troubleshooting

### Check if Caddy is Running

```bash
# Any platform
curl -s http://localhost:2019/config/ | head

# Linux with systemd
systemctl is-active caddy

# macOS with brew
brew services list | grep caddy
```

### View Logs

```bash
# systemd (production)
sudo journalctl -u caddy -n 100 --no-pager

# macOS (Homebrew)
log show --predicate 'process == "caddy"' --last 1h

# Local (foreground)
caddy run --config Caddyfile 2>&1
```

### Validate Configuration

```bash
# Production
sudo caddy validate --config /etc/caddy/Caddyfile

# Local
caddy validate --config Caddyfile
```

### Fix Permissions (Production)

```bash
sudo chown -R caddy:caddy /var/www/sites/
sudo chmod -R 755 /var/www/sites/
```

### Test Site

```bash
# Test locally
curl -s http://localhost -H 'Host: mydomain.com'

# Check headers
curl -I http://localhost

# Follow redirects
curl -L http://localhost
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 80/443 in use | `sudo lsof -i :80` to find process |
| Permission denied | Check `chown -R caddy:caddy` on sites dir |
| Config error | Run `caddy validate --config Caddyfile` |
| HTTPS not working | Ensure ports 80/443 open, DNS points to server |
| 404 errors | Check root path, file permissions |

---

## Quick Reference

### Commands

| Command | Description |
|---------|-------------|
| `caddy version` | Check version |
| `caddy run` | Run in foreground |
| `caddy start` | Start as daemon |
| `caddy stop` | Stop daemon |
| `caddy reload` | Reload config |
| `caddy validate` | Validate config |
| `caddy fmt` | Format config |
| `caddy file-server` | Quick static server |
| `caddy reverse-proxy` | Quick reverse proxy |

### Environment Variables

```bash
# Use custom config path
export CADDY_CONFIG=/path/to/Caddyfile

# Change data directory
export CADDY_DATA_DIR=/var/lib/caddy
```

---

*Skill for managing Caddy web server with OpenClaw dashboard generation*
