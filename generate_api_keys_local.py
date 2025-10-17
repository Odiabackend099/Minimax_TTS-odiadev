#!/usr/bin/env python3
"""Generate API keys locally and save them for Render deployment."""

import json
import secrets
import string
from datetime import datetime

def generate_api_key():
    """Generate a secure API key."""
    # Generate a 32-character random string
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def generate_api_keys(count=10):
    """Generate multiple API keys."""
    print(f"🔑 Generating {count} API keys...")
    
    api_keys = []
    for i in range(1, count + 1):
        api_key = generate_api_key()
        api_keys.append({
            "id": i,
            "name": f"API Key {i}",
            "api_key": api_key,
            "created_at": datetime.now().isoformat(),
            "description": f"Generated API key {i} for ODIADEV TTS testing"
        })
        print(f"✅ Generated API key {i}: {api_key[:8]}...")
    
    return api_keys

def save_api_keys(api_keys):
    """Save API keys to files."""
    print("\n💾 Saving API keys...")
    
    # Save as JSON
    with open('api_keys.json', 'w') as f:
        json.dump(api_keys, f, indent=2)
    print("✅ Saved to api_keys.json")
    
    # Save as environment file
    with open('.env.api_keys', 'w') as f:
        f.write("# ODIADEV TTS API Keys\n")
        f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
        for i, key_data in enumerate(api_keys, 1):
            f.write(f"API_KEY_{i}={key_data['api_key']}\n")
    print("✅ Saved to .env.api_keys")
    
    # Save as individual files
    for key_data in api_keys:
        filename = f"api_key_{key_data['id']}.txt"
        with open(filename, 'w') as f:
            f.write(f"# {key_data['name']}\n")
            f.write(f"# Generated: {key_data['created_at']}\n")
            f.write(f"# Description: {key_data['description']}\n\n")
            f.write(f"API_KEY={key_data['api_key']}\n")
        print(f"✅ Saved to {filename}")

def create_test_script(api_keys):
    """Create a test script using the generated API keys."""
    print("\n📝 Creating test script...")
    
    script_content = '''#!/usr/bin/env python3
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
'''
    
    for key_data in api_keys:
        script_content += f'    "{key_data["api_key"]}",\n'
    
    script_content += ''']

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
        print(f"\\n--- API KEY {i}/{len(API_KEYS)} ---")
        if test_tts_with_key(api_key, i):
            successful_tests += 1
    
    print(f"\\n📊 FINAL RESULTS")
    print("=" * 50)
    print(f"✅ Successful tests: {successful_tests}/{len(API_KEYS)}")
    print(f"❌ Failed tests: {len(API_KEYS) - successful_tests}/{len(API_KEYS)}")
    
    if successful_tests > 0:
        print(f"\\n🎉 SUCCESS! ODIADEV TTS is working!")
        print(f"Generated {successful_tests} CallWaiting AI demos!")
    else:
        print(f"\\n❌ No successful tests")

if __name__ == "__main__":
    main()
'''
    
    with open('test_api_keys.py', 'w') as f:
        f.write(script_content)
    print("✅ Created test_api_keys.py")

def main():
    """Main function."""
    print("🎯 ODIADEV TTS - API Key Generator")
    print("=" * 50)
    print("Generating API keys for local testing and Render deployment...")
    print()
    
    # Generate API keys
    api_keys = generate_api_keys(10)
    
    # Save API keys
    save_api_keys(api_keys)
    
    # Create test script
    create_test_script(api_keys)
    
    print(f"\\n📊 SUMMARY")
    print("=" * 50)
    print(f"✅ Generated {len(api_keys)} API keys")
    print(f"✅ Saved to multiple formats")
    print(f"✅ Created test script")
    print(f"\\n🎉 Ready to push to Git and deploy to Render!")
    print(f"\\nNext steps:")
    print(f"1. git add .")
    print(f"2. git commit -m 'Add API keys for testing'")
    print(f"3. git push origin main")
    print(f"4. Test with: python3 test_api_keys.py")

if __name__ == "__main__":
    main()
