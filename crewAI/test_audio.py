#!/usr/bin/env python3
"""
Audio Test for ElevenLabs Integration
Tests basic text-to-speech functionality
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_elevenlabs():
    """Test ElevenLabs basic functionality"""
    print("🧪 Testing ElevenLabs Audio Integration")
    print("="*50)
    
    # Check import
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play
        print("✅ ElevenLabs imported successfully")
    except ImportError as e:
        print(f"❌ ElevenLabs import failed: {e}")
        return False
    
    # Check API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or api_key == "your_elevenlabs_api_key_here":
        print("❌ ElevenLabs API key not configured")
        print("🔑 Please add your API key to .env file")
        print("📝 Get API key from: https://elevenlabs.io/app/settings/api-keys")
        return False
    
    print("✅ ElevenLabs API key found")
    
    # Test client initialization
    try:
        client = ElevenLabs(api_key=api_key)
        print("✅ ElevenLabs client initialized")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
    
    # Test basic text-to-speech (only if API key is valid)
    if api_key != "your_elevenlabs_api_key_here":
        try:
            print("🎙️ Testing text-to-speech...")
            audio = client.text_to_speech.convert(
                text="Hello! This is a test of the ElevenLabs audio integration for our AI debate system.",
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            print("✅ Audio generated successfully")
            
            # Try to play audio
            print("🔊 Playing test audio...")
            play(audio)
            print("✅ Audio playback successful")
            
        except Exception as e:
            print(f"❌ Audio generation/playback failed: {e}")
            print("💡 This might be due to invalid API key or network issues")
            return False
    
    print("\n🎉 ElevenLabs integration test complete!")
    print("🎭 Your audio debate system is ready to use!")
    return True

def show_usage():
    """Show usage examples"""
    print("\n🎙️ Audio Debate System Usage:")
    print("="*40)
    print("Basic usage:")
    print("  python audio_debate_system.py 'AI will replace human jobs'")
    print("")
    print("Conversational mode:")
    print("  python audio_debate_system.py 'Remote work vs office' --mode conversation")
    print("")
    print("Mixed mode (research + audio):")
    print("  python audio_debate_system.py 'Climate change' --mode mixed")
    print("")
    print("Voice options:")
    print("  🎭 Pro Debater: Rachel (confident female)")
    print("  🎭 Con Debater: Domi (analytical male)")
    print("  ⚖️ Judge: Bella (authoritative neutral)")
    print("  🔬 Researcher: Antoni (informative)")

if __name__ == "__main__":
    test_success = test_elevenlabs()
    
    if test_success:
        show_usage()
    else:
        print("\n❌ Audio setup incomplete")
        print("📝 Please configure your ElevenLabs API key in .env file")
