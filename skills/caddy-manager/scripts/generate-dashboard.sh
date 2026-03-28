#!/bin/bash
# generate-dashboard.sh - Create OpenClaw agent homepage
# Usage: ./generate-dashboard.sh [output-directory]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 OpenClaw Dashboard Generator${NC}"
echo "================================"

# Detect environment and set paths
if [[ -f /etc/caddy/Caddyfile ]]; then
    WEB_ROOT="${1:-/var/www/welcome}"
    SITES_DIR="/var/www/sites"
    CADDY_ENV="production"
    echo -e "${GREEN}✓${NC} Detected: Production environment (Caddy system install)"
else
    WEB_ROOT="${1:-./sites/dashboard}"
    SITES_DIR="./sites"
    CADDY_ENV="local"
    echo -e "${GREEN}✓${NC} Detected: Local development environment"
fi

# Create directories
mkdir -p "$WEB_ROOT"
echo -e "${GREEN}✓${NC} Output directory: $WEB_ROOT"

# Detect OpenClaw paths
echo -e "${BLUE}🔍${NC} Detecting OpenClaw installation..."
OPENCLAW_DIR=""
OPENCLAW_CONFIG_PATHS=(
    "$HOME/.openclaw"
    "/opt/weagents/.openclaw"
    "/opt/openclaw"
)

for path in "${OPENCLAW_CONFIG_PATHS[@]}"; do
    if [[ -d "$path" ]]; then
        OPENCLAW_DIR="$path"
        echo -e "${GREEN}✓${NC} Found OpenClaw at: $OPENCLAW_DIR"
        break
    fi
done

if [[ -z "$OPENCLAW_DIR" ]]; then
    echo -e "${YELLOW}⚠${NC} OpenClaw directory not found, using defaults"
fi

# Extract agent info
echo -e "${BLUE}📋${NC} Extracting agent information..."

AGENT_NAME="main"
AGENT_MODEL="Unknown"
OPENCLAW_VERSION="Unknown"
AGENT_STATUS="Active"

# Try to get version
if command -v openclaw &>/dev/null; then
    OPENCLAW_VERSION=$(openclaw --version 2>/dev/null | head -1 | awk '{print $NF}' || echo "Unknown")
fi

