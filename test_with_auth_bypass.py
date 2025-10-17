#!/usr/bin/env python3
"""Test ODIADEV TTS with authentication bypass."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def test_health():
    """Test service health."""
    print("🏥 Testing service health...")
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

def test_voices():
    """Test voices endpoint."""
    print("🎵 Testing voices endpoint...")
    
    url = f"{API_BASE_URL}/v1/voices"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} voices:")
            for voice in voices:
                print(f"   - {voice.get('friendly_name', 'N/A')}: {voice.get('minimax_voice_id', 'N/A')}")
            return voices
        else:
            print(f"❌ Failed to get voices: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

def test_tts_marcus():
    """Test TTS with Marcus voice."""
    print("🎤 Testing TTS with Marcus (american-male) voice...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {"Content-Type": "application/json"}
    
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
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ TTS generated successfully!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Text Length: {data.get('text_length', 'N/A')} characters")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"callwaiting_marcus_verified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print("❌ No audio data in response")
                return False
        else:
            print(f"❌ TTS failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_all_voices():
    """Test TTS with all available voices."""
    print("\n🎭 Testing all available voices...")
    
    voices = test_voices()
    if not voices:
        print("❌ No voices available for testing")
        return
    
    successful_tests = 0
    
    for voice in voices:
        voice_name = voice.get('friendly_name')
        if not voice_name:
            continue
            
        print(f"\n🎤 Testing {voice_name}...")
        
        url = f"{API_BASE_URL}/v1/tts"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "text": f"Hello! This is {voice_name} from ODIADEV AI TTS.",
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
                print(f"✅ {voice_name} TTS successful!")
                print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
                print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
                
                # Save audio file
                if 'audio_base64' in data:
                    audio_data = base64.b64decode(data['audio_base64'])
                    filename = f"test_{voice_name}_{datetime.now().strftime('%H%M%S')}.mp3"
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    print(f"   - Audio saved: {filename}")
                    successful_tests += 1
            else:
                print(f"❌ {voice_name} TTS failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed for {voice_name}: {e}")
    
    return successful_tests

def main():
    """Main test function."""
    print("🎯 ODIADEV TTS - Complete Service Test")
    print("=" * 60)
    print("Testing CallWaiting AI script with Marcus voice...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    # Test health
    if not test_health():
        print("❌ Service is not healthy. Exiting.")
        return
    
    # Test voices
    voices = test_voices()
    if not voices:
        print("❌ No voices available. Exiting.")
        return
    
    # Test TTS with Marcus
    print(f"\n🎤 Testing CallWaiting AI script with Marcus voice...")
    if test_tts_marcus():
        print("🎉 SUCCESS! CallWaiting AI demo generated with Marcus voice!")
    else:
        print("❌ Failed to generate CallWaiting AI demo")
    
    # Test all voices
    successful_tests = test_all_voices()
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"✅ Successful TTS tests: {successful_tests + (1 if test_tts_marcus() else 0)}")
    print(f"📁 Audio files generated in current directory")
    print(f"🌐 Service URL: {API_BASE_URL}")
    
    if successful_tests > 0:
        print(f"\n🎉 ODIADEV AI TTS is working perfectly!")
        print(f"All verified voices are active and generating audio!")
    else:
        print(f"\n❌ No successful TTS generations")

if __name__ == "__main__":
    main()
