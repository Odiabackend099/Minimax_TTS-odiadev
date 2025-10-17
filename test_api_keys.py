#!/usr/bin/env python3
"""Test ODIADEV TTS with generated API keys."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

# Generated API keys
API_KEYS = [
    "5hKMJhmixHQYGJqxQDizIMjdZODAVjhe",
    "ioMz5ACdNfIcQ7xbR5Zar3XOD1UdNN27",
    "I7OUyAdNWiviDX2JdCGJZyBJI4UBgJIF",
    "A65hNxfVolKNRhSw9L032J5HWc7GNGwI",
    "udKR8aIs4QBaa4RIiPnZTOYFiGLfmIm4",
    "dJsw47CbP29chkEwxuKFMuHh1oxMCzbN",
    "QYlpFv92XVdaXZOeCQgnd01x4K5snl0T",
    "2QlyYDNVyDYXUsrOLdlCGJgvvwslQou9",
    "2rDokxw4ejK672Lakj6tnsB0XuAvUA7a",
    "WavvLu9rC5cnsbTvU3t6J7zrM4nscVqp",
]

def test_tts_with_key(api_key, key_number):
    """Test TTS with a specific API key."""
    print(f"🎤 Testing API key {key_number}...")
    
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
            print(f"✅ API key {key_number} successful!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"callwaiting_marcus_key{key_number}_{datetime.now().strftime('%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print(f"❌ No audio data for key {key_number}")
                return False
        else:
            print(f"❌ API key {key_number} failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed for key {key_number}: {e}")
        return False

def main():
    """Test all API keys."""
    print("🎯 ODIADEV TTS - API Key Testing")
    print("=" * 50)
    print(f"Testing {len(API_KEYS)} API keys...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    successful_tests = 0
    
    for i, api_key in enumerate(API_KEYS, 1):
        print(f"\n--- API KEY {i}/{len(API_KEYS)} ---")
        if test_tts_with_key(api_key, i):
            successful_tests += 1
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 50)
    print(f"✅ Successful tests: {successful_tests}/{len(API_KEYS)}")
    print(f"❌ Failed tests: {len(API_KEYS) - successful_tests}/{len(API_KEYS)}")
    
    if successful_tests > 0:
        print(f"\n🎉 SUCCESS! ODIADEV TTS is working!")
        print(f"Generated {successful_tests} CallWaiting AI demos!")
    else:
        print(f"\n❌ No successful tests")

if __name__ == "__main__":
    main()
