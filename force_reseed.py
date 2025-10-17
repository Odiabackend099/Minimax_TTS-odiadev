#!/usr/bin/env python3
"""Force database reseed with verified voices."""

import requests
import json

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

def trigger_reseed():
    """Trigger a database reseed by calling the init endpoint."""
    print("🔄 Triggering database reseed...")
    
    # Try to access the init endpoint if it exists
    try:
        response = requests.post(f"{API_BASE_URL}/admin/reseed", timeout=30)
        if response.status_code == 200:
            print("✅ Database reseed triggered successfully")
            return True
        else:
            print(f"❌ Reseed failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main function."""
    print("🎯 ODIADEV AI TTS - Force Reseed")
    print("=" * 50)
    
    # Check if service is healthy
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Service not accessible: {e}")
        return
    
    # Try to trigger reseed
    if trigger_reseed():
        print("\n🎉 Database reseed completed!")
        print("The service should now have the verified voice IDs.")
    else:
        print("\n⚠️  Manual reseed required.")
        print("The database needs to be manually updated with the new voice IDs.")

if __name__ == "__main__":
    main()
