#!/usr/bin/env python3
"""Test ODIADEV TTS service without authentication."""

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
    """Test voices endpoint without authentication."""
    print("🎵 Testing voices endpoint without authentication...")
    
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

def test_tts_no_auth(voice_name, text, filename_prefix):
    """Test TTS without authentication."""
    print(f"🎤 Testing TTS with {voice_name} (no auth)...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {"Content-Type": "application/json"}
    
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
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS successful with {voice_name}!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Text Length: {data.get('text_length', 'N/A')} characters")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"{filename_prefix}_{voice_name}_{datetime.now().strftime('%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print(f"❌ No audio data for {voice_name}")
                return False
        else:
            print(f"❌ TTS failed with {voice_name}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed for {voice_name}: {e}")
        return False

def test_callwaiting_demo():
    """Test CallWaiting AI demo with Marcus voice."""
    print("\n🎯 Testing CallWaiting AI Demo with Marcus Voice")
    print("=" * 60)
    print("Generating CallWaiting AI script with Marcus voice...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    return test_tts_no_auth("american-male", CALLWAITING_SCRIPT, "callwaiting_marcus")

def test_all_voices():
    """Test all available voices."""
    print("\n🎭 Testing All Available Voices")
    print("=" * 60)
    
    # Test voices
    voices = test_voices()
    if not voices:
        print("❌ No voices available for testing")
        return 0
    
    successful_tests = 0
    
    for voice in voices:
        voice_name = voice.get('friendly_name')
        if not voice_name:
            continue
            
        print(f"\n🎤 Testing {voice_name}...")
        
        test_text = f"Hello! I am {voice_name} from ODIADEV AI TTS. I provide professional voice services for your applications."
        
        if test_tts_no_auth(voice_name, test_text, f"test_{voice_name}"):
            successful_tests += 1
    
    return successful_tests

def main():
    """Main test function."""
    print("🎯 ODIADEV TTS - Complete Service Test (No Auth)")
    print("=" * 70)
    print("Testing service without authentication...")
    print()
    
    # Test health
    if not test_health():
        print("❌ Service is not healthy. Exiting.")
        return
    
    # Test CallWaiting AI demo with Marcus voice
    callwaiting_success = test_callwaiting_demo()
    
    # Test all voices
    voice_success_count = test_all_voices()
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 70)
    print(f"✅ CallWaiting AI Demo: {'SUCCESS' if callwaiting_success else 'FAILED'}")
    print(f"✅ Voice Tests: {voice_success_count} successful")
    print(f"📁 Audio files generated in current directory")
    print(f"🌐 Service URL: {API_BASE_URL}")
    
    if callwaiting_success and voice_success_count > 0:
        print(f"\n🎉 SUCCESS! ODIADEV TTS is working perfectly!")
        print(f"✅ CallWaiting AI demo generated with Marcus voice!")
        print(f"✅ {voice_success_count} voices verified and working!")
        print(f"🚀 Service is ready for production use!")
    else:
        print(f"\n❌ Some tests failed")
        if not callwaiting_success:
            print(f"   - CallWaiting AI demo failed")
        if voice_success_count == 0:
            print(f"   - No voices working")

if __name__ == "__main__":
    main()
