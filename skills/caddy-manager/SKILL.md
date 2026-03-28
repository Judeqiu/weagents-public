---
name: caddy-manager
description: Manage Caddy web server on Kai VM for deploying static websites. Use when deploying web pages, managing sites, configuring domains, or troubleshooting the web server.
---

# Caddy Manager - Kai Web Server

Caddy is installed on the Kai VM (ssh kai) as a production-ready web server with automatic HTTPS.

## Architecture

- **Caddy Version**: v2.x
- **Config**: `/etc/caddy/Caddyfile`
- **Sites Directory**: `/var/www/sites/`
- **Default Welcome**: `/var/www/welcome/`
- **Service**: `caddy` (systemd)

## Site Directory Structure

```
/var/www/sites/
├── example.com/           # Domain-based site
│   ├── Caddyfile          # Site-specific Caddy configuration
│   ├── index.html         # Site files
│   └── ...
└── myapp/                 # Path-based site
    └── index.html
```

## Quick Commands

### Check Server Status
```bash
sudo systemctl status caddy --no-pager
```

### View Logs
```bash
sudo journalctl -u caddy --no-pager -n 50
```

### Reload Configuration
```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

### Validate Configuration
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

## Deploying a New Site

### Method 1: With Custom Domain (Auto HTTPS)

```bash
# 1. Create site directory
sudo mkdir -p /var/www/sites/mydomain.com

# 2. Create site Caddyfile
sudo tee /var/www/sites/mydomain.com/Caddyfile << 'EOF'
mydomain.com {
    root * /var/www/sites/mydomain.com
    file_server
    encode gzip
}
EOF

# 3. Upload files to /var/www/sites/mydomain.com/

# 4. Set permissions
sudo chown -R caddy:caddy /var/www/sites/mydomain.com

# 5. Reload Caddy
sudo systemctl reload caddy
```

### Method 2: Path-Based (No Domain)

```bash
# 1. Create site directory and upload files
sudo mkdir -p /var/www/sites/myapp

# 2. Add handler to main Caddyfile
sudo tee -a /etc/caddy/Caddyfile << 'EOF'

handle_path /myapp/* {
    root * /var/www/sites/myapp
    file_server
    encode gzip
}
EOF

# 3. Reload Caddy
sudo caddy fmt --overwrite /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

### Method 3: Reverse Proxy

```bash
sudo tee /var/www/sites/api.example.com/Caddyfile << 'EOF'
api.example.com {
    reverse_proxy localhost:3000
    encode gzip
}
EOF

sudo systemctl reload caddy
```

## Common Patterns

### Path-Based Site with Trailing Slash Redirect
When serving a site at a subpath, add a redirect so `/path` works without the trailing slash:

```caddyfile
:80 {
    # Redirect /myapp to /myapp/
    redir /myapp /myapp/ permanent
    
    handle_path /myapp/* {
        root * /var/www/sites/myapp
        file_server
        encode gzip
    }
}
```

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

## Site Management

### List Sites
```bash
ls -la /var/www/sites/
```

### Delete Site
```bash
sudo rm -rf /var/www/sites/mydomain.com
sudo systemctl reload caddy
```

## Troubleshooting

### Check Config
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo journalctl -u caddy -n 100 --no-pager
```

### Fix Permissions
```bash
sudo chown -R caddy:caddy /var/www/sites/
```

### Test Site
```bash
curl -s http://localhost -H 'Host: mydomain.com'
```
