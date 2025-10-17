#!/usr/bin/env python3
"""Generate multiple API keys to test the ODIADEV TTS service."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def create_user(user_number):
    """Create a user and return API key."""
    print(f"👤 Creating user {user_number}...")
    
    url = f"{API_BASE_URL}/admin/users"
    headers = {"Content-Type": "application/json"}
    
    user_data = {
        "name": f"Test User {user_number}",
        "email": f"test{user_number}@callwaiting.ai",
        "plan": "free"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=30)
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ User {user_number} created with API key: {api_key[:20]}...")
            return api_key
        else:
            print(f"❌ Failed to create user {user_number}: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed for user {user_number}: {e}")
        return None

def test_tts(api_key, user_number):
    """Test TTS with the API key."""
    print(f"🎤 Testing TTS for user {user_number}...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": CALLWAITING_SCRIPT,
        "voice_name": "american-male",
        "model": "speech-02-hd",
        "speed": 1.0,
        "pitch": 0,
        "emotion": "neutral"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS successful for user {user_number}!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"callwaiting_marcus_user{user_number}_{datetime.now().strftime('%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print(f"❌ No audio data for user {user_number}")
                return False
        else:
            print(f"❌ TTS failed for user {user_number}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed for user {user_number}: {e}")
        return False

def main():
    """Generate API keys and test TTS."""
    print("🎯 ODIADEV TTS - API Key Generation & Testing")
    print("=" * 60)
    print("Generating multiple API keys to test the service...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    # Test service health first
    print("🏥 Testing service health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Service not accessible: {e}")
        return
    
    # Generate API keys and test
    successful_users = 0
    total_users = 10
    
    for i in range(1, total_users + 1):
        print(f"\n--- USER {i}/{total_users} ---")
        
        # Create user
        api_key = create_user(i)
        if not api_key:
            print(f"❌ Skipping user {i} - no API key")
            continue
        
        # Test TTS
        if test_tts(api_key, i):
            successful_users += 1
        
        print(f"User {i} completed")
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"✅ Successful TTS generations: {successful_users}/{total_users}")
    print(f"❌ Failed: {total_users - successful_users}/{total_users}")
    
    if successful_users > 0:
        print(f"\n🎉 SUCCESS! ODIADEV TTS is working!")
        print(f"Generated {successful_users} CallWaiting AI demos using Marcus voice")
        print(f"Service URL: {API_BASE_URL}")
    else:
        print(f"\n❌ No successful TTS generations")
        print("The service may require admin authentication")

if __name__ == "__main__":
    main()
