# Agent Creator - Quick Start

Create new WeAgents agents in seconds.

## Usage

### Interactive Mode (Recommended)

```bash
./skills/agent-creator/scripts/create-agent.sh my-agent --interactive
```

This will prompt you for all configuration options.

### Command Line Mode

```bash
./skills/agent-creator/scripts/create-agent.sh <agent-name> [options]
```

**Options:**
- `-p, --purpose` - Agent's purpose (e.g., "Coding helper")
- `-u, --user` - Target user's name
- `-t, --timezone` - User timezone (default: UTC)
- `-v, --vibe` - Personality description
- `-e, --emoji` - Agent emoji
- `-m, --model` - Default LLM model
- `-i, --interactive` - Interactive mode
- `-h, --help` - Show help

### Examples

**Developer Assistant:**
```bash
./skills/agent-creator/scripts/create-agent.sh dev-helper \
    --purpose "Code review and debugging" \
    --user "Alex" \
    --timezone "America/New_York" \
    --vibe "Technical, precise, helpful" \
    --emoji "💻"
```

**Personal Assistant:**
```bash
./skills/agent-creator/scripts/create-agent.sh daily-helper \
    --purpose "Task management and scheduling" \
    --user "Maria" \
    --timezone "Europe/London" \
    --vibe "Friendly, organized, proactive" \
    --emoji "📅"
```

## What Gets Created

```
agents/{agent-name}/
├── .env                           # Environment configuration
├── workspace/
│   ├── SOUL.md                   # Core personality & values
│   ├── IDENTITY.md               # Specific identity details
│   ├── USER.md                   # Human user info
│   ├── MEMORY.md                 # Long-term memory
│   ├── TOOLS.md                  # Credentials index
│   ├── AGENTS.md                 # Workspace guide
│   ├── HEARTBEAT.md              # Periodic tasks
│   ├── TODO.md                   # Active tasks
│   ├── stream.md                 # Consciousness stream
│   ├── .dockerignore             # Docker exclusions
│   └── memory/
│       └── YYYY-MM-DD.md         # First daily note
├── data/
│   ├── logs/
│   ├── sessions/
│   └── cache/
└── .config/
    ├── gmail/
    └── notion/
```

## Next Steps After Creation

1. **Review Files** - Check the generated identity files
2. **Configure Tools** - Add API keys to `.config/`
3. **Update TOOLS.md** - Document your integrations
4. **Start Agent** - Launch the container

## Customization Tips

- **SOUL.md** - Edit to change core personality
- **IDENTITY.md** - Update as the agent learns
- **USER.md** - Add preferences as you discover them
- **MEMORY.md** - Curate important insights
- **HEARTBEAT.md** - Add service-specific checks
