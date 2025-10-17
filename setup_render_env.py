#!/usr/bin/env python3
"""Setup Render environment variables with API keys."""

import json
import secrets
import string
from datetime import datetime

def generate_api_key():
    """Generate a secure API key."""
    # Generate a 32-character random string
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def generate_render_env_vars():
    """Generate environment variables for Render."""
    print("🔑 Generating API keys for Render environment variables...")
    
    # Generate 10 API keys
    api_keys = []
    for i in range(1, 11):
        api_key = generate_api_key()
        api_keys.append({
            "name": f"API_KEY_{i}",
            "value": api_key,
            "description": f"ODIADEV TTS API Key {i} for testing"
        })
        print(f"✅ Generated API_KEY_{i}: {api_key[:8]}...")
    
    return api_keys

def create_render_env_file(api_keys):
    """Create environment variables file for Render."""
    print("\n📝 Creating Render environment variables file...")
    
    env_content = f"""# ODIADEV TTS - Render Environment Variables
# Generated on: {datetime.now().isoformat()}
# These should be set in Render dashboard under Environment Variables

# MiniMax API Configuration
MINIMAX_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw
MINIMAX_GROUP_ID=1933510987994895143
MINIMAX_MODEL=speech-02-hd

# Authentication Configuration
ENFORCE_AUTH=false
ADMIN_API_KEY={api_keys[0]['value']}

# Generated API Keys for Testing
"""
    
    # Add all API keys
    for key_data in api_keys:
        env_content += f"{key_data['name']}={key_data['value']}\n"
    
    # Add additional configuration
    env_content += """
# Database Configuration
DATABASE_URL=sqlite:///./odiadev_tts.db

# Service Configuration
SERVICE_NAME=ODIADEV AI TTS
SERVICE_VERSION=1.0.0
SERVICE_DESCRIPTION=Production-ready TTS service with verified voice characteristics

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=10

# Voice Configuration
DEFAULT_VOICE=american-male
DEFAULT_SPEED=1.0
DEFAULT_PITCH=0
DEFAULT_EMOTION=neutral
"""
    
    with open('render.env', 'w') as f:
        f.write(env_content)
    print("✅ Created render.env file")
    
    return env_content

def create_render_yaml(api_keys):
    """Create render.yaml with environment variables."""
    print("\n📝 Creating render.yaml with environment variables...")
    
    yaml_content = f"""services:
  - type: web
    name: odiadev-ai-tts
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m src.main
    envVars:
      - key: MINIMAX_API_KEY
        value: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw
      - key: MINIMAX_GROUP_ID
        value: "1933510987994895143"
      - key: MINIMAX_MODEL
        value: speech-02-hd
      - key: ENFORCE_AUTH
        value: "false"
      - key: ADMIN_API_KEY
        value: {api_keys[0]['value']}
      - key: API_KEY_1
        value: {api_keys[0]['value']}
      - key: API_KEY_2
        value: {api_keys[1]['value']}
      - key: API_KEY_3
        value: {api_keys[2]['value']}
      - key: API_KEY_4
        value: {api_keys[3]['value']}
      - key: API_KEY_5
        value: {api_keys[4]['value']}
      - key: API_KEY_6
        value: {api_keys[5]['value']}
      - key: API_KEY_7
        value: {api_keys[6]['value']}
      - key: API_KEY_8
        value: {api_keys[7]['value']}
      - key: API_KEY_9
        value: {api_keys[8]['value']}
      - key: API_KEY_10
        value: {api_keys[9]['value']}
      - key: SERVICE_NAME
        value: "ODIADEV AI TTS"
      - key: SERVICE_VERSION
        value: "1.0.0"
      - key: LOG_LEVEL
        value: INFO
      - key: RATE_LIMIT_PER_MINUTE
        value: "60"
      - key: DEFAULT_VOICE
        value: american-male
      - key: DEFAULT_SPEED
        value: "1.0"
      - key: DEFAULT_PITCH
        value: "0"
      - key: DEFAULT_EMOTION
        value: neutral
"""
    
    with open('render.yaml', 'w') as f:
        f.write(yaml_content)
    print("✅ Created render.yaml file")

def create_test_script(api_keys):
    """Create test script for the API keys."""
    print("\n📝 Creating test script...")
    
    script_content = f'''#!/usr/bin/env python3
"""Test ODIADEV TTS with environment API keys."""

import requests
import json
import base64
import os
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

# API keys from environment variables
API_KEYS = [
'''
    
    for key_data in api_keys:
        script_content += f'    "{key_data["value"]}",\n'
    
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
    print("🎯 ODIADEV TTS - Environment API Key Testing")
    print("=" * 60)
    print(f"Testing {len(API_KEYS)} API keys from environment variables...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    successful_tests = 0
    
    for i, api_key in enumerate(API_KEYS, 1):
        print(f"\\n--- API KEY {i}/{len(API_KEYS)} ---")
        if test_tts_with_key(api_key, i):
            successful_tests += 1
    
    print(f"\\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"✅ Successful tests: {successful_tests}/{len(API_KEYS)}")
    print(f"❌ Failed tests: {len(API_KEYS) - successful_tests}/{len(API_KEYS)}")
    
    if successful_tests > 0:
        print(f"\\n🎉 SUCCESS! ODIADEV TTS is working!")
        print(f"Generated {successful_tests} CallWaiting AI demos with Marcus voice!")
        print(f"Service URL: {API_BASE_URL}")
    else:
        print(f"\\n❌ No successful tests")

if __name__ == "__main__":
    main()
'''
    
    with open('test_env_api_keys.py', 'w') as f:
        f.write(script_content)
    print("✅ Created test_env_api_keys.py")

def main():
    """Main function."""
    print("🎯 ODIADEV TTS - Render Environment Setup")
    print("=" * 60)
    print("Setting up API keys as Render environment variables...")
    print()
    
    # Generate API keys
    api_keys = generate_render_env_vars()
    
    # Create environment files
    create_render_env_file(api_keys)
    create_render_yaml(api_keys)
    create_test_script(api_keys)
    
    print(f"\\n📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Generated {len(api_keys)} API keys")
    print(f"✅ Created render.env file")
    print(f"✅ Created render.yaml file")
    print(f"✅ Created test script")
    print(f"\\n🎉 Ready to deploy to Render!")
    print(f"\\nNext steps:")
    print(f"1. git add .")
    print(f"2. git commit -m 'Add Render environment variables'")
    print(f"3. git push origin main")
    print(f"4. Render will automatically deploy with the new environment variables")
    print(f"5. Test with: python3 test_env_api_keys.py")

if __name__ == "__main__":
    main()
