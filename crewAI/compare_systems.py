#!/usr/bin/env python3
"""
Audio vs Text Debate System Comparison
Shows the enhancements made with ElevenLabs audio integration
"""

import os
import json
from datetime import datetime

def compare_systems():
    """Compare original text system with audio-enhanced system"""
    
    print("🎭 DEBATE SYSTEM COMPARISON")
    print("="*60)
    
    print("\n📊 FEATURE COMPARISON:")
    print("-"*40)
    
    features = [
        ("Text-based Arguments", "✅", "✅"),
        ("Research Agents", "✅", "✅"),
        ("Shared Memory", "✅", "✅"),
        ("JSON Logging", "✅", "✅"),
        ("🎙️ Text-to-Speech", "❌", "✅"),
        ("🎭 Voice Personalities", "❌", "✅"),
        ("🎬 Conversational Mode", "❌", "✅"),
        ("🎵 Audio File Saving", "❌", "✅"),
        ("🔊 Real-time Playback", "❌", "✅"),
        ("📱 Multiple Audio Modes", "❌", "✅")
    ]
    
    print(f"{'Feature':<25} {'Original':<10} {'Audio Enhanced':<15}")
    print("-"*50)
    for feature, original, enhanced in features:
        print(f"{feature:<25} {original:<10} {enhanced:<15}")
    
    print("\n🎙️ AUDIO MODES AVAILABLE:")
    print("-"*40)
    modes = [
        ("individual", "Each agent speaks their argument separately"),
        ("conversation", "Real-time conversational debate format"),
        ("mixed", "Research + individual audio arguments")
    ]
    
    for mode, description in modes:
        print(f"🎭 {mode.upper():<12}: {description}")
    
    print("\n🎬 VOICE PERSONALITIES:")
    print("-"*40)
    voices = [
        ("Pro Debater", "Rachel", "Confident and persuasive female voice"),
        ("Con Debater", "Domi", "Analytical and critical male voice"),
        ("Judge", "Bella", "Balanced and authoritative neutral voice"),
        ("Researcher", "Antoni", "Informative and clear delivery")
    ]
    
    for role, name, style in voices:
        print(f"🎭 {role:<12}: {name:<8} - {style}")
    
    print("\n📁 OUTPUT COMPARISON:")
    print("-"*40)
    print("Original System Output:")
    print("  📄 debate_log_YYYYMMDD_HHMMSS.json")
    print("  📊 Text-based shared memory")
    print("  📋 Final judgment text")
    
    print("\nAudio-Enhanced System Output:")
    print("  📄 audio_debate_log_YYYYMMDD_HHMMSS.json")
    print("  📊 Enhanced shared memory with audio metadata")
    print("  📋 Final judgment text")
    print("  🎵 audio_debate_YYYYMMDD_HHMMSS/")
    print("    ├── pro_argument_HHMMSS.mp3")
    print("    ├── con_argument_HHMMSS.mp3")
    print("    ├── judge_evaluation_HHMMSS.mp3")
    print("    └── full_dialogue.mp3 (conversation mode)")
    
    print("\n🚀 USAGE EXAMPLES:")
    print("-"*40)
    
    print("Original System:")
    print("  python debate_system.py 'Topic here'")
    print("  ./start_debate.sh")
    
    print("\nAudio-Enhanced System:")
    print("  python audio_debate_system.py 'Topic here'")
    print("  python audio_debate_system.py 'Topic' --mode conversation")
    print("  python audio_debate_system.py 'Topic' --mode mixed")
    print("  python audio_debate_system.py 'Topic' --no-playback")
    
    print("\n🎯 BEST USE CASES:")
    print("-"*40)
    print("Original System:")
    print("  ✅ Quick text-based analysis")
    print("  ✅ Research documentation")
    print("  ✅ Silent operation")
    print("  ✅ Faster execution")
    
    print("\nAudio-Enhanced System:")
    print("  ✅ Presentations and demos")
    print("  ✅ Educational content")
    print("  ✅ Accessibility (audio learners)")
    print("  ✅ Immersive experience")
    print("  ✅ Real-time debate simulation")
    print("  ✅ Podcast-style content creation")

def analyze_recent_logs():
    """Analyze recent debate logs to show differences"""
    print("\n📋 RECENT DEBATE LOGS:")
    print("-"*40)
    
    # Find text logs
    text_logs = [f for f in os.listdir('.') if f.startswith('debate_log_') and f.endswith('.json')]
    audio_logs = [f for f in os.listdir('.') if f.startswith('audio_debate_log_') and f.endswith('.json')]
    
    print(f"📄 Text-based logs: {len(text_logs)}")
    for log in sorted(text_logs, reverse=True)[:3]:
        try:
            mtime = os.path.getmtime(log)
            formatted_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"   {log} ({formatted_time})")
        except:
            print(f"   {log}")
    
    print(f"\n🎙️ Audio-enhanced logs: {len(audio_logs)}")
    for log in sorted(audio_logs, reverse=True)[:3]:
        try:
            mtime = os.path.getmtime(log)
            formatted_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"   {log} ({formatted_time})")
        except:
            print(f"   {log}")
    
    # Find audio directories
    audio_dirs = [d for d in os.listdir('.') if d.startswith('audio_debate_') and os.path.isdir(d)]
    print(f"\n🎵 Audio directories: {len(audio_dirs)}")
    for audio_dir in sorted(audio_dirs, reverse=True)[:3]:
        try:
            audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
            print(f"   {audio_dir}/ ({len(audio_files)} audio files)")
        except:
            print(f"   {audio_dir}/")

def show_setup_requirements():
    """Show setup requirements for audio system"""
    print("\n🔧 SETUP REQUIREMENTS:")
    print("-"*40)
    
    print("Original System:")
    print("  ✅ Python 3.12+")
    print("  ✅ crewai, mistralai")
    print("  ✅ MISTRAL_API_KEY")
    
    print("\nAudio-Enhanced System:")
    print("  ✅ Python 3.12+")
    print("  ✅ crewai, mistralai, elevenlabs")
    print("  ✅ MISTRAL_API_KEY")
    print("  ✅ ELEVENLABS_API_KEY")
    print("  ✅ Audio playback system (speakers/headphones)")
    print("  ✅ FFmpeg (for audio processing)")
    
    print("\n📦 INSTALLATION:")
    print("-"*40)
    print("pip install elevenlabs")
    print("# Add ELEVENLABS_API_KEY to .env file")
    print("# Get API key from: https://elevenlabs.io/app/settings/api-keys")

if __name__ == "__main__":
    compare_systems()
    analyze_recent_logs()
    show_setup_requirements()
    
    print("\n" + "="*60)
    print("🎉 AUDIO DEBATE SYSTEM READY!")
    print("🎙️ Experience the future of AI debates with voice!")
    print("="*60)
