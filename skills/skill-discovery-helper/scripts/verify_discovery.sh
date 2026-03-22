#!/bin/bash
# Verify skill discovery is properly configured

echo "==================================="
echo "Skill Discovery Verification"
echo "==================================="
echo ""

errors=0
warnings=0

# 1. Check openclaw installation
echo "[1/8] Checking OpenClaw installation..."
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)" || true

if command -v openclaw &> /dev/null; then
    version=$(openclaw --version 2>/dev/null || echo "unknown")
    echo "  ✓ OpenClaw installed: $version"
else
    echo "  ✗ OpenClaw not found in PATH"
    ((errors++))
fi
echo ""

# 2. Check openclaw.json exists
echo "[2/8] Checking configuration file..."
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "  ✓ ~/.openclaw/openclaw.json exists"
else
    echo "  ✗ ~/.openclaw/openclaw.json not found"
    ((errors++))
fi
echo ""

# 3. Check workspace directory
echo "[3/8] Checking workspace directory..."
if [ -d ~/.openclaw/workspace ]; then
    echo "  ✓ ~/.openclaw/workspace/ exists"
else
    echo "  ✗ ~/.openclaw/workspace/ not found"
    ((errors++))
fi
echo ""

# 4. Check workspace/skills directory
echo "[4/8] Checking workspace/skills directory..."
if [ -d ~/.openclaw/workspace/skills ]; then
    skill_count=$(ls -d ~/.openclaw/workspace/skills/*/ 2>/dev/null | wc -l)
    echo "  ✓ ~/.openclaw/workspace/skills/ exists ($skill_count skills)"
else
    echo "  ⚠ ~/.openclaw/workspace/skills/ not found (creating...)"
    mkdir -p ~/.openclaw/workspace/skills
    echo "  ✓ Created ~/.openclaw/workspace/skills/"
    ((warnings++))
fi
echo ""

# 5. Check extraDirs configuration
echo "[5/8] Checking extraDirs configuration..."
if [ -f ~/.openclaw/openclaw.json ]; then
    if grep -q '"extraDirs"' ~/.openclaw/openclaw.json; then
        extraDirs=$(grep -o '"extraDirs":\s*\[[^]]*\]' ~/.openclaw/openclaw.json 2>/dev/null)
        echo "  ✓ extraDirs configured"
        echo "    $extraDirs"
        
        # Check if it points to workspace/skills
        if grep -q 'workspace/skills' ~/.openclaw/openclaw.json; then
            echo "  ✓ extraDirs points to workspace/skills"
        else
            echo "  ⚠ extraDirs may not point to workspace/skills"
            ((warnings++))
        fi
    else
        echo "  ✗ extraDirs NOT configured"
        echo "    Fix: openclaw config set skills.load.extraDirs '[\"/home/"$(whoami)"/.openclaw/workspace/skills\"]'"
        ((errors++))
    fi
else
    echo "  ✗ Cannot check (openclaw.json not found)"
    ((errors++))
fi
echo ""

# 6. Check MEMORY.md
echo "[6/8] Checking MEMORY.md..."
if [ -f ~/.openclaw/workspace/MEMORY.md ]; then
    echo "  ✓ ~/.openclaw/workspace/MEMORY.md exists"
    
    if grep -q "skill discovery" ~/.openclaw/workspace/MEMORY.md 2>/dev/null; then
        echo "  ✓ MEMORY.md contains skill discovery protocol"
    else
        echo "  ⚠ MEMORY.md missing skill discovery protocol"
        ((warnings++))
    fi
else
    echo "  ⚠ ~/.openclaw/workspace/MEMORY.md not found"
    ((warnings++))
fi
echo ""

# 7. Check AGENTS.md
echo "[7/8] Checking AGENTS.md..."
if [ -f ~/.openclaw/workspace/AGENTS.md ]; then
    echo "  ✓ ~/.openclaw/workspace/AGENTS.md exists"
    
    if grep -q "skill" ~/.openclaw/workspace/AGENTS.md 2>/dev/null; then
        echo "  ✓ AGENTS.md references skills"
    else
        echo "  ⚠ AGENTS.md doesn't reference skills"
        ((warnings++))
    fi
    
    if grep -q "MEMORY.md" ~/.openclaw/workspace/AGENTS.md 2>/dev/null; then
        echo "  ✓ AGENTS.md references MEMORY.md"
    else
        echo "  ⚠ AGENTS.md doesn't reference MEMORY.md"
        ((warnings++))
    fi
else
    echo "  ⚠ ~/.openclaw/workspace/AGENTS.md not found"
    ((warnings++))
fi
echo ""

# 8. Test skill discovery
echo "[8/8] Testing skill discovery..."
if command -v openclaw &> /dev/null; then
    skill_count=$(openclaw skills list 2>/dev/null | wc -l)
    if [ "$skill_count" -gt 0 ]; then
        echo "  ✓ openclaw skills list works ($skill_count skills found)"
        
        # Check for workspace skills (both extra and workspace sources)
        extra_count=$(openclaw skills list 2>/dev/null | grep -c "openclaw-extra" || echo "0")
        workspace_count=$(openclaw skills list 2>/dev/null | grep -c "openclaw-workspace" || echo "0")
        if [ "$extra_count" -gt 0 ] || [ "$workspace_count" -gt 0 ]; then
            echo "  ✓ Found $extra_count extra + $workspace_count workspace skills"
        else
            echo "  ⚠ No workspace skills found"
            echo "    (Skills may still be in directory but not discovered)"
            ((warnings++))
        fi
    else
        echo "  ⚠ No skills found via 'openclaw skills list'"
        ((warnings++))
    fi
else
    echo "  ✗ Cannot test (openclaw not available)"
    ((errors++))
fi
echo ""

# Summary
echo "==================================="
echo "Verification Summary"
echo "==================================="
echo "  Errors:   $errors"
echo "  Warnings: $warnings"
echo ""

if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo "✓ All checks passed! Skill discovery is properly configured."
    exit 0
elif [ "$errors" -eq 0 ]; then
    echo "⚠ Some warnings. Skill discovery should work but could be improved."
    exit 0
else
    echo "✗ Errors found. Please fix the issues above."
    echo ""
    echo "Quick fixes:"
    echo "  1. Configure extraDirs:"
    USER=$(whoami)
    echo "     openclaw config set skills.load.extraDirs '[\"/home/$USER/.openclaw/workspace/skills\"]'"
    echo "  2. Restart gateway:"
    echo "     systemctl --user restart openclaw-gateway"
    echo "  3. Create memory files:"
    echo "     touch ~/.openclaw/workspace/MEMORY.md"
    echo "     touch ~/.openclaw/workspace/AGENTS.md"
    exit 1
fi
