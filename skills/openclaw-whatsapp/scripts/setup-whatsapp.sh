#!/bin/bash
# OpenClaw WhatsApp Bridge Setup Script
# This script automates the setup of WhatsApp integration for OpenClaw

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BRIDGE_DIR="${HOME}/.openclaw/whatsapp-bridge"
SERVICE_NAME="openclaw-whatsapp"

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        echo "Please install Node.js 18+ first"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ required, found $(node -v)"
        exit 1
    fi
    print_success "Node.js $(node -v) found"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    print_success "npm $(npm -v) found"
    
    # Check if running on VPS (optional check)
    if [ -f /etc/os-release ]; then
        OS=$(grep ^NAME= /etc/os-release | cut -d'"' -f2)
        print_info "Operating System: $OS"
    fi
}

# Install bridge
install_bridge() {
    print_header "Installing WhatsApp Bridge"
    
    # Create directory
    mkdir -p "$BRIDGE_DIR"
    cd "$BRIDGE_DIR"
    print_success "Created directory: $BRIDGE_DIR"
    
    # Initialize npm project
    npm init -y > /dev/null 2>&1
    print_success "Initialized npm project"
    
    # Install dependencies
    print_info "Installing dependencies (this may take a few minutes)..."
    npm install whatsapp-web.js qrcode-terminal axios > /dev/null 2>&1
    print_success "Installed dependencies"
    
    # Create auth directory
    mkdir -p auth
}

# Create bridge script
create_bridge_script() {
    print_header "Creating Bridge Script"
    
    # Check if script exists in current directory
    if [ -f "whatsapp-bridge.js" ]; then
        cp whatsapp-bridge.js "$BRIDGE_DIR/"
        print_success "Copied whatsapp-bridge.js"
    else
        print_warning "whatsapp-bridge.js not found in current directory"
        print_info "Please copy it manually to: $BRIDGE_DIR/"
    fi
}

