#!/usr/bin/env python3
"""Database migration script to update voices to verified ODIADEV TTS voices."""

import requests
import json
import os

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"
ADMIN_API_KEY = "your_admin_api_key_here"  # Replace with actual admin API key

# New verified voices
VERIFIED_VOICES = [
    {
        "friendly_name": "american-female",
        "minimax_voice_id": "moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a",
        "language": "en-US",
        "gender": "female",
        "description": "American female voice with professional, neutral tone - verified for production use",
        "is_cloned": False,
    },
    {
        "friendly_name": "american-male",
        "minimax_voice_id": "moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc",
        "language": "en-US",
        "gender": "male",
        "description": "Marcus American male voice with confident, neutral tone - verified for production use",
        "is_cloned": False,
    },
    {
        "friendly_name": "nigerian-female",
        "minimax_voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
        "language": "en-NG",
        "gender": "female",
        "description": "Ezinne Nigerian female voice with professional, neutral tone - verified for production use",
        "is_cloned": False,
    },
    {
        "friendly_name": "nigerian-male",
        "minimax_voice_id": "moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc",
        "language": "en-NG",
        "gender": "male",
        "description": "Odia Nigerian male voice with strong, authoritative tone - verified for production use",
        "is_cloned": False,
    },
]

def create_voice(voice_data):
    """Create a new voice via API."""
    url = f"{API_BASE_URL}/admin/voices"
    headers = {
        "Authorization": f"Bearer {ADMIN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=voice_data, timeout=30)
        
        if response.status_code == 201:
            print(f"✅ Created voice: {voice_data['friendly_name']}")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"⏭️  Voice already exists: {voice_data['friendly_name']}")
            return True
        else:
            print(f"❌ Failed to create {voice_data['friendly_name']}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {voice_data['friendly_name']}: {e}")
        return False

def main():
    """Migrate voices to verified ODIADEV TTS voices."""
    print("🎯 ODIADEV AI TTS - Voice Migration")
    print("=" * 50)
    
    if ADMIN_API_KEY == "your_admin_api_key_here":
        print("❌ Please set ADMIN_API_KEY with your actual admin API key")
        return
    
    print("Creating verified voices...")
    
    success_count = 0
    for voice in VERIFIED_VOICES:
        if create_voice(voice):
            success_count += 1
    
    print(f"\n📊 MIGRATION RESULTS")
    print("=" * 50)
    print(f"✅ Successful: {success_count}/{len(VERIFIED_VOICES)} voices")
    print(f"❌ Failed: {len(VERIFIED_VOICES) - success_count}/{len(VERIFIED_VOICES)} voices")
    
    if success_count == len(VERIFIED_VOICES):
        print("\n🎉 ALL VOICES MIGRATED! ODIADEV AI TTS is ready with verified voices.")
    else:
        print(f"\n⚠️  {len(VERIFIED_VOICES) - success_count} voices need manual attention.")

if __name__ == "__main__":
    main()
