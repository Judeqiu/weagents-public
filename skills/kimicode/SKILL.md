---
name: kimicode
description: Manage and troubleshoot Kimi model configurations for OpenClaw agents. Use when checking, fixing, or updating the LLM model configuration. Helps diagnose model authentication issues, provider misconfigurations, and failover problems.
---

# KimiCode - Model Configuration Manager

Manage and troubleshoot Kimi model configurations for OpenClaw agents.

## How to Engage This Skill

> **User says:** *"My agent is using the wrong model"*
> 
> **Agent action:** Check current model config, identify issues, fix configuration

> **User says:** *"Fix my model configuration"*
> 
> **Agent action:** Check config, compare with working setup (like Kai), apply fixes

> **User says:** *"I'm getting model authentication errors"*
> 
> **Agent action:** Check API keys, model mapping, provider configuration

> **User says:** *"Update my model to match Kai"*
> 
> **Agent action:** Copy Kai's model configuration to target server

---

## Quick Diagnostics

### Check Current Model Configuration

```bash
# Check default model
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'

# Check available providers
cat ~/.openclaw/openclaw.json | jq '.models.providers | keys'

# Check specific provider config
cat ~/.openclaw/openclaw.json | jq '.models.providers."kimi-code"'

# Check agent model in logs
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep 'agent model'
```

### Verify Model is Working

```bash
# Check for model errors in logs
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -E 'ERROR|fail|timeout' | grep -i model

# Check gateway status
systemctl --user status openclaw-gateway --no-pager | head -10
```

---

## Common Issues and Fixes

### Issue 1: Wrong Model Configuration

**Symptoms:**
- Agent reports using wrong model (e.g., "Kimi K2.5 Pro" instead of "kimi-code")
- Model mapping mismatch in config

**Diagnosis:**
```bash
# Check current config
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'
# Expected: "kimi-code/kimi-for-coding"
# Wrong: "kimi-coding/k2p5" or "moonshot/kimi-k2.5"
```

**Fix:**
```bash
# Update to correct model
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary = "kimi-code/kimi-for-coding"' > /tmp/config.json && mv /tmp/config.json ~/.openclaw/openclaw.json

# Restart gateway
systemctl --user restart openclaw-gateway
```

### Issue 2: Missing kimi-code Provider

**Symptoms:**
- `kimi-code` provider not in providers list
- Agent falls back to wrong model

**Diagnosis:**
```bash
cat ~/.openclaw/openclaw.json | jq '.models.providers | keys'
# Missing: "kimi-code"
```

**Fix:** Add kimi-code provider:

```python
import json

with open('/home/USER/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)

# Add kimi-code provider
config['models']['providers']['kimi-code'] = {
    "baseUrl": "https://api.kimi.com/coding/v1",
    "api": "openai-completions",
    "models": [
        {
            "id": "kimi-for-coding",
            "name": "Kimi For Coding",
            "api": "openai-completions",
            "reasoning": True,
            "input": ["text", "image"],
            "cost": {
                "input": 0,
                "output": 0,
                "cacheRead": 0,
                "cacheWrite": 0
            },
            "contextWindow": 262144,
            "maxTokens": 32768,
            "headers": {
                "User-Agent": "KimiCLI/0.77"
            },
            "compat": {
                "supportsDeveloperRole": False
            }
        }
    ]
}

# Update default model
config['agents']['defaults']['model']['primary'] = 'kimi-code/kimi-for-coding'

with open('/home/USER/.openclaw/openclaw.json', 'w') as f:
    json.dump(config, f, indent=2)

print('Config updated!')
```

Then restart:
```bash
systemctl --user restart openclaw-gateway
```

### Issue 3: Model Authentication Errors

**Symptoms:**
- Logs show: `Invalid Authentication` or `401` errors
- API key issues

**Diagnosis:**
```bash
# Check if KIMI_API_KEY is set
cat ~/.openclaw/openclaw.json | jq '.env.KIMI_API_KEY'

# Check logs for auth errors
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i 'auth\|401'
```

**Fix:**
```bash
# Update API key in config
# Edit ~/.openclaw/openclaw.json and update env.KIMI_API_KEY
```

### Issue 4: Model Timeout / Failover

**Symptoms:**
- Logs show: `Profile kimi-coding:default timed out`
- Agent tries next account
- Slow responses

**Diagnosis:**
```bash
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i 'timeout\|failover'
```

**Fix:**
- Check network connectivity to `api.kimi.com`
- Verify API key is valid
- Check if model is overloaded

---

## Reference: Working Configuration (Kai)

### Default Model
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-code/kimi-for-coding"
      }
    }
  }
}
```

### kimi-code Provider
```json
{
  "models": {
    "providers": {
      "kimi-code": {
        "baseUrl": "https://api.kimi.com/coding/v1",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-for-coding",
            "name": "Kimi For Coding",
            "api": "openai-completions",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 262144,
            "maxTokens": 32768,
            "headers": {
              "User-Agent": "KimiCLI/0.77"
            },
            "compat": {
              "supportsDeveloperRole": false
            }
          }
        ]
      }
    }
  }
}
```

---

## Helper Script

```bash
#!/bin/bash
# check-model.sh - Quick model configuration check

echo "=== OpenClaw Model Configuration Check ==="
echo ""

echo "Default Model:"
cat ~/.openclaw/openclaw.json 2>/dev/null | jq -r '.agents.defaults.model.primary' || echo "ERROR: Cannot read config"

echo ""
echo "Available Providers:"
cat ~/.openclaw/openclaw.json 2>/dev/null | jq -r '.models.providers | keys[]' || echo "ERROR: Cannot read providers"

echo ""
echo "kimi-code Provider:"
cat ~/.openclaw/openclaw.json 2>/dev/null | jq '.models.providers."kimi-code"' 2>/dev/null || echo "NOT FOUND: kimi-code provider"

echo ""
echo "Recent Model Logs:"
tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | grep 'agent model' | tail -1 || echo "No model logs found"

echo ""
echo "Gateway Status:"
systemctl --user is-active openclaw-gateway 2>/dev/null || echo "Gateway not running"
```

---

## Troubleshooting Checklist

When user reports model issues:

1. **Check current model:**
   ```bash
   cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'
   ```

2. **Check providers:**
   ```bash
   cat ~/.openclaw/openclaw.json | jq '.models.providers | keys'
   ```

3. **Check gateway logs:**
   ```bash
   tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -E 'model|ERROR|fail'
   ```

4. **Compare with Kai:**
   ```bash
   # SSH to Kai and check its config
   ssh kai "cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'"
   ```

5. **Fix if needed:**
   - Add missing provider
   - Update default model
   - Restart gateway

6. **Verify fix:**
   ```bash
   tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep 'agent model'
   ```

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `cat ~/.openclaw/openclaw.json \| jq '.agents.defaults.model.primary'` | Check default model |
| `cat ~/.openclaw/openclaw.json \| jq '.models.providers \| keys'` | List providers |
| `systemctl --user restart openclaw-gateway` | Restart gateway |
| `tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log` | View recent logs |

---

*Skill for managing Kimi model configurations on OpenClaw agents*
