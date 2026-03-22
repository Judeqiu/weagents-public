#!/bin/bash
# List all OpenClaw skills organized by source

echo "==================================="
echo "OpenClaw Skill Inventory"
echo "==================================="
echo ""

# Check if openclaw is available
if ! command -v openclaw &> /dev/null; then
    echo "Warning: openclaw command not found in PATH"
    echo "Trying with fnm..."
    export PATH="$HOME/.local/share/fnm:$PATH"
    eval "$(fnm env --shell bash 2>/dev/null)" || true
fi

# List skills from openclaw
echo "Skills from 'openclaw skills list':"
echo "-----------------------------------"
if command -v openclaw &> /dev/null; then
    openclaw skills list 2>/dev/null | while read line; do
        echo "  $line"
    done
else
    echo "  (openclaw not available)"
fi
echo ""

# List workspace skills
echo "Skills in ~/.openclaw/workspace/skills/:"
echo "----------------------------------------"
if [ -d ~/.openclaw/workspace/skills ]; then
    for skill in ~/.openclaw/workspace/skills/*/; do
        if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            if [ -f "$skill/SKILL.md" ]; then
                echo "  ✓ $skill_name (has SKILL.md)"
            else
                echo "  ⚠ $skill_name (no SKILL.md)"
            fi
        fi
    done
else
    echo "  (workspace/skills directory not found)"
fi
echo ""

# Check extraDirs configuration
echo "extraDirs Configuration:"
echo "------------------------"
if [ -f ~/.openclaw/openclaw.json ]; then
    extraDirs=$(grep -o '"extraDirs":\s*\[[^]]*\]' ~/.openclaw/openclaw.json 2>/dev/null || echo "not configured")
    echo "  $extraDirs"
else
    echo "  (openclaw.json not found)"
fi
echo ""

# Summary
echo "==================================="
echo "Summary"
echo "==================================="

bundled_count=0
extra_count=0
workspace_count=0

if command -v openclaw &> /dev/null; then
    bundled_count=$(openclaw skills list 2>/dev/null | grep -c "openclaw-bundled" || echo "0")
    extra_count=$(openclaw skills list 2>/dev/null | grep -c "openclaw-extra" || echo "0")
    workspace_count=$(openclaw skills list 2>/dev/null | grep -c "openclaw-workspace" || echo "0")
fi

echo "  Bundled skills:     $bundled_count"
echo "  Extra skills:       $extra_count"
echo "  Workspace skills:   $workspace_count"
echo ""

workspace_dir_count=$(ls -d ~/.openclaw/workspace/skills/*/ 2>/dev/null | wc -l)
echo "  Skills in ~/.openclaw/workspace/skills/: $workspace_dir_count"
echo ""

echo "Remember: <available_skills> context is INCOMPLETE!"
echo "Always run 'openclaw skills list' to see ALL skills."
