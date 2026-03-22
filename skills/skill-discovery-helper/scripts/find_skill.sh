#!/bin/bash
# Find a specific skill across all sources

SKILL_NAME="$1"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <skill-name>"
    echo ""
    echo "Examples:"
    echo "  $0 mychrome"
    echo "  $0 customer-research-agent"
    exit 1
fi

echo "==================================="
echo "Searching for skill: $SKILL_NAME"
echo "==================================="
echo ""

# Setup PATH for openclaw
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)" || true

found=false

# 1. Check openclaw skills list
echo "1. Checking 'openclaw skills list'..."
if command -v openclaw &> /dev/null; then
    result=$(openclaw skills list 2>/dev/null | grep -i "$SKILL_NAME" || true)
    if [ -n "$result" ]; then
        echo "   ✓ Found:"
        echo "$result" | while read line; do
            echo "     $line"
        done
        found=true
    else
        echo "   ✗ Not found in openclaw skills list"
    fi
else
    echo "   ⚠ openclaw command not available"
fi
echo ""

# 2. Check workspace directory
echo "2. Checking ~/.openclaw/workspace/skills/..."
if [ -d ~/.openclaw/workspace/skills ]; then
    # Check exact match
    if [ -d ~/.openclaw/workspace/skills/$SKILL_NAME ]; then
        echo "   ✓ Found directory: ~/.openclaw/workspace/skills/$SKILL_NAME"
        if [ -f ~/.openclaw/workspace/skills/$SKILL_NAME/SKILL.md ]; then
            echo "   ✓ Has SKILL.md"
            # Extract description
            desc=$(grep "^description:" ~/.openclaw/workspace/skills/$SKILL_NAME/SKILL.md 2>/dev/null | head -1)
            if [ -n "$desc" ]; then
                echo "   $desc"
            fi
        else
            echo "   ⚠ Missing SKILL.md"
        fi
        found=true
    else
        # Check partial match
        matches=$(ls ~/.openclaw/workspace/skills/ 2>/dev/null | grep -i "$SKILL_NAME" || true)
        if [ -n "$matches" ]; then
            echo "   ✓ Partial matches found:"
            echo "$matches" | while read match; do
                echo "     - $match"
            done
            found=true
        else
            echo "   ✗ Not found in workspace/skills/"
        fi
    fi
else
    echo "   ⚠ ~/.openclaw/workspace/skills/ directory not found"
fi
echo ""

# 3. Check for SKILL.md files
echo "3. Searching for SKILL.md files..."
if command -v find &> /dev/null; then
    results=$(find ~/.openclaw -name "SKILL.md" 2>/dev/null | head -20)
    if [ -n "$results" ]; then
        echo "   Found SKILL.md files:"
        echo "$results" | while read file; do
            dir=$(dirname "$file")
            skill=$(basename "$dir")
            if echo "$skill" | grep -qi "$SKILL_NAME"; then
                echo "     ✓ $skill"
                echo "       Location: $file"
                found=true
            fi
        done
        if [ "$found" = false ]; then
            echo "   (no matches for '$SKILL_NAME')"
        fi
    else
        echo "   No SKILL.md files found"
    fi
else
    echo "   ⚠ find command not available"
fi
echo ""

# 4. Check extraDirs configuration
echo "4. Checking extraDirs configuration..."
if [ -f ~/.openclaw/openclaw.json ]; then
    extraDirs=$(grep -o '"extraDirs":\s*\[[^]]*\]' ~/.openclaw/openclaw.json 2>/dev/null || echo "")
    if [ -n "$extraDirs" ]; then
        echo "   ✓ extraDirs configured: $extraDirs"
    else
        echo "   ⚠ extraDirs NOT configured"
        echo "      Run: openclaw config set skills.load.extraDirs '[\"/home/\"$(whoami)\"/.openclaw/workspace/skills\"]"'
    fi
else
    echo "   ⚠ ~/.openclaw/openclaw.json not found"
fi
echo ""

# Summary
echo "==================================="
if [ "$found" = true ]; then
    echo "✓ Skill '$SKILL_NAME' FOUND"
else
    echo "✗ Skill '$SKILL_NAME' NOT FOUND"
    echo ""
    echo "Suggestions:"
    echo "  1. Deploy the skill: skill-deployer deploy $SKILL_NAME --host kai"
    echo "  2. Clone from git: cd ~/.openclaw/workspace/skills/ && git clone <repo>"
    echo "  3. Check skill name spelling"
fi
echo "==================================="