# Configure environment
configure_environment() {
    print_header "Configuration"
    
    cd "$BRIDGE_DIR"
    
    # Ask for allowed numbers
    echo ""
    print_info "Enter the phone numbers allowed to use this bot."
    print_info "Format: Country code + number without + or spaces"
    print_info "Examples: 65912345678 (Singapore), 86138xxxxxxxx (China)"
    echo ""
    read -p "Allowed phone numbers (comma-separated, or * for all): " allowed_numbers
    
    # Ask for gateway URL
    echo ""
    read -p "OpenClaw Gateway URL [http://localhost:3000]: " gateway_url
    gateway_url=${gateway_url:-http://localhost:3000}
    
    # Create .env file
    cat > .env << EOF
# OpenClaw Gateway URL
OPENCLAW_GATEWAY_URL=${gateway_url}

# Security: Only allow these phone numbers (with country code)
ALLOWED_NUMBERS=${allowed_numbers}

# Optional: Block specific numbers
BLOCKED_NUMBERS=

# Debug mode (true/false)
DEBUG=false
EOF
    
    chmod 600 .env
    print_success "Created .env configuration"
}

# Install systemd service
install_service() {
    print_header "Installing Systemd Service"
    
    # Create user systemd directory if not exists
    mkdir -p ~/.config/systemd/user
    
    # Create service file
    cat > ~/.config/systemd/user/${SERVICE_NAME}.service << EOF
[Unit]
Description=OpenClaw WhatsApp Bridge
After=network.target openclaw-gateway.service
Wants=openclaw-gateway.service

[Service]
Type=simple
WorkingDirectory=${BRIDGE_DIR}
ExecStart=/usr/bin/node ${BRIDGE_DIR}/whatsapp-bridge.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=default.target
EOF
    
    # Reload systemd
    systemctl --user daemon-reload
    print_success "Created systemd service"
    
    # Enable linger (keep service running after logout)
    if command -v loginctl &> /dev/null; then
        LINGER_STATUS=$(loginctl show-user "$USER" | grep Linger | cut -d= -f2)
        if [ "$LINGER_STATUS" != "yes" ]; then
            print_warning "Systemd linger is not enabled"
            print_info "Run: sudo loginctl enable-linger $USER"
            print_info "This allows services to keep running after SSH logout"
        else
            print_success "Systemd linger is enabled"
        fi
    fi
}

# Test configuration
test_configuration() {
    print_header "Testing Configuration"
    
    cd "$BRIDGE_DIR"
    
    # Check if all files are in place
    if [ -f "whatsapp-bridge.js" ] && [ -f ".env" ] && [ -d "node_modules" ]; then
        print_success "All files are in place"
    else
        print_error "Some files are missing!"
        print_info "Required: whatsapp-bridge.js, .env, node_modules/"
        return 1
    fi
    
    # Test Node.js can run the script (syntax check)
    if node --check whatsapp-bridge.js 2>/dev/null; then
        print_success "Bridge script syntax is valid"
    else
        print_warning "Could not verify bridge script"
    fi
    
    # Check gateway if local
    GATEWAY_URL=$(grep OPENCLAW_GATEWAY_URL .env | cut -d= -f2)
    if [[ "$GATEWAY_URL" == *"localhost"* ]] || [[ "$GATEWAY_URL" == *"127.0.0.1"* ]]; then
        if curl -s "$GATEWAY_URL/health" > /dev/null 2>&1; then
            print_success "OpenClaw gateway is accessible"
        else
            print_warning "OpenClaw gateway may not be running"
            print_info "Start it with: systemctl --user start openclaw-gateway"
        fi
    fi
}

# Start the bridge
start_bridge() {
    print_header "Starting WhatsApp Bridge"
    
    echo ""
    print_info "Starting the WhatsApp bridge for the first time..."
    print_info "You will need to scan a QR code with your WhatsApp app"
    echo ""
    print_warning "Make sure you have your phone ready!"
    echo ""
    read -p "Press Enter to continue..."
    
    cd "$BRIDGE_DIR"
    node whatsapp-bridge.js
}

# Show status
show_status() {
    print_header "Installation Complete!"
    
    echo ""
    echo "WhatsApp Bridge Status:"
    echo "-----------------------"
    echo "Directory: $BRIDGE_DIR"
    
    if systemctl --user is-active --quiet ${SERVICE_NAME} 2>/dev/null; then
        print_success "Service is running"
    else
        print_warning "Service is not running"
    fi
    
    echo ""
    echo "Useful Commands:"
    echo "----------------"
    echo "Start service:   systemctl --user start ${SERVICE_NAME}"
    echo "Stop service:    systemctl --user stop ${SERVICE_NAME}"
    echo "Restart service: systemctl --user restart ${SERVICE_NAME}"
    echo "View logs:       journalctl --user -u ${SERVICE_NAME} -f"
    echo "Edit config:     nano ${BRIDGE_DIR}/.env"
    echo ""
    
    echo "Next Steps:"
    echo "-----------"
    echo "1. Start the service: systemctl --user start ${SERVICE_NAME}"
    echo "2. View logs to see QR code: journalctl --user -u ${SERVICE_NAME} -f"
    echo "3. Scan the QR code with WhatsApp → Settings → Linked Devices"
    echo "4. Send a test message to your WhatsApp number"
    echo ""
}

# Main function
main() {
    print_header "OpenClaw WhatsApp Bridge Setup"
    
    # Check if running in correct directory
    if [ ! -f "whatsapp-bridge.js" ] && [ "$1" != "--skip-script-check" ]; then
        print_warning "whatsapp-bridge.js not found in current directory"
        print_info "Please run this script from the directory containing whatsapp-bridge.js"
        print_info "Or run with --skip-script-check to skip this validation"
        exit 1
    fi
    
    # Run setup steps
    check_prerequisites
    install_bridge
    create_bridge_script
    configure_environment
    install_service
    test_configuration
    
    # Ask if user wants to start now
    echo ""
    read -p "Do you want to start the bridge now? (y/N): " start_now
    if [[ $start_now =~ ^[Yy]$ ]]; then
        start_bridge
    else
        show_status
    fi
}

# Run main function
main "$@"
