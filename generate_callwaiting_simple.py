#!/usr/bin/env python3
"""Generate CallWaiting AI demo using Marcus voice - Simple version."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def test_service():
    """Test if service is accessible."""
    print("🏥 Testing service health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
            return True
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Service not accessible: {e}")
        return False

def check_docs():
    """Check API documentation."""
    print("📚 Checking API documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            print("✅ API documentation accessible")
            print(f"   - Title: {spec.get('info', {}).get('title', 'N/A')}")
            print(f"   - Version: {spec.get('info', {}).get('version', 'N/A')}")
            
            # Check available endpoints
            paths = spec.get('paths', {})
            print(f"   - Available endpoints: {len(paths)}")
            for path in paths.keys():
                print(f"     - {path}")
            
            return True
        else:
            print(f"❌ API documentation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documentation check failed: {e}")
        return False

def try_direct_tts():
    """Try to call TTS endpoint directly."""
    print("🎤 Attempting direct TTS call...")
    
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
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"callwaiting_marcus_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
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

def main():
    """Generate CallWaiting AI demo."""
    print("🎯 CallWaiting AI - Marcus Voice Demo")
    print("=" * 50)
    print("Generating CallWaiting AI script using Marcus voice...")
    print(f"Script length: {len(CALLWAITING_SCRIPT)} characters")
    print()
    
    # Test service
    if not test_service():
        print("❌ Service is not accessible. Exiting.")
        return
    
    # Check documentation
    check_docs()
    
    # Try direct TTS call
    if try_direct_tts():
        print(f"\n🎉 SUCCESS!")
        print(f"CallWaiting AI demo generated using Marcus voice!")
        print(f"Service: ODIADEV AI TTS")
    else:
        print("\n❌ Failed to generate demo")
        print("The service requires authentication to generate TTS.")
        print("You need to:")
        print("1. Create an admin user first")
        print("2. Get the API key")
        print("3. Use the API key for TTS generation")

if __name__ == "__main__":
    main()
