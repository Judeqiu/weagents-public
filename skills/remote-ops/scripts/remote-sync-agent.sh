#!/bin/bash
# Sync a local agent to a remote host
# Usage: ./remote-sync-agent.sh <user@host> <agent-name> [options]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REMOTE_HOST="$1"
AGENT_NAME="$2"
DRY_RUN=false
EXCLUDE_DATA=true

# Parse options
shift 2
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --include-data)
            EXCLUDE_DATA=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 <user@host> <agent-name> [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run        Show what would be synced without doing it"
            echo "  --include-data   Also sync data/ directory (default: excluded)"
            echo "  -h, --help       Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

if [ -z "$REMOTE_HOST" ] || [ -z "$AGENT_NAME" ]; then
    echo -e "${RED}Usage: $0 <user@host> <agent-name> [options]${NC}"
    exit 1
fi

LOCAL_AGENT="./agents/$AGENT_NAME"
REMOTE_BASE="/opt/weagents/agents/$AGENT_NAME"

if [ ! -d "$LOCAL_AGENT" ]; then
    echo -e "${RED}Error: Local agent '$AGENT_NAME' not found at $LOCAL_AGENT${NC}"
    exit 1
fi

echo -e "${BLUE}=== Syncing Agent to Remote ===${NC}"
echo "Local: $LOCAL_AGENT"
echo "Remote: $REMOTE_HOST:$REMOTE_BASE"
echo "Dry run: $DRY_RUN"
echo ""

# Build rsync options
RSYNC_OPTS="-avz"
if [ "$DRY_RUN" = true ]; then
    RSYNC_OPTS="$RSYNC_OPTS --dry-run"
fi

# Build exclude patterns
EXCLUDES=""
if [ "$EXCLUDE_DATA" = true ]; then
    EXCLUDES="--exclude=data/ --exclude=.config/"
fi

echo -e "${YELLOW}Syncing files...${NC}"
if rsync $RSYNC_OPTS $EXCLUDES "$LOCAL_AGENT/" "$REMOTE_HOST:$REMOTE_BASE/"; then
    echo ""
    echo -e "${GREEN}✓ Sync completed${NC}"
else
    echo ""
    echo -e "${RED}✗ Sync failed${NC}"
    exit 1
fi

# Set permissions on remote
echo -e "${YELLOW}Setting remote permissions...${NC}"
ssh "$REMOTE_HOST" "chmod 700 $REMOTE_BASE/.config 2>/dev/null || true"
echo -e "${GREEN}✓ Permissions set${NC}"

echo ""
echo -e "${GREEN}Done!${NC}"