# Read from config if available
if [[ -n "$OPENCLAW_DIR" && -f "$OPENCLAW_DIR/openclaw.json" ]]; then
    if command -v jq &>/dev/null; then
        AGENT_NAME=$(jq -r '.agents.default // "main"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null || echo "main")
        AGENT_MODEL=$(jq -r '.agents.defaults.model.primary // "Unknown"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null || echo "Unknown")
    else
        # Fallback: grep for model in config
        AGENT_MODEL=$(grep -o '"primary": *"[^"]*"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null | head -1 | cut -d'"' -f4 || echo "Unknown")
    fi
fi

echo -e "${GREEN}✓${NC} Agent: $AGENT_NAME"
echo -e "${GREEN}✓${NC} Model: $AGENT_MODEL"
echo -e "${GREEN}✓${NC} Version: $OPENCLAW_VERSION"

# Get skills list
echo -e "${BLUE}🧩${NC} Scanning installed skills..."

SKILLS_DIR=""
SKILLS_SEARCH_PATHS=(
    "$HOME/.openclaw/workspace/skills"
    "$HOME/.openclaw/agents/main/skills"
    "/opt/weagents/.openclaw/workspace/skills"
    "./skills"
)

for path in "${SKILLS_SEARCH_PATHS[@]}"; do
    if [[ -d "$path" ]]; then
        SKILLS_DIR="$path"
        echo -e "${GREEN}✓${NC} Found skills directory: $SKILLS_DIR"
        break
    fi
done

SKILLS_COUNT=0
SKILLS_HTML=""

if [[ -n "$SKILLS_DIR" ]]; then
    # Count skills
    SKILLS_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" -type f 2>/dev/null | wc -l)
    echo -e "${GREEN}✓${NC} Found $SKILLS_COUNT skills"
    
    # Generate skills HTML
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [[ -d "$skill_dir" ]]; then
            skill_name=$(basename "$skill_dir")
            skill_md="$skill_dir/SKILL.md"
            
            if [[ -f "$skill_md" ]]; then
                # Extract description from SKILL.md
                skill_desc=$(grep -m1 "^description:" "$skill_md" 2>/dev/null | sed 's/description: //' | tr -d '"' | cut -c1-100 || echo "")
                
                # If no description in frontmatter, try first paragraph
                if [[ -z "$skill_desc" ]]; then
                    skill_desc=$(grep -v "^#" "$skill_md" 2>/dev/null | grep -v "^$" | head -1 | cut -c1-100 || echo "")
                fi
                
                # Fallback description
                if [[ -z "$skill_desc" ]]; then
                    skill_desc="OpenClaw skill for $skill_name"
                fi
                
                # Truncate if too long
                if [[ ${#skill_desc} -gt 90 ]]; then
                    skill_desc="${skill_desc:0:90}..."
                fi
                
                # Assign emoji based on skill name
                skill_emoji="📋"
                case "$skill_name" in
                    *browser*|*web*|*fetch*|*http*) skill_emoji="🌐" ;;
                    *caddy*|*server*|*nginx*|*apache*) skill_emoji="🚀" ;;
                    *skill*|*pull*|*deploy*|*install*) skill_emoji="🧩" ;;
                    *search*|*find*|*lookup*) skill_emoji="🔍" ;;
                    *download*|*file*|*save*) skill_emoji="📥" ;;
                    *chat*|*message*|*telegram*|*whatsapp*) skill_emoji="💬" ;;
                    *email*|*mail*|*smtp*) skill_emoji="📧" ;;
                    *security*|*guard*|*auth*|*protect*) skill_emoji="🔒" ;;
                    *config*|*setup*|*init*) skill_emoji="⚙️" ;;
                    *research*|*analysis*|*report*) skill_emoji="📊" ;;
                    *finance*|*money*|*bank*|*trade*) skill_emoji="💰" ;;
                    *shop*|*buy*|*sell*|*ecommerce*) skill_emoji="🛒" ;;
                    *pdf*|*doc*|*document*) skill_emoji="📄" ;;
                    *image*|*photo*|*picture*) skill_emoji="🖼️" ;;
                    *video*|*movie*) skill_emoji="🎬" ;;
                    *music*|*audio*|*sound*) skill_emoji="🎵" ;;
                    *code*|*dev*|*program*) skill_emoji="💻" ;;
                    *git*|*github*) skill_emoji="🐙" ;;
                    *docker*|*container*) skill_emoji="🐳" ;;
                    *cloud*|*aws*|*azure*) skill_emoji="☁️" ;;
                    *database*|*db*|*sql*) skill_emoji="🗄️" ;;
                    *ssh*|*remote*|*vps*) skill_emoji="🔌" ;;
                    *cron*|*schedule*|*timer*) skill_emoji="⏰" ;;
                    *log*|*monitor*|*status*) skill_emoji="📈" ;;
                    *test*|*check*|*verify*) skill_emoji="✅" ;;
                    *fix*|*repair*|*heal*) skill_emoji="🔧" ;;
                    *clean*|*cleanup*|*purge*) skill_emoji="🧹" ;;
                esac
                
                SKILLS_HTML="${SKILLS_HTML}
                <div class=\"skill-item\">
                    <div class=\"skill-icon\">$skill_emoji</div>
                    <div class=\"skill-info\">
                        <div class=\"skill-name\">$skill_name</div>
                        <div class=\"skill-desc\">$skill_desc</div>
                    </div>
                </div>"
            fi
        fi
    done
else
    echo -e "${YELLOW}⚠${NC} Skills directory not found"
fi

if [[ -z "$SKILLS_HTML" ]]; then
    SKILLS_HTML='<div class="skill-item"><div class="skill-icon">⚠️</div><div class="skill-info"><div class="skill-name">No Skills Found</div><div class="skill-desc">No skills detected in the workspace directory. Install skills to see them here.</div></div></div>'
fi

# Get system info
HOSTNAME=$(hostname)
PLATFORM=$(uname -s)
UPTIME=$(uptime -p 2>/dev/null || uptime | awk -F',' '{print $1}' | sed 's/^.*up //')
GENERATED_DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "${GREEN}✓${NC} System: $HOSTNAME ($PLATFORM)"
echo -e "${GREEN}✓${NC} Uptime: $UPTIME"

# Generate HTML
echo -e "${BLUE}🎨${NC} Generating HTML dashboard..."

