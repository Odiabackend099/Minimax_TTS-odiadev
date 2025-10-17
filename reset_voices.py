#!/usr/bin/env python3
"""Reset voices to verified ODIADEV TTS voices."""

import requests
import json

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"
ADMIN_API_KEY = "your_admin_api_key_here"  # Replace with actual admin API key

def test_service():
    """Test if the service is accessible."""
    print("🏥 Testing service health...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
            return True
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Service not accessible: {e}")
        return False

def get_voices():
    """Get current voices (requires auth)."""
    print("🎵 Getting current voices...")
    
    url = f"{API_BASE_URL}/v1/voices"
    headers = {
        "Authorization": f"Bearer {ADMIN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} current voices:")
            for voice in voices:
                print(f"   - {voice.get('friendly_name', 'N/A')}: {voice.get('minimax_voice_id', 'N/A')}")
            return voices
        else:
            print(f"❌ Failed to get voices: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []

def create_admin_user():
    """Create an admin user to get API key."""
    print("👤 Creating admin user...")
    
    url = f"{API_BASE_URL}/admin/users"
    headers = {
        "Authorization": "Bearer admin-key-placeholder",  # This might not work
        "Content-Type": "application/json"
    }
    
    user_data = {
        "name": "Admin User",
        "email": "admin@odiadev.com",
        "plan": "enterprise"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=10)
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ Admin user created with API key: {api_key}")
            return api_key
        else:
            print(f"❌ Failed to create admin user: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def main():
    """Main function to reset voices."""
    print("🎯 ODIADEV AI TTS - Voice Reset")
    print("=" * 50)
    
    # Test service health
    if not test_service():
        print("❌ Service is not accessible. Check deployment status.")
        return
    
    # Try to get current voices
    voices = get_voices()
    
    if ADMIN_API_KEY == "your_admin_api_key_here":
        print("\n⚠️  ADMIN_API_KEY not set. You need to:")
        print("1. Create an admin user first")
        print("2. Get the API key from the response")
        print("3. Update this script with the API key")
        print("4. Run the migration script")
        
        # Try to create admin user
        api_key = create_admin_user()
        if api_key:
            print(f"\n✅ Use this API key: {api_key}")
            print("Update the ADMIN_API_KEY in this script and run again.")
        
        return
    
    print(f"\n📊 Current voices: {len(voices)}")
    print("The service is running with the old voice IDs.")
    print("You need to manually update the database or redeploy with a fresh database.")

if __name__ == "__main__":
    main()
