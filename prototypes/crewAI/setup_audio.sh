#!/bin/bash

# Audio-Enhanced AI Debate System Setup
echo "🎙️ Audio-Enhanced AI Debate System Setup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "debate_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run the regular setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source debate_env/bin/activate

# Install ElevenLabs
echo "🔊 Installing ElevenLabs..."
pip install elevenlabs

# Check for API keys
echo ""
echo "🔑 Checking API keys..."

if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found. Creating template..."
    cat > .env << EOF
MISTRAL_API_KEY=your_mistral_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
EOF
    echo "📝 Please edit .env with your API keys"
else
    echo "✅ .env file found"
fi

# Test audio capabilities
echo ""
echo "🧪 Testing audio capabilities..."
python -c "
try:
    from elevenlabs.client import ElevenLabs
    print('✅ ElevenLabs imported successfully')
    import os
    from dotenv import load_dotenv
    load_dotenv()
    if os.getenv('ELEVENLABS_API_KEY'):
        print('✅ ElevenLabs API key found')
    else:
        print('⚠️ ElevenLabs API key not found in .env')
except ImportError:
    print('❌ ElevenLabs import failed')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "🎭 Audio Debate System Ready!"
echo "Usage examples:"
echo "  python audio_debate_system.py 'AI will replace human jobs'"
echo "  python audio_debate_system.py 'Remote work vs office work' --mode conversation"
echo "  python audio_debate_system.py 'Climate change solutions' --mode mixed"
echo ""
echo "📚 See AUDIO_README.md for full documentation"
