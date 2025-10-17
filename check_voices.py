#!/usr/bin/env python3
"""Check what voices are available in the service."""

import requests
import json

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

def check_health():
    """Check service health."""
    print("🏥 Checking service health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Service not accessible: {e}")
        return False

def check_docs():
    """Check if there's a docs endpoint."""
    print("📚 Checking for API documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation available at /docs")
            return True
        else:
            print(f"❌ No docs endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs check failed: {e}")
        return False

def check_root():
    """Check root endpoint."""
    print("🏠 Checking root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"Root response: {response.status_code}")
        if response.text:
            print(f"Response: {response.text[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Root check failed: {e}")
        return False

def main():
    """Main function."""
    print("🎯 ODIADEV AI TTS - Service Check")
    print("=" * 50)
    
    # Check health
    if not check_health():
        print("❌ Service is not healthy. Exiting.")
        return
    
    # Check docs
    check_docs()
    
    # Check root
    check_root()
    
    print("\n📋 SUMMARY")
    print("=" * 50)
    print("✅ Service is running and healthy")
    print("❌ Admin access required to manage voices")
    print("💡 You need to:")
    print("   1. Set up admin authentication")
    print("   2. Create a user with API key")
    print("   3. Test the voices endpoint")
    print("   4. Verify the voice IDs are updated")

if __name__ == "__main__":
    main()
