#!/usr/bin/env python3
"""Test ODIADEV TTS using local MiniMax client."""

import os
import sys
import base64
from datetime import datetime

# Add src directory to path
sys.path.append('src')

try:
    from minimax_client import MinimaxClient
except ImportError:
    print("❌ Could not import MinimaxClient. Make sure you're in the project directory.")
    sys.exit(1)

# CallWaiting AI script
CALLWAITING_SCRIPT = """Imagine waking up to realize every missed call might be costing you $500 or more. Callwaiting AI is here to change that. For just $80 each month, this intelligent agent answers your calls, books appointments, and sends payment links and updates you on whatsapp and email—even while you sleep. Never miss a valuable opportunity again. Start now and experience the peace of knowing your business is always moving forward, effortlessly handled by Callwaiting AI."""

def test_local_tts():
    """Test TTS using local MiniMax client."""
    print("🎤 Testing TTS with local MiniMax client...")
    
    try:
        # Initialize MiniMax client
        client = MinimaxClient()
        
        # Generate TTS with Marcus voice (american-male)
        print("   - Using Marcus voice (american-male)...")
        result = client.text_to_speech(
            text=CALLWAITING_SCRIPT,
            voice_id="moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc",  # Marcus American Male
            model="speech-02-hd",
            speed=1.0,
            pitch=0,
            emotion="neutral"
        )
        
        print("✅ CallWaiting AI demo generated successfully!")
        print(f"   - Duration: {result.get('duration_seconds', 'N/A')} seconds")
        print(f"   - Sample Rate: {result.get('sample_rate', 'N/A')} Hz")
        
        # Save audio file
        if 'audio_base64' in result:
            audio_data = base64.b64decode(result['audio_base64'])
            filename = f"callwaiting_marcus_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            with open(filename, 'wb') as f:
                f.write(audio_data)
            print(f"   - Audio saved: {filename}")
            return True
        else:
            print("❌ No audio data in result")
            return False
            
    except Exception as e:
        print(f"❌ Local client failed: {e}")
        return False

def test_all_voices():
    """Test all verified voices."""
    print("\n🎭 Testing all verified voices...")
    
    voices = [
        {
            "name": "American Female",
            "voice_id": "moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a",
            "text": "Hello! I am the American female voice from ODIADEV AI TTS. I provide clear, professional speech for business communications and customer service."
        },
        {
            "name": "Marcus American Male",
            "voice_id": "moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc",
            "text": "Greetings! I am Marcus, the American male voice from ODIADEV AI TTS. I deliver confident, authoritative speech for corporate communications and technical documentation."
        },
        {
            "name": "Ezinne Nigerian Female",
            "voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
            "text": "Hello! I am Ezinne, the Nigerian female voice from ODIADEV AI TTS. I bring the warmth and authenticity of Nigerian culture to professional communications."
        },
        {
            "name": "Odia Nigerian Male",
            "voice_id": "moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc",
            "text": "Greetings! I am Odia, the Nigerian male voice from ODIADEV AI TTS. I represent strength and confidence in business and leadership across Africa and internationally."
        }
    ]
    
    successful_generations = 0
    
    try:
        client = MinimaxClient()
        
        for voice in voices:
            print(f"\n🎤 Generating {voice['name']}...")
            
            try:
                result = client.text_to_speech(
                    text=voice['text'],
                    voice_id=voice['voice_id'],
                    model="speech-02-hd",
                    speed=1.0,
                    pitch=0,
                    emotion="neutral"
                )
                
                if 'audio_base64' in result:
                    audio_data = base64.b64decode(result['audio_base64'])
                    filename = f"verified_{voice['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.mp3"
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    print(f"✅ {voice['name']} generated: {filename}")
                    successful_generations += 1
                else:
                    print(f"❌ {voice['name']} failed: No audio data")
                    
            except Exception as e:
                print(f"❌ {voice['name']} failed: {e}")
        
        return successful_generations
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return 0

def main():
    """Main function."""
    print("🎯 ODIADEV TTS - Local Testing")
    print("=" * 60)
    print("Testing TTS using local MiniMax client...")
    print(f"Script: {CALLWAITING_SCRIPT[:100]}...")
    print()
    
    # Test CallWaiting demo with Marcus voice
    print(f"🎤 Generating CallWaiting AI demo...")
    callwaiting_success = test_local_tts()
    
    # Test all voices
    successful_voices = test_all_voices()
    
    print(f"\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"✅ CallWaiting AI demo: {'SUCCESS' if callwaiting_success else 'FAILED'}")
    print(f"✅ Successful voice generations: {successful_voices}/4")
    print(f"📁 Audio files generated in current directory")
    
    if callwaiting_success and successful_voices > 0:
        print(f"\n🎉 SUCCESS! ODIADEV AI TTS voices are working!")
        print(f"✅ CallWaiting AI demo generated with Marcus voice!")
        print(f"✅ {successful_voices} verified voices working!")
        print(f"🚀 Ready for production use!")
        print(f"🌐 Service URL: https://minimax-tts-odiadev.onrender.com")
    else:
        print(f"\n❌ Some generations failed")
        if not callwaiting_success:
            print(f"   - CallWaiting AI demo failed")
        if successful_voices == 0:
            print(f"   - No voices working")

if __name__ == "__main__":
    main()
