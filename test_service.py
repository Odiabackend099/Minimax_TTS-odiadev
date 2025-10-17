#!/usr/bin/env python3
"""Test the ODIADEV AI TTS service."""

import requests
import json
import base64

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

def test_health():
    """Test health endpoint."""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def create_test_user():
    """Create a test user."""
    print("👤 Creating test user...")
    
    # First, try to create an admin user
    url = f"{API_BASE_URL}/admin/users"
    headers = {"Content-Type": "application/json"}
    
    user_data = {
        "name": "Test User",
        "email": "test@odiadev.com",
        "plan": "free"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=30)
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ Test user created with API key: {api_key[:20]}...")
            return api_key
        else:
            print(f"❌ Failed to create user: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_voices(api_key):
    """Test voices endpoint."""
    print("🎵 Testing voices endpoint...")
    
    url = f"{API_BASE_URL}/v1/voices"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} voices:")
            for voice in voices:
                print(f"   - {voice.get('friendly_name', 'N/A')}: {voice.get('minimax_voice_id', 'N/A')}")
            return voices
        else:
            print(f"❌ Failed to get voices: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

def test_tts(api_key, voice_name):
    """Test TTS endpoint."""
    print(f"🎤 Testing TTS with {voice_name}...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": f"Hello! This is {voice_name} from ODIADEV AI TTS.",
        "voice_name": voice_name,
        "model": "speech-02-hd",
        "speed": 1.0,
        "pitch": 0,
        "emotion": "neutral"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS successful!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            return True
        else:
            print(f"❌ TTS failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎯 ODIADEV AI TTS - Service Test")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("❌ Service is not healthy. Exiting.")
        return
    
    # Create test user
    api_key = create_test_user()
    if not api_key:
        print("❌ Could not create test user. Exiting.")
        return
    
    # Test voices
    voices = test_voices(api_key)
    if not voices:
        print("❌ Could not get voices. Exiting.")
        return
    
    # Test TTS with each voice
    success_count = 0
    for voice in voices:
        voice_name = voice.get('friendly_name')
        if voice_name:
            if test_tts(api_key, voice_name):
                success_count += 1
    
    print(f"\n📊 TEST RESULTS")
    print("=" * 50)
    print(f"✅ Successful TTS: {success_count}/{len(voices)} voices")
    print(f"❌ Failed TTS: {len(voices) - success_count}/{len(voices)} voices")
    
    if success_count == len(voices):
        print("\n🎉 ALL TESTS PASSED! ODIADEV AI TTS is working perfectly.")
    else:
        print(f"\n⚠️  {len(voices) - success_count} voices need attention.")

if __name__ == "__main__":
    main()
