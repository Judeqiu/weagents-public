---
name: caddy-manager
description: Manage Caddy web server on Kai VM or localhost for deploying static websites with automatic HTTPS. Handles installation, configuration, deployment, and troubleshooting.
---

# Caddy Manager - Web Server Deployment

Deploy static websites with automatic HTTPS using Caddy web server. Works on both Kai VM (remote) and localhost.

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

*Skill for managing Caddy web server on Kai VM or localhost*
