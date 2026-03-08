# Financial Skills Remote Deployment Plan

Deploying financial skills to weagents remote VM using remote-ops skill.

## Target Server

| Property | Value |
|----------|-------|
| **Host** | `weagents` (152.42.253.91) |
| **User** | `root` |
| **SSH Key** | `~/.ssh/id_ed25519_weagents` |
| **Destination** | `/opt/agents/ono-assistant/workspace/skills/` |

## Skills to Deploy

1. `financial-analysis-core/` - Valuation tools
2. `investment-banking/` - M&A tools
3. `equity-research/` - Stock analysis
4. `private-equity/` - LBO tools

Plus documentation:
- `README.md` - Ecosystem overview
- `TUTORIAL.md` - Complete tutorial
- `HOW-TO-TALK-TO-AI.md` - Conversation guide
- `CONVERSATION-CHEATSHEET.md` - Quick phrases
- `SIMPLE-GUIDE.md` - Beginner guide
- `START-HERE.md` - Quick start
- `VISUAL-GUIDE.md` - Visual guide
- `QUICK-REFERENCE.md` - Cheat sheet

## Deployment Steps

### Step 1: Test Connection
```bash
ssh weagents "echo 'Connected successfully' && hostname"
```

### Step 2: Create Skills Directory Structure
```bash
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts"
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/examples"
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/investment-banking/scripts"
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/equity-research/examples"
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/private-equity/examples"
```

### Step 3: Transfer Core Skill Files

#### financial-analysis-core
```bash
# SKILL.md and README
scp skills/financial-analysis-core/SKILL.md weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/
scp skills/financial-analysis-core/README.md weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/
scp skills/financial-analysis-core/requirements.txt weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/

# Scripts
scp skills/financial-analysis-core/scripts/generate-comps.py weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts/
scp skills/financial-analysis-core/scripts/generate-dcf.py weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts/

# Examples
scp skills/financial-analysis-core/examples/sample-comps-report.md weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/examples/
scp skills/financial-analysis-core/examples/sample-dcf-output.md weagents:/opt/agents/ono-assistant/workspace/skills/financial-analysis-core/examples/
```

#### investment-banking
```bash
scp skills/investment-banking/SKILL.md weagents:/opt/agents/ono-assistant/workspace/skills/investment-banking/
scp skills/investment-banking/README.md weagents:/opt/agents/ono-assistant/workspace/skills/investment-banking/
scp skills/investment-banking/scripts/generate-buyer-list.py weagents:/opt/agents/ono-assistant/workspace/skills/investment-banking/scripts/
```

#### equity-research
```bash
scp skills/equity-research/SKILL.md weagents:/opt/agents/ono-assistant/workspace/skills/equity-research/
scp skills/equity-research/README.md weagents:/opt/agents/ono-assistant/workspace/skills/equity-research/
scp skills/equity-research/examples/sample-earnings-update.md weagents:/opt/agents/ono-assistant/workspace/skills/equity-research/examples/
```

#### private-equity
```bash
scp skills/private-equity/SKILL.md weagents:/opt/agents/ono-assistant/workspace/skills/private-equity/
scp skills/private-equity/README.md weagents:/opt/agents/ono-assistant/workspace/skills/private-equity/
scp skills/private-equity/examples/sample-lbo-output.md weagents:/opt/agents/ono-assistant/workspace/skills/private-equity/examples/
```

### Step 4: Transfer Documentation
```bash
scp skills/README.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/TUTORIAL.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/HOW-TO-TALK-TO-AI.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/CONVERSATION-CHEATSHEET.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/SIMPLE-GUIDE.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/START-HERE.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/VISUAL-GUIDE.md weagents:/opt/agents/ono-assistant/workspace/skills/
scp skills/QUICK-REFERENCE.md weagents:/opt/agents/ono-assistant/workspace/skills/
```

### Step 5: Make Scripts Executable
```bash
ssh weagents "chmod +x /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts/*.py"
ssh weagents "chmod +x /opt/agents/ono-assistant/workspace/skills/investment-banking/scripts/*.py"
```

### Step 6: Install Python Dependencies on Remote
```bash
ssh weagents "pip3 install openpyxl pandas numpy"
```

### Step 7: Verify Installation
```bash
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/skills/"
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/"
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts/"
ssh weagents "python3 /opt/agents/ono-assistant/workspace/skills/financial-analysis-core/scripts/generate-comps.py --help"
```

## Verification Checklist

- [ ] All 4 skill directories created
- [ ] All SKILL.md files transferred
- [ ] All Python scripts transferred and executable
- [ ] All example files transferred
- [ ] All documentation files transferred
- [ ] Python dependencies installed on remote
- [ ] Scripts can execute without errors

## Post-Deployment

After deployment, the AI agent on the remote VM will be able to:
1. Read the skill documentation
2. Execute the Python scripts
3. Generate Excel models
4. Provide financial analysis

## Rollback Plan

If needed, remove the skills:
```bash
ssh weagents "rm -rf /opt/agents/ono-assistant/workspace/skills/financial-analysis-core"
ssh weagents "rm -rf /opt/agents/ono-assistant/workspace/skills/investment-banking"
ssh weagents "rm -rf /opt/agents/ono-assistant/workspace/skills/equity-research"
ssh weagents "rm -rf /opt/agents/ono-assistant/workspace/skills/private-equity"
ssh weagents "rm -f /opt/agents/ono-assistant/workspace/skills/*.md"
```
