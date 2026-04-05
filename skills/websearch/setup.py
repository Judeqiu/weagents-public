#!/usr/bin/env python3
"""
Setup script for websearch skill.
Interactive configuration with validation and testing.
"""

import json
import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")


def find_existing_key():
    """Find existing API key from various sources."""
    # Check environment
    env_key = os.environ.get("BRAVE_API_KEY")
    if env_key and not env_key.startswith("YOUR_"):
        return "environment", env_key
    
    # Check config files
    config_paths = [
        Path("config.json"),
        Path(__file__).parent / "config.json",
        Path.home() / ".config" / "websearch" / "config.json",
    ]
    
    for path in config_paths:
        if path.exists():
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                key = config.get("brave_api_key", "")
                if key and not key.startswith("YOUR_"):
                    return str(path), key
            except (json.JSONDecodeError, IOError):
                continue
    
    return None, None


def validate_api_key(key):
    """Validate API key format."""
    if not key:
        return False, "Key is empty"
    
    if len(key) < 20:
        return False, "Key is too short"
    
    # Brave API keys typically start with BS or sk-
    if not (key.startswith("BS") or key.startswith("sk-")):
        return False, "Key format looks unusual (should start with 'BS' or 'sk-')"
    
    return True, "Valid"


def test_api_key(key):
    """Test API key by making a simple request."""
    try:
        import requests
        
        headers = {
            "X-Subscription-Token": key,
            "Accept": "application/json",
        }
        
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": "test", "count": 1},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "API key is working!"
        elif response.status_code == 401:
            return False, "Invalid API key (401 Unauthorized)"
        elif response.status_code == 429:
            return False, "Rate limit exceeded (429 Too Many Requests)"
        else:
            return False, f"API error: {response.status_code}"
            
    except ImportError:
        return None, "Cannot test - 'requests' package not installed"
    except Exception as e:
        return False, f"Test failed: {str(e)}"


def save_api_key(key, location="config"):
    """Save API key to specified location."""
    if location == "config":
        config_path = Path(__file__).parent / "config.json"
        config = {"brave_api_key": key}
        
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            os.chmod(config_path, 0o600)
            return True, str(config_path)
        except IOError as e:
            return False, str(e)
    
    elif location == "global":
        config_dir = Path.home() / ".config" / "websearch"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "config.json"
        config = {"brave_api_key": key}
        
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            os.chmod(config_path, 0o600)
            return True, str(config_path)
        except IOError as e:
            return False, str(e)
    
    elif location == "env":
        shell = os.environ.get("SHELL", "/bin/bash")
        if "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            rc_file = Path.home() / ".bashrc"
        
        try:
            with open(rc_file, "a") as f:
                f.write(f'\n# Brave Search API Key for websearch skill\n')
                f.write(f'export BRAVE_API_KEY="{key}"\n')
            return True, str(rc_file)
        except IOError as e:
            return False, str(e)
    
    return False, "Unknown location"


