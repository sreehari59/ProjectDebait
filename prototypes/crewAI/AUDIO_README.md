# Audio-Enhanced AI Debate System

This enhanced version adds ElevenLabs audio capabilities to create a real-time conversational debate experience.

## Features Added

### 🎙️ Audio Capabilities
- **Text-to-Speech**: Each agent speaks their arguments aloud
- **Text-to-Dialogue**: Real-time conversational debate format
- **Voice Personalities**: Distinct voices for each debater
- **Audio Logging**: Save audio files alongside debate logs

### 🎭 Enhanced Agents
- **Pro Debater**: Male authoritative voice
- **Con Debater**: Female analytical voice  
- **Judge**: Neutral professional voice
- **Research Agents**: Background information gathering

## Setup Requirements

### ElevenLabs API
1. Create account at [elevenlabs.io](https://elevenlabs.io)
2. Get API key from dashboard
3. Add to `.env` file:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

### Installation
```bash
pip install elevenlabs python-dotenv
```

## Usage Options

### Option 1: Audio-Enhanced Individual Arguments
```bash
python audio_debate_system.py "Topic here" --mode individual
```

### Option 2: Real-time Conversational Debate
```bash
python audio_debate_system.py "Topic here" --mode conversation
```

### Option 3: Mixed Mode (Research + Audio Debate)
```bash
python audio_debate_system.py "Topic here" --mode mixed
```

## Voice Configurations

### Pre-configured Voices
- **Pro Debater**: Authoritative male voice
- **Con Debater**: Analytical female voice
- **Judge**: Professional neutral voice

### Custom Voice Setup
You can customize voices by modifying the `VOICE_CONFIG` in the script.

## Audio Output
- Individual MP3 files for each argument
- Combined dialogue audio for conversational mode
- Audio logs saved with timestamps
- Real-time playback during debate

## Example Commands

```bash
# Quick audio debate
python audio_debate_system.py "AI will replace human jobs"

# Conversational format
python audio_debate_system.py "Remote work is better than office work" --mode conversation

# Save audio files only (no playback)
python audio_debate_system.py "Climate change solutions" --save-audio --no-playback
```
