#!/bin/bash
# List all WeAgents agents on a remote host
# Usage: ./remote-list-agents.sh <user@host> [remote-base-path]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REMOTE_HOST="$1"
REMOTE_BASE="${2:-/opt/weagents/agents}"

if [ -z "$REMOTE_HOST" ]; then
    echo -e "${RED}Usage: $0 <user@host> [remote-base-path]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 ubuntu@192.168.1.100"
    echo "  $0 ubuntu@vm.example.com /home/ubuntu/weagents/agents"
    exit 1
fi

echo -e "${BLUE}=== Remote Agents on $REMOTE_HOST ===${NC}"
echo ""

# Check connection and list agents
ssh -o ConnectTimeout=5 "$REMOTE_HOST" "
    if [ ! -d '$REMOTE_BASE' ]; then
        echo 'DIRECTORY_NOT_FOUND'
        exit 1
    fi
    
    echo 'AGENT|STATUS|AGENT_ID|PURPOSE'
    for agent_dir in $REMOTE_BASE/*/; do
        if [ -d '\$agent_dir' ]; then
            name=\$(basename '\$agent_dir')
            
            # Check if agent is properly set up
            if [ -f '\$agent_dir/workspace/SOUL.md' ] && [ -f '\$agent_dir/workspace/IDENTITY.md' ]; then
                status='✓ Active'
            else
                status='✗ Incomplete'
            fi
            
            # Get agent ID from .env
            agent_id='N/A'
            if [ -f '\$agent_dir/.env' ]; then
                agent_id=\$(grep 'OPENCLAW_AGENT_ID=' '\$agent_dir/.env' | cut -d'=' -f2 | head -1)
            fi
            
            # Get purpose from IDENTITY.md
            purpose='N/A'
            if [ -f '\$agent_dir/workspace/IDENTITY.md' ]; then
                purpose=\$(grep 'Full Identifier:' '\$agent_dir/workspace/IDENTITY.md' | sed 's/.*for //' | head -1)
                if [ -z '\$purpose' ]; then
                    purpose='General assistant'
                fi
            fi
            
            echo '\$name|\$status|\$agent_id|\$purpose'
        fi
    done
" 2>/dev/null | while IFS='|' read -r name status agent_id purpose; do
    if [ "$name" = "DIRECTORY_NOT_FOUND" ]; then
        echo -e "${YELLOW}No agents directory found at $REMOTE_BASE${NC}"
        echo "Run: ssh $REMOTE_HOST 'mkdir -p $REMOTE_BASE'"
        exit 1
    elif [ "$name" = "AGENT" ]; then
        # Header row
        printf "%-20s %-12s %-15s %s\n" "Agent Name" "Status" "Agent ID" "Purpose"
        printf "%s\n" "--------------------------------------------------------------------------------"
    else
        printf "%-20s %-12s %-15s %s\n" "$name" "$status" "$agent_id" "$purpose"
    fi
done

echo ""
echo -e "${GREEN}Use ./remote-create-agent.sh to add more agents${NC}"
