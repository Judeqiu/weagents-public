#!/bin/bash
# OpenClaw Doctor - Batch Health Check for Multiple Hosts
# Usage: ./doctor-all.sh [host1 host2 ...]
# If no hosts specified, reads from ~/.ssh/config

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCTOR_SCRIPT="$SCRIPT_DIR/doctor.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get hosts from arguments or SSH config
if [ $# -gt 0 ]; then
    HOSTS="$@"
else
    # Extract Host entries from SSH config, exclude wildcards
    if [ -f ~/.ssh/config ]; then
        HOSTS=$(grep -E "^Host " ~/.ssh/config | grep -v "[*?]" | awk '{print $2}')
    fi
fi

if [ -z "$HOSTS" ]; then
    echo -e "${RED}Error: No hosts specified and no Host entries found in ~/.ssh/config${NC}"
    echo ""
    echo "Usage:"
    echo "  $0                    # Use all hosts from ~/.ssh/config"
    echo "  $0 host1 host2        # Check specific hosts"
    exit 1
fi

HOST_COUNT=$(echo "$HOSTS" | wc -w)

echo ""
echo "🔍 OpenClaw Doctor - Batch Check"
echo "================================"
echo ""
echo -e "Hosts to check (${BLUE}$HOST_COUNT${NC}): ${YELLOW}$HOSTS${NC}"
echo ""

# Track results
declare -A RESULTS
TOTAL_ISSUES=0
TOTAL_WARNINGS=0

for HOST in $HOSTS; do
    echo "========================================"
    echo -e "Checking: ${BLUE}$HOST${NC}"
    echo "========================================"
    
    # Run doctor and capture output
    OUTPUT=$("$DOCTOR_SCRIPT" "$HOST" auto 2>&1) && STATUS=0 || STATUS=1
    
    # Display output
    echo "$OUTPUT"
    
    # Parse results
    if echo "$OUTPUT" | grep -q "Healthy - No issues"; then
        RESULTS[$HOST]="healthy"
    elif echo "$OUTPUT" | grep -q "issue(s)"; then
        ISSUES=$(echo "$OUTPUT" | grep -oE "[0-9]+ issue" | grep -oE "[0-9]+" || echo "0")
        WARNINGS=$(echo "$OUTPUT" | grep -oE "[0-9]+ warning" | grep -oE "[0-9]+" || echo "0")
        RESULTS[$HOST]="issues:${ISSUES}:${WARNINGS}"
        TOTAL_ISSUES=$((TOTAL_ISSUES + ISSUES))
        TOTAL_WARNINGS=$((TOTAL_WARNINGS + WARNINGS))
    elif [ $STATUS -ne 0 ]; then
        RESULTS[$HOST]="failed"
    else
        RESULTS[$HOST]="unknown"
    fi
    
    echo ""
done

echo "========================================"
echo "           SUMMARY REPORT"
echo "========================================"
echo ""

HEALTHY_COUNT=0
ISSUE_COUNT=0
FAILED_COUNT=0

for HOST in $HOSTS; do
    RESULT="${RESULTS[$HOST]}"
    case "$RESULT" in
        healthy)
            echo -e "${GREEN}✅${NC} $HOST - Healthy"
            HEALTHY_COUNT=$((HEALTHY_COUNT+1))
            ;;
        issues:*)
            IFS=':' read -r _ I W <<< "$RESULT"
            echo -e "${YELLOW}⚠️${NC} $HOST - $I issue(s), $W warning(s)"
            ISSUE_COUNT=$((ISSUE_COUNT+1))
            ;;
        failed)
            echo -e "${RED}❌${NC} $HOST - Connection/Check failed"
            FAILED_COUNT=$((FAILED_COUNT+1))
            ;;
        *)
            echo -e "${YELLOW}?${NC} $HOST - Unknown status"
            ;;
    esac
done

echo ""
echo "----------------------------------------"
echo -e "Total:      ${BLUE}$HOST_COUNT${NC} hosts checked"
echo -e "Healthy:    ${GREEN}$HEALTHY_COUNT${NC}"
echo -e "Issues:     ${YELLOW}$ISSUE_COUNT${NC}"
echo -e "Failed:     ${RED}$FAILED_COUNT${NC}"
[ $TOTAL_ISSUES -gt 0 ] && echo -e "Total issues:    ${RED}$TOTAL_ISSUES${NC}"
[ $TOTAL_WARNINGS -gt 0 ] && echo -e "Total warnings:  ${YELLOW}$TOTAL_WARNINGS${NC}"
echo "========================================"
echo ""

# Exit with error if any issues found
if [ $ISSUE_COUNT -gt 0 ] || [ $FAILED_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Some hosts require attention${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All hosts healthy${NC}"
    exit 0
fi
