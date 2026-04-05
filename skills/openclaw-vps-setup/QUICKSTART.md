# OpenClaw VPS Quickstart

## 1-Minute Setup (Copy & Paste)

```bash
# SSH to your VPS
ssh user@your-vps-ip

# Install everything
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 22 && nvm use 22 && nvm alias default 22
curl -fsSL https://get.pnpm.io/install.sh | sh -
export PNPM_HOME="$HOME/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH"
pnpm add -g openclaw

# Configure
openclaw setup
openclaw config set gateway.mode local
echo 'KIMI_API_KEY=your-key' >> ~/.openclaw/.env
openclaw config set agents.defaults.model.primary 'kimi-coding/k2p5'

# Start
openclaw gateway install
systemctl --user start openclaw-gateway

# Done!
openclaw status
```

## Essential Commands

```bash
# Check status
openclaw status

# View logs
journalctl --user -u openclaw-gateway -f

# Restart
systemctl --user restart openclaw-gateway

# Access dashboard (from local machine)
ssh -L 18789:localhost:18789 user@your-vps-ip
# Then open: http://localhost:18789/
```

## File Locations

| File | Path |
|------|------|
| Config | `~/.openclaw/openclaw.json` |
| Secrets | `~/.openclaw/.env` |
| Auth | `~/.openclaw/auth-profiles.json` |
| Workspace | `~/.openclaw/workspace/` |
| Logs | `~/.openclaw/logs/` |
| Service | `~/.config/systemd/user/openclaw-gateway.service` |

## Troubleshooting

**Gateway won't start:**
```bash
journalctl --user -u openclaw-gateway -n 50
openclaw config set gateway.mode local
systemctl --user restart openclaw-gateway
```

**Node version error:**
```bash
nvm use 22
nvm alias default 22
```

**Permission denied:**
```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/.env
chmod 600 ~/.openclaw/auth-profiles.json
```
