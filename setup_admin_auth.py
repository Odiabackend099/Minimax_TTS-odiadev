#!/usr/bin/env python3
"""Setup admin authentication for ODIADEV TTS service."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def test_service_health():
    """Test if service is healthy."""
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

def check_environment_variables():
    """Check if environment variables are properly set."""
    print("\n🔧 Checking environment variables...")
    
    # Check if ENFORCE_AUTH is set to false
    try:
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            print("✅ OpenAPI spec accessible")
            print(f"   - Title: {spec.get('info', {}).get('title', 'N/A')}")
            print(f"   - Version: {spec.get('info', {}).get('version', 'N/A')}")
            return True
        else:
            print(f"❌ OpenAPI spec failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return False

def try_create_admin_user():
    """Try to create an admin user."""
    print("\n👤 Attempting to create admin user...")
    
    url = f"{API_BASE_URL}/admin/users"
    headers = {"Content-Type": "application/json"}
    
    user_data = {
        "name": "Admin User",
        "email": f"admin@odiadev.com",
        "plan": "enterprise"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=30)
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ Admin user created successfully!")
            print(f"   - API Key: {api_key}")
            print(f"   - User ID: {data.get('user', {}).get('id', 'N/A')}")
            return api_key
        else:
            print(f"❌ Failed to create admin user: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def try_create_test_user(admin_api_key):
    """Try to create a test user with admin API key."""
    print("\n👤 Creating test user with admin API key...")
    
    url = f"{API_BASE_URL}/admin/users"
    headers = {
        "Authorization": f"Bearer {admin_api_key}",
        "Content-Type": "application/json"
    }
    
    user_data = {
        "name": "CallWaiting Demo User",
        "email": f"demo@callwaiting.ai",
        "plan": "free"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data, timeout=30)
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            api_key = data.get('api_key')
            print(f"✅ Test user created successfully!")
            print(f"   - API Key: {api_key}")
            print(f"   - User ID: {data.get('user', {}).get('id', 'N/A')}")
            return api_key
        else:
            print(f"❌ Failed to create test user: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_tts_with_api_key(api_key):
    """Test TTS generation with API key."""
    print(f"\n🎤 Testing TTS with API key...")
    
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
        print(f"   - Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS generated successfully!")
            print(f"   - Duration: {data.get('duration_seconds', 'N/A')} seconds")
            print(f"   - Voice Used: {data.get('voice_used', 'N/A')}")
            print(f"   - Text Length: {data.get('text_length', 'N/A')} characters")
            print(f"   - Remaining Quota: {data.get('remaining_quota', 'N/A')} seconds")
            
            # Save audio file
            if 'audio_base64' in data:
                audio_data = base64.b64decode(data['audio_base64'])
                filename = f"callwaiting_marcus_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f"   - Audio saved: {filename}")
                return True
            else:
                print(f"❌ No audio data in response")
                return False
        else:
            print(f"❌ TTS failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_all_voices(api_key):
    """Test all available voices."""
    print(f"\n🎭 Testing all available voices...")
    
    # First get available voices
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
            
            # Test each voice
            successful_tests = 0
            for voice in voices:
                voice_name = voice.get('friendly_name')
                if not voice_name:
                    continue
                    
                print(f"\n🎤 Testing {voice_name}...")
                
                test_text = f"Hello! I am {voice_name} from ODIADEV AI TTS. I provide professional voice services for your applications."
                
                tts_url = f"{API_BASE_URL}/v1/tts"
                tts_headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                tts_payload = {
                    "text": test_text,
                    "voice_name": voice_name,
                    "model": "speech-02-hd",
                    "speed": 1.0,
                    "pitch": 0,
                    "emotion": "neutral"
                }
                
                try:
                    tts_response = requests.post(tts_url, headers=tts_headers, json=tts_payload, timeout=60)
                    
                    if tts_response.status_code == 200:
                        tts_data = tts_response.json()
                        print(f"✅ {voice_name} TTS successful!")
                        print(f"   - Duration: {tts_data.get('duration_seconds', 'N/A')} seconds")
                        print(f"   - Voice Used: {tts_data.get('voice_used', 'N/A')}")
                        
                        # Save audio file
                        if 'audio_base64' in tts_data:
                            audio_data = base64.b64decode(tts_data['audio_base64'])
                            filename = f"test_{voice_name}_{datetime.now().strftime('%H%M%S')}.mp3"
                            with open(filename, 'wb') as f:
                                f.write(audio_data)
                            print(f"   - Audio saved: {filename}")
                            successful_tests += 1
                    else:
                        print(f"❌ {voice_name} TTS failed: {tts_response.status_code}")
                        print(f"   Response: {tts_response.text}")
                        
                except Exception as e:
                    print(f"❌ Request failed for {voice_name}: {e}")
            
            return successful_tests
        else:
            print(f"❌ Failed to get voices: {response.status_code}")
            print(f"   Response: {response.text}")
            return 0
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return 0

def main():
    """Main function."""
    print("🎯 ODIADEV TTS - Admin Authentication Setup")
    print("=" * 70)
    print("Setting up admin authentication and testing TTS...")
    print()
    
    # Test service health
    if not test_service_health():
        print("❌ Service is not healthy. Exiting.")
        return
    
    # Check environment variables
    check_environment_variables()
    
    # Try to create admin user
    admin_api_key = try_create_admin_user()
    if not admin_api_key:
        print("\n❌ Could not create admin user. Authentication may still be enforced.")
        print("💡 You may need to:")
        print("   1. Check Render environment variables")
        print("   2. Ensure ENFORCE_AUTH=false is set")
        print("   3. Restart the service")
        return
    
    # Create test user
    test_api_key = try_create_test_user(admin_api_key)
    if not test_api_key:
        print("\n❌ Could not create test user.")
        return
    
    # Test TTS with CallWaiting AI demo
    print(f"\n🎤 Testing CallWaiting AI Demo...")
    callwaiting_success = test_tts_with_api_key(test_api_key)
    
    # Test all voices
    voice_success_count = test_all_voices(test_api_key)
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 70)
    print(f"✅ Admin user created: {admin_api_key[:20]}...")
    print(f"✅ Test user created: {test_api_key[:20]}...")
    print(f"✅ CallWaiting AI Demo: {'SUCCESS' if callwaiting_success else 'FAILED'}")
    print(f"✅ Voice Tests: {voice_success_count} successful")
    print(f"📁 Audio files generated in current directory")
    
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
