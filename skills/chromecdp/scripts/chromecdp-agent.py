#!/usr/bin/env python3
"""
chromecdp-agent.py - Natural language interface for Chrome CDP operations

This script provides a high-level interface that agents can use
to perform browser operations conversationally.
"""

import argparse
import json
import sys
import subprocess
import os

# FIXED: Always use port 9222
CHROME_CDP_URL = "http://127.0.0.1:9222"
CHROME_PORT = "9222"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")


def run_shell(cmd):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def ensure_chrome():
    """Ensure Chrome is running on port 9222"""
    # Check if Chrome is already running on port 9222
    success, stdout, _ = run_shell(f"curl -s {CHROME_CDP_URL}/json/version")
    if success:
        return True
    
    # Start Chrome
    start_script = os.path.join(SCRIPTS_DIR, "chromecdp-start.sh")
    success, stdout, stderr = run_shell(f"bash {start_script}")
    return success


def handle_popups():
    """Handle any blocking popups"""
    popup_script = os.path.join(SCRIPTS_DIR, "chromecdp-popup-handler.py")
    success, stdout, stderr = run_shell(f"python3 {popup_script} --auto-close --quiet")
    return success, stdout


def navigate_to(url):
    """Navigate to a URL using browser tool"""
    # This would be called via the agent's browser tool
    # For now, return the action the agent should take
    return {
        "action": "open",
        "url": url,
        "target": "host"
    }


def main():
    parser = argparse.ArgumentParser(
        description="Natural language browser automation helper"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Ensure Chrome is running
    subparsers.add_parser("ensure-chrome", help="Ensure Chrome is running")
    
    # Handle popups
    subparsers.add_parser("handle-popups", help="Detect and close popups")
    
    # Get status
    subparsers.add_parser("status", help="Get Chrome status")
    
    args = parser.parse_args()
    
    if args.command == "ensure-chrome":
        if ensure_chrome():
            print(json.dumps({"status": "ready", "message": "Chrome is running"}))
            sys.exit(0)
        else:
            print(json.dumps({"status": "error", "message": "Failed to start Chrome"}))
            sys.exit(1)
    
    elif args.command == "handle-popups":
        success, output = handle_popups()
        print(json.dumps({"status": "success" if success else "error", "output": output}))
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        status_script = os.path.join(SCRIPTS_DIR, "chromecdp-status.sh")
        success, stdout, _ = run_shell(f"bash {status_script}")
        print(stdout)
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
