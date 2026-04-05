---
name: openclaw-kimi-setup
description: Use when deploying Moonshot Kimi K2.5 model to OpenClaw, configuring OpenClaw to use Kimi as the default LLM, or setting up multiple LLM providers with Kimi
---

# OpenClaw Kimi Setup

Deploy Moonshot Kimi K2.5 model to OpenClaw and set it as the default model.

## Overview

Automated deployment of Moonshot Kimi K2.5 to OpenClaw with proper API configuration, endpoint setup, and default model assignment.

## Quick Deploy

Deploy Kimi and set as default in one command:

```bash
ssh <your-host> << 'DEPLOY'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# 1. Set API key
openclaw config set env.MOONSHOT_API_KEY "your-api-key-here"

# 2. Configure Moonshot provider
openclaw config set models.providers.moonshot '{
  "baseUrl": "https://api.moonshot.ai/v1",
  "apiKey": "${env.MOONSHOT_API_KEY}",
  "api": "openai-completions",
  "authHeader": true,
  "models": [
    {
      "id": "kimi-k2.5",
      "name": "Kimi K2.5",
      "reasoning": false,
      "input": ["text"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 256000,
      "maxTokens": 8192
    }
  ]
}'

# 3. Add model alias
openclaw config set agents.defaults.models."moonshot/kimi-k2.5" '{"alias": "Kimi25"}'

# 4. Set as default
openclaw config set agents.defaults.model.primary "moonshot/kimi-k2.5"

# 5. Validate and restart
openclaw config validate && pkill -f "openclaw-gateway" 2>/dev/null; nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &

echo "✅ Kimi K2.5 deployed and set as default"
DEPLOY
```

## Configuration Reference

| Setting | Value | Notes |
|---------|-------|-------|
| Base URL | `https://api.moonshot.ai/v1` | International endpoint |
| API Type | `openai-completions` | OpenAI-compatible |
| Model ID | `kimi-k2.5` | Use `moonshot/kimi-k2.5` ref |
| Context | 256,000 tokens | Max context window |
| Max Tokens | 8,192 | Output limit |

## Alternative: China Endpoint

For China region, use `https://api.moonshot.cn/v1` instead.

## Verification

Check deployment:

```bash
ssh <your-host> << 'CHECK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

echo "Primary Model: $(openclaw config get agents.defaults.model.primary)"
echo "Providers: $(openclaw config get models.providers | grep -o '"[a-z-]*":' | tr -d '":')"
echo "Gateway: $(pgrep -f 'openclaw-gateway' > /dev/null && echo 'Running' || echo 'Stopped')"
CHECK
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrong endpoint | Use `api.moonshot.ai` not `api.moonshot.cn` for international |
| Invalid API type | Must be `openai-completions`, not `openai` or `openai-responses` |
| Missing model alias | Add alias in `agents.defaults.models` for easy reference |
| Gateway not restarted | Always restart gateway after model config changes |

## Model Switching

Switch back to another model:

```bash
openclaw config set agents.defaults.model.primary "minimax/MiniMax-M2.5"
# or
openclaw config set agents.defaults.model.primary "openai/gpt-4o"
```