def interactive_setup():
    """Run interactive setup wizard."""
    print_header("Websearch Skill Setup Wizard")
    
    print("This wizard will help you configure the Brave Search API key.")
    print("You can get a free API key at: https://api.search.brave.com/app/keys")
    print()
    
    # Check for existing key
    existing_source, existing_key = find_existing_key()
    
    if existing_key:
        print_success(f"Found existing API key in: {existing_source}")
        print_info(f"Key: {existing_key[:10]}...{existing_key[-5:]}")
        print()
        
        response = input("Do you want to update this key? (y/N): ").strip().lower()
        if response != 'y':
            print()
            print_success("Keeping existing configuration.")
            test_existing = input("Test the existing key? (Y/n): ").strip().lower()
            if test_existing != 'n':
                print()
                print("Testing API key...")
                success, message = test_api_key(existing_key)
                if success:
                    print_success(message)
                elif success is None:
                    print_warning(message)
                else:
                    print_error(message)
            return
    
    print()
    print("Step 1: Enter your Brave Search API key")
    print("-" * 60)
    print("Get your key from: https://api.search.brave.com/app/keys")
    print("Free tier: 2,000 queries/month")
    print()
    
    while True:
        api_key = input("API Key: ").strip()
        
        if not api_key:
            print_error("API key cannot be empty")
            continue
        
        valid, message = validate_api_key(api_key)
        if not valid:
            print_warning(f"Validation: {message}")
            confirm = input("Continue anyway? (y/N): ").strip().lower()
            if confirm != 'y':
                continue
        
        break
    
    print()
    print("Step 2: Choose where to save the API key")
    print("-" * 60)
    print("1) Skill directory (config.json) - Recommended for single user")
    print("2) Global config (~/.config/websearch/) - System-wide")
    print("3) Shell environment (.bashrc/.zshrc) - Works across tools")
    print()
    
    while True:
        choice = input("Choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print_error("Please enter 1, 2, or 3")
    
    location_map = {'1': 'config', '2': 'global', '3': 'env'}
    location = location_map[choice]
    
    print()
    print("Step 3: Testing and saving")
    print("-" * 60)
    
    # Test the key
    print("Testing API key...")
    success, message = test_api_key(api_key)
    
    if success:
        print_success(message)
    elif success is None:
        print_warning(message)
    else:
        print_error(message)
        print()
        proceed = input("Save key anyway? (y/N): ").strip().lower()
        if proceed != 'y':
            print()
            print_error("Setup cancelled.")
            return
    
    # Save the key
    print()
    print(f"Saving API key to {location}...")
    saved, path_or_error = save_api_key(api_key, location)
    
    if saved:
        print_success(f"API key saved to: {path_or_error}")
    else:
        print_error(f"Failed to save: {path_or_error}")
        print()
        print_info("You can manually set the API key:")
        print(f'  export BRAVE_API_KEY="{api_key}"')
        return
    
    # Final summary
    print()
    print_header("Setup Complete!")
    print_success("Websearch skill is configured and ready to use")
    print()
    print("Quick test:")
    print('  python3 search.py "hello world"')
    print()
    print("Interactive mode:")
    print('  python3 search.py --interactive')
    print()
    print("API Limits (Free Tier):")
    print("  - 2,000 queries per month")
    print("  - 1 query per second")
    print()


def quick_test():
    """Run quick API test."""
    print_header("API Key Test")
    
    source, key = find_existing_key()
    
    if not key:
        print_error("No API key found")
        print()
        print_info("Configure an API key first:")
        print("  python3 setup.py")
        return False
    
    print_info(f"Found API key in: {source}")
    print_info(f"Key: {key[:10]}...{key[-5:]}")
    print()
    
    print("Testing API connectivity...")
    print("-" * 60)
    
    success, message = test_api_key(key)
    
    if success:
        print_success(message)
        
        # Try an actual search
        print()
        print("Performing test search...")
        try:
            from search import BraveSearchClient
            client = BraveSearchClient()
            results = client.search("test", limit=1, use_cache=False)
            print_success(f"Search successful! Found {results['total_results']} results")
            return True
        except Exception as e:
            print_error(f"Search test failed: {e}")
            return False
    
    elif success is None:
        print_warning(message)
        return None
    else:
        print_error(message)
        print()
        print_info("Troubleshooting:")
        print("  1. Check your API key at https://api.search.brave.com/app/keys")
        print("  2. Ensure the key is active and not expired")
        print("  3. Check your internet connection")
        return False


def show_status():
    """Show current configuration status."""
    print_header("Configuration Status")
    
    # Check all possible locations
    locations = []
    
    # Environment
    env_key = os.environ.get("BRAVE_API_KEY")
    if env_key and not env_key.startswith("YOUR_"):
        locations.append(("Environment Variable", f"BRAVE_API_KEY={env_key[:10]}...{env_key[-5:]}", True))
    else:
        locations.append(("Environment Variable", "Not set", False))
    
    # Config files
    config_paths = [
        ("Skill Directory", Path(__file__).parent / "config.json"),
        ("Global Config", Path.home() / ".config" / "websearch" / "config.json"),
        ("OpenClaw Skills", Path.home() / ".openclaw" / "workspace" / "skills" / "websearch" / "config.json"),
    ]
    
    for name, path in config_paths:
        if path.exists():
            try:
                with open(path, "r") as f:
                    config = json.load(f)
                key = config.get("brave_api_key", "")
                if key and not key.startswith("YOUR_"):
                    locations.append((name, f"{path}\n  Key: {key[:10]}...{key[-5:]}", True))
                else:
                    locations.append((name, f"{path}\n  No valid key", False))
            except (json.JSONDecodeError, IOError) as e:
                locations.append((name, f"{path}\n  Error: {e}", False))
        else:
            locations.append((name, f"{path}\n  Not found", False))
    
    # Print status
    for name, status, ok in locations:
        symbol = "✅" if ok else "❌"
        print(f"{symbol} {name}")
        for line in status.split('\n'):
            print(f"   {line}")
        print()
    
    # Overall status
    has_key = any(ok for _, _, ok in locations)
    if has_key:
        print_success("At least one valid API key configuration found")
    else:
        print_error("No valid API key configuration found")
        print()
        print_info("Run setup to configure:")
        print("  python3 setup.py")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ["--test", "-t", "test"]:
            quick_test()
        
        elif command in ["--status", "-s", "status"]:
            show_status()
        
        elif command in ["--help", "-h", "help"]:
            print_header("Websearch Setup - Help")
            print("Usage: python3 setup.py [command]")
            print()
            print("Commands:")
            print("  (no command)    Run interactive setup wizard")
            print("  --test, -t      Test the configured API key")
            print("  --status, -s    Show configuration status")
            print("  --help, -h      Show this help message")
            print()
            print("Examples:")
            print("  python3 setup.py                    # Interactive setup")
            print("  python3 setup.py --test             # Test API key")
            print("  python3 setup.py --status           # Check configuration")
        
        else:
            print_error(f"Unknown command: {command}")
            print("Use --help for usage information")
            sys.exit(1)
    else:
        interactive_setup()


if __name__ == "__main__":
    main()
