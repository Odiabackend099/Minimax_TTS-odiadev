#!/usr/bin/env python3
"""Test script to verify ODIADEV AI TTS voices are working correctly."""

import requests
import json
import base64
import os
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"
TEST_API_KEY = "your_api_key_here"  # Replace with actual API key

# Test voices
VERIFIED_VOICES = [
    {
        "name": "american-female",
        "description": "American Female - Professional",
        "test_text": "Hello! I am the American female voice. I provide clear, professional speech for business communications and customer service."
    },
    {
        "name": "american-male", 
        "description": "Marcus American Male - Authoritative",
        "test_text": "Greetings! I am Marcus, the American male voice. I deliver confident, authoritative speech for corporate communications and technical documentation."
    },
    {
        "name": "nigerian-female",
        "description": "Ezinne Nigerian Female - Professional", 
        "test_text": "Hello! I am Ezinne, the Nigerian female voice. I bring the warmth and authenticity of Nigerian culture to professional communications."
    },
    {
        "name": "nigerian-male",
        "description": "Odia Nigerian Male - Authoritative",
        "test_text": "Greetings! I am Odia, the Nigerian male voice. I represent strength and confidence in business and leadership across Africa and internationally."
    }
]

def test_voice(voice_name, test_text):
    """Test a specific voice with the given text."""
    print(f"\n🎤 Testing {voice_name}...")
    
    url = f"{API_BASE_URL}/v1/tts"
    headers = {
        "Authorization": f"Bearer {TEST_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": test_text,
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
            print(f"✅ Success!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Text Length: {data.get('text_length', 'N/A')} characters")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"test_{voice_name}_{datetime.now().strftime('%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
            
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   - Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_health():
    """Test the health endpoint."""
    print("🏥 Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_voices_list():
    """Test the voices list endpoint."""
    print("\n🎵 Testing voices list endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/v1/voices", timeout=10)
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} voices:")
            for voice in voices:
                print(f"   - {voice.get('friendly_name', 'N/A')}: {voice.get('description', 'N/A')}")
            return True
        else:
            print(f"❌ Voices list failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Voices list failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎯 ODIADEV AI TTS - Voice Verification Test")
    print("=" * 50)
    
    if TEST_API_KEY == "your_api_key_here":
        print("❌ Please set TEST_API_KEY with your actual API key")
        return
    
    # Test health
    if not test_health():
        print("❌ Health check failed. Service may be down.")
        return
    
    # Test voices list
    if not test_voices_list():
        print("❌ Voices list failed. Check authentication.")
        return
    
    # Test each voice
    success_count = 0
    for voice in VERIFIED_VOICES:
        if test_voice(voice["name"], voice["test_text"]):
            success_count += 1
    
    print(f"\n📊 TEST RESULTS")
    print("=" * 50)
    print(f"✅ Successful: {success_count}/{len(VERIFIED_VOICES)} voices")
    print(f"❌ Failed: {len(VERIFIED_VOICES) - success_count}/{len(VERIFIED_VOICES)} voices")
    
    if success_count == len(VERIFIED_VOICES):
        print("\n🎉 ALL VOICES WORKING! ODIADEV AI TTS is ready for production.")
    else:
        print(f"\n⚠️  {len(VERIFIED_VOICES) - success_count} voices need attention.")

if __name__ == "__main__":
    main()
