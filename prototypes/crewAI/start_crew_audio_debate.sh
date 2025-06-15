#!/bin/bash

# CrewAI Audio Debate System Launcher
# Launches the debate system with specialized audio agents

echo "🎙️ CrewAI Audio Debate System"
echo "👥 Launching with specialized audio production agents..."
echo "================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ Virtual environment not detected"
    echo "💡 Activating debate_env..."
    source debate_env/bin/activate
fi

# Check for required environment variables
if [[ -z "$ELEVENLABS_API_KEY" ]]; then
    echo "⚠️ ELEVENLABS_API_KEY not found in environment"
    echo "💡 Loading from .env file..."
fi

if [[ -z "$MISTRAL_API_KEY" ]]; then
    echo "⚠️ MISTRAL_API_KEY not found in environment"
    echo "💡 Loading from .env file..."
fi

# Run the CrewAI audio debate system
echo "🚀 Starting CrewAI Audio Debate System..."
python crew_audio_debate_system.py "$@"