cat > "$WEB_ROOT/index.html" << HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Agent Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            font-weight: 700;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
        }
        
        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #333;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        
        .info-item {
            padding: 16px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.2s ease;
        }
        
        .info-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .info-label {
            font-size: 0.75rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        
        .info-value {
            font-size: 1.05rem;
            font-weight: 600;
            color: #212529;
            word-break: break-word;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        
        .status-active::before {
            content: "";
            width: 8px;
            height: 8px;
            background: #28a745;
            border-radius: 50%;
            display: inline-block;
        }
        
        .skills-list {
            display: grid;
            gap: 12px;
        }
        
        .skill-item {
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 16px;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 12px;
            border: 1px solid #e9ecef;
            transition: all 0.2s ease;
        }
        
        .skill-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-color: #667eea;
        }
        
        .skill-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .skill-info {
            flex: 1;
            min-width: 0;
        }
        
        .skill-name {
            font-weight: 600;
            font-size: 1.05rem;
            margin-bottom: 4px;
            color: #212529;
        }
        
        .skill-desc {
            font-size: 0.9rem;
            color: #6c757d;
            line-height: 1.4;
        }
        
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
            font-size: 0.9rem;
        }
        
        .actions {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 30px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
            backdrop-filter: blur(10px);
            cursor: pointer;
            font-size: 0.95rem;
        }
        
        .btn:hover {
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-2px);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .btn-primary:hover {
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        }
        
        .count-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 24px;
            height: 24px;
            padding: 0 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-left: 8px;
        }
        
        @media (max-width: 600px) {
            .header h1 { font-size: 1.8rem; }
            .card { padding: 20px; }
            .info-grid { grid-template-columns: 1fr; }
            .skill-icon { width: 40px; height: 40px; font-size: 1.2rem; }
        }
        
        @media (prefers-color-scheme: dark) {
            .card {
                background: #1a1a2e;
                color: #eee;
            }
            .info-item {
                background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
            }
            .info-label { color: #a0a0a0; }
            .info-value { color: #fff; }
            .skill-item {
                background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
                border-color: #0f3460;
            }
            .skill-name { color: #fff; }
            .skill-desc { color: #a0a0a0; }
            .card-title { color: #fff; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 OpenClaw Agent</h1>
            <p>Dashboard and System Overview</p>
        </div>

        <div class="card">
            <div class="card-title">📊 Agent Information</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Agent Name</div>
                    <div class="info-value">${AGENT_NAME}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Model</div>
                    <div class="info-value">${AGENT_MODEL}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Version</div>
                    <div class="info-value">${OPENCLAW_VERSION}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Status</div>
                    <div class="info-value">
                        <span class="status-badge status-active">Active</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🖥️ System Information</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Hostname</div>
                    <div class="info-value">${HOSTNAME}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Platform</div>
                    <div class="info-value">${PLATFORM}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Uptime</div>
                    <div class="info-value">${UPTIME}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Skills Installed</div>
                    <div class="info-value">${SKILLS_COUNT}</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                📦 Installed Skills
                <span class="count-badge">${SKILLS_COUNT}</span>
            </div>
            <div class="skills-list">
                ${SKILLS_HTML}
            </div>
        </div>

        <div class="actions">
            <a href="javascript:location.reload()" class="btn">🔄 Refresh Dashboard</a>
            <a href="/" class="btn btn-primary">🏠 Home</a>
        </div>

        <div class="footer">
            <p>Generated on ${GENERATED_DATE} | OpenClaw Agent Dashboard</p>
            <p style="margin-top: 8px; opacity: 0.7;">Powered by Caddy Web Server</p>
        </div>
    </div>
</body>
</html>
HTMLEOF

echo -e "${GREEN}✓${NC} Dashboard saved to: $WEB_ROOT/index.html"

# Set permissions for production
if [[ "$CADDY_ENV" == "production" ]]; then
    echo -e "${BLUE}🔒${NC} Setting permissions..."
    sudo chown -R caddy:caddy "$WEB_ROOT" 2>/dev/null || true
    sudo chmod -R 755 "$WEB_ROOT" 2>/dev/null || true
    
    # Reload Caddy if running
    if systemctl is-active caddy &>/dev/null; then
        echo -e "${BLUE}🔄${NC} Reloading Caddy..."
        sudo systemctl reload caddy
        echo -e "${GREEN}✓${NC} Caddy reloaded"
    fi
    
    # Detect IP for access URL
    IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
    echo ""
    echo -e "${GREEN}🎉 Dashboard is live!${NC}"
    echo -e "   Local: ${BLUE}http://localhost${NC}"
    echo -e "   LAN:   ${BLUE}http://$IP${NC}"
else
    echo ""
    echo -e "${GREEN}🎉 Dashboard generated!${NC}"
    echo -e "   File: ${BLUE}$WEB_ROOT/index.html${NC}"
    echo ""
    echo -e "${YELLOW}💡${NC} To view it:"
    echo -e "   1. Run: ${BLUE}caddy file-server --root $WEB_ROOT --browse${NC}"
    echo -e "   2. Open: ${BLUE}http://localhost:8080${NC}"
fi

echo ""
echo -e "${GREEN}✅ Done!${NC}"
