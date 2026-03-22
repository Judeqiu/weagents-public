#!/usr/bin/env python3
"""
Quick test script for Marketing Creator skill.
Verifies setup and API connectivity without consuming credits.
"""

import os
import sys
from pathlib import Path

# Add skill directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from byteplus_client import BytePlusClient


def test_setup():
    """Test basic setup."""
    print("🔧 Testing Marketing Creator Setup")
    print("=" * 50)
    
    # Check Python version
    print(f"\n✓ Python version: {sys.version.split()[0]}")
    
    # Check dependencies
    try:
        import requests
        print("✓ requests: OK")
    except ImportError:
        print("✗ requests: NOT INSTALLED (pip install requests)")
        return False
    
    try:
        from byteplussdkarkruntime import Ark
        print("✓ byteplus-python-sdk-v2: OK (video generation available)")
    except ImportError:
        print("⚠ byteplus-python-sdk-v2: NOT INSTALLED")
        print("  Install with: pip install byteplus-python-sdk-v2 pydantic")
        print("  Note: Image generation works without SDK. Video generation requires SDK.")
    
    # Check API key (config.json or env var)
    config_path = Path(__file__).parent / "config.json"
    api_key = None
    config_source = None
    
    if config_path.exists():
        try:
            import json
            with open(config_path) as f:
                config = json.load(f)
                api_key = config.get("api_key")
                if api_key:
                    config_source = "config.json"
        except (json.JSONDecodeError, IOError):
            pass
    
    if not api_key:
        api_key = os.environ.get("ARK_API_KEY")
        if api_key:
            config_source = "environment variable"
    
    if api_key:
        masked = f"{api_key[:8]}...{api_key[-4:]}"
        print(f"✓ API Key: {masked} (from {config_source})")
    else:
        print("✗ API Key: NOT CONFIGURED")
        print("  Option 1: Add to config.json")
        print("  Option 2: Set ARK_API_KEY environment variable")
        print("  Get your key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey")
        return False
    
    return True


def test_client_init():
    """Test client initialization."""
    print("\n🔌 Testing API Client")
    print("-" * 50)
    
    try:
        client = BytePlusClient()
        print("✓ Client initialized successfully")
        
        print("\n  Available Image Models:")
        for name, model_id in client.IMAGE_MODELS.items():
            print(f"    • {name}: {model_id}")
        
        print("\n  Available Video Models:")
        for name, model_id in client.VIDEO_MODELS.items():
            print(f"    • {name}: {model_id}")
        
        return True
        
    except Exception as e:
        print(f"✗ Client initialization failed: {e}")
        return False


def main():
    """Run all tests."""
    print()
    
    setup_ok = test_setup()
    
    if not setup_ok:
        print("\n" + "=" * 50)
        print("❌ Setup incomplete. Please fix the issues above.")
        print("\nInstall dependencies:")
        print("  pip install -r requirements.txt")
        print("\nSet API key:")
        print("  export ARK_API_KEY='your-byteplus-api-key'")
        return 1
    
    client_ok = test_client_init()
    
    if not client_ok:
        print("\n" + "=" * 50)
        print("❌ Client test failed.")
        return 1
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Marketing Creator is ready.")
    print("\nQuick start:")
    print("  ./marketing.py models")
    print("  ./marketing.py image \"Your prompt here\"")
    print("  ./marketing.py campaign --product \"X\" --audience \"Y\"")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
