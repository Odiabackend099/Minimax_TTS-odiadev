#!/usr/bin/env python3
"""Generate CallWaiting AI demo using Marcus voice from ODIADEV TTS service."""

import requests
import json
import base64
import os
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script with voice direction cues
CALLWAITING_SCRIPT = """[WHISPERING] Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. [slows down] For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. [emphasized] Never miss a valuable opportunity again. [EXCITED] Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def create_user():
    """Create a user to get API access."""
    print("👤 Creating user for API access...")
    
    # Try to create user without admin auth (might work if no auth required)
    url = f"{API_BASE_URL}/admin/users"
    headers = {"Content-Type": "application/json"}
    
    user_data = {
        "name": "CallWaiting Demo User",
        "email": f"demo-{datetime.now().strftime('%Y%m%d%H%M%S')}@callwaiting.ai",
        "plan": "free"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=30)
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ User created with API key: {api_key[:20]}...")
            return api_key
        else:
            print(f"❌ Failed to create user: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def generate_tts(api_key, text, voice_name, filename):
    """Generate TTS using the service."""
    print(f"🎤 Generating TTS with {voice_name}...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice_name": voice_name,
        "model": "speech-02-hd",
        "speed": 1.0,
        "pitch": 0,
        "emotion": "neutral"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS generated successfully!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print("❌ No audio data in response")
                return False
        else:
            print(f"❌ TTS generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Generate CallWaiting AI demo."""
    print("🎯 CallWaiting AI - Marcus Voice Demo")
    print("=" * 50)
    print("Generating CallWaiting AI script using Marcus voice...")
    print(f"Script length: {len(CALLWAITING_SCRIPT)} characters")
    print()
    
    # Create user
    api_key = create_user()
    if not api_key:
        print("❌ Could not create user. Cannot proceed.")
        return
    
    # Generate TTS
    filename = f"callwaiting_marcus_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    if generate_tts(api_key, CALLWAITING_SCRIPT, "american-male", filename):
        print(f"\n🎉 SUCCESS!")
        print(f"CallWaiting AI demo generated: {filename}")
        print(f"Voice: Marcus (American Male)")
        print(f"Service: ODIADEV AI TTS")
        print(f"Duration: ~{len(CALLWAITING_SCRIPT.split()) / 3:.1f} seconds")
    else:
        print("\n❌ Failed to generate demo")

if __name__ == "__main__":
    main()
