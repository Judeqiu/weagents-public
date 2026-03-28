#!/bin/bash
#
# SSH Config Add - APPEND ONLY
# Safely adds new SSH host entries without modifying existing ones
#
# SAFETY GUARANTEES:
# - Will NOT modify existing hosts
# - Will NOT delete hosts  
# - Will NOT replace hosts
# - Only APPENDS new entries
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# SSH Config file
SSH_CONFIG="${HOME}/.ssh/config"

# Default values
DEFAULT_USER="ubuntu"
DEFAULT_HOSTNAME=""

# Function to print colored output
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Function to show help
show_help() {
    cat << EOF
SSH Config Add - Append Only
==============================

SAFETY: This tool only APPENDS new entries. It will NEVER modify,
delete, or replace existing SSH config entries.

USAGE:
    ./add-host.sh [options]

OPTIONS:
    --name, -n      Host name (required, e.g., 'kai', 'enraie')
    --ip, -i        IP address or hostname (required)
    --user, -u      SSH user (default: ubuntu)
    --key, -k       SSH key file path (optional)
    --help, -h      Show this help

INTERACTIVE MODE:
    Run without arguments for interactive prompts:
    ./add-host.sh

EXAMPLES:
    # Interactive mode
    ./add-host.sh

    # Add simple host
    ./add-host.sh --name kai --ip 15.204.118.66

    # Add with custom user
    ./add-host.sh --name enraie --ip 148.113.174.79 --user admin

    # Add with specific SSH key
    ./add-host.sh --name myserver --ip 192.168.1.100 --key ~/.ssh/my_key

SAFETY:
    - Creates backup before any changes
    - Refuses to modify existing hosts
    - Sets proper file permissions (600)

EOF
}

# Function to check if SSH config directory exists
ensure_ssh_dir() {
    if [ ! -d "${HOME}/.ssh" ]; then
        print_info "Creating ~/.ssh directory..."
        mkdir -p "${HOME}/.ssh"
        chmod 700 "${HOME}/.ssh"
    fi
}

# Function to check if host exists in SSH config
host_exists() {
    local host_name="$1"
    
    if [ ! -f "$SSH_CONFIG" ]; then
        return 1  # File doesn't exist, so host doesn't exist
    fi
    
    # Check if Host entry exists (exact match)
    if grep -qE "^Host ${host_name}$" "$SSH_CONFIG" 2>/dev/null; then
        return 0  # Host exists
    fi
    
    return 1  # Host doesn't exist
}

# Function to get existing host details
get_existing_host() {
    local host_name="$1"
    
    if [ ! -f "$SSH_CONFIG" ]; then
        echo ""
        return
    fi
    
    # Extract the host entry
    awk "/^Host ${host_name}\$/{found=1} found{print; if(/^\$/ || /^Host / && !/^Host ${host_name}\$/){exit}}" "$SSH_CONFIG" 2>/dev/null || true
}

# Function to create backup
create_backup() {
    if [ -f "$SSH_CONFIG" ]; then
        local backup_file="${SSH_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$SSH_CONFIG" "$backup_file"
        chmod 600 "$backup_file"
        echo "$backup_file"
    else
        echo ""
    fi
}

# Function to validate inputs
validate_inputs() {
    local name="$1"
    local ip="$2"
    local user="$3"
    
    # Validate host name
    if [ -z "$name" ]; then
        print_error "Host name is required"
        return 1
    fi
    
    # Check for invalid characters in host name
    if [[ ! "$name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        print_error "Host name must contain only letters, numbers, hyphens, and underscores"
        return 1
    fi
    
    # Validate IP/hostname
    if [ -z "$ip" ]; then
        print_error "IP address or hostname is required"
        return 1
    fi
    
    # Basic validation - not empty and no spaces
    if [[ "$ip" =~ [[:space:]] ]]; then
        print_error "IP/hostname cannot contain spaces"
        return 1
    fi
    
    return 0
}

# Function to add host to SSH config
add_host() {
    local name="$1"
    local ip="$2"
    local user="$3"
    local key="$4"
    
    # Ensure SSH directory exists
    ensure_ssh_dir
    
    # Create backup if file exists
    local backup_file
    backup_file=$(create_backup)
    
    # Append new host entry
    {
        echo ""
        echo "Host ${name}"
        echo "    HostName ${ip}"
        echo "    User ${user}"
        if [ -n "$key" ]; then
            echo "    IdentityFile ${key}"
        fi
        echo "    StrictHostKeyChecking accept-new"
    } >> "$SSH_CONFIG"
    
    # Set proper permissions
    chmod 600 "$SSH_CONFIG"
    
    # Print success
    print_success "Successfully added '${name}' to ${SSH_CONFIG}"
    echo ""
    echo "NEW ENTRY:"
    echo "----------"
    get_existing_host "$name"
    echo "----------"
    
    if [ -n "$backup_file" ]; then
        echo ""
        print_info "Backup created: ${backup_file}"
    fi
    
    echo ""
    echo "Test the connection:"
    echo "  ssh ${name} \"hostname && whoami\""
}

# Function to run in interactive mode
interactive_mode() {
    echo ""
    echo "=========================================="
    echo "  SSH Config Add - Interactive Mode"
    echo "=========================================="
    echo ""
    print_info "This tool APPENDS new SSH hosts only."
    print_info "It will NEVER modify existing entries."
    echo ""
    
    # Get host name
    while true; do
        read -rp "Enter host name (e.g., kai, enraie): " name
        if [ -n "$name" ]; then
            if [[ "$name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
                break
            else
                print_error "Host name must contain only letters, numbers, hyphens, and underscores"
            fi
        else
            print_error "Host name is required"
        fi
    done
    
    # Check if host already exists
    if host_exists "$name"; then
        echo ""
        print_error "Host '${name}' already exists in ${SSH_CONFIG}!"
        echo ""
        echo "EXISTING ENTRY:"
        echo "---------------"
        get_existing_host "$name"
        echo "---------------"
        echo ""
        print_warning "NO CHANGES MADE."
        echo "This tool is APPEND-ONLY and cannot modify existing entries."
        echo "To modify, please edit ${SSH_CONFIG} manually."
        exit 1
    fi
    
    # Get IP/hostname
    while true; do
        read -rp "Enter IP address or hostname: " ip
        if [ -n "$ip" ] && [[ ! "$ip" =~ [[:space:]] ]]; then
            break
        else
            print_error "Valid IP or hostname is required (no spaces)"
        fi
    done
    
    # Get user (with default)
    read -rp "Enter SSH user [${DEFAULT_USER}]: " user
    user="${user:-$DEFAULT_USER}"
    
    # Get SSH key (optional)
    read -rp "Enter SSH key path (optional, press Enter to skip): " key
    
    # Confirm
    echo ""
    echo "=========================================="
    echo "  Review New Entry"
    echo "=========================================="
    echo "Host: ${name}"
    echo "Hostname: ${ip}"
    echo "User: ${user}"
    if [ -n "$key" ]; then
        echo "IdentityFile: ${key}"
    fi
    echo ""
    read -rp "Add this entry? (y/N): " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_warning "Cancelled. No changes made."
        exit 0
    fi
    
    # Add the host
    echo ""
    add_host "$name" "$ip" "$user" "$key"
}

# Parse command line arguments
parse_args() {
    local name=""
    local ip=""
    local user="$DEFAULT_USER"
    local key=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --name|-n)
                name="$2"
                shift 2
                ;;
            --ip|-i)
                ip="$2"
                shift 2
                ;;
            --user|-u)
                user="$2"
                shift 2
                ;;
            --key|-k)
                key="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Validate inputs
    if ! validate_inputs "$name" "$ip" "$user"; then
        exit 1
    fi
    
    # Check if host exists
    if host_exists "$name"; then
        echo ""
        print_error "Host '${name}' already exists in ${SSH_CONFIG}!"
        echo ""
        echo "EXISTING ENTRY:"
        echo "---------------"
        get_existing_host "$name"
        echo "---------------"
        echo ""
        print_warning "NO CHANGES MADE."
        echo "This tool is APPEND-ONLY and cannot modify existing entries."
        echo "To modify, please edit ${SSH_CONFIG} manually."
        exit 1
    fi
    
    # Add the host
    add_host "$name" "$ip" "$user" "$key"
}

# Main
main() {
    # Check if any arguments provided
    if [ $# -eq 0 ]; then
        interactive_mode
    else
        parse_args "$@"
    fi
}

main "$@"
