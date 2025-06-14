# CrewAI Debate System

An AI-powered debate system built with CrewAI and Mistral API, featuring both text-based and audio-enhanced debate capabilities.

## 🎭 Features

### Core Debate System (`debate_system.py`)
- **3 AI Agents**: Pro Debater, Con Debater, and Judge
- **Simplified Workflow**: Direct arguments without research phase
- **Shared Memory**: Context preservation across debate phases
- **JSON Logging**: Complete debate session recording
- **Multi-Agent Coordination**: Powered by CrewAI framework

### Audio-Enhanced System (`audio_debate_system.py`)
- **🎙️ Text-to-Speech**: Arguments spoken with distinct voices
- **🎭 Voice Personalities**: Unique voices for each debater
- **🎬 Conversational Mode**: Real-time dialogue format
- **🎵 Audio Logging**: MP3 files saved alongside text
- **📱 Multiple Modes**: Individual, conversation, and mixed formats

## 🚀 Quick Start

### Prerequisites
1. Python 3.12+
2. Mistral API key from [mistral.ai](https://mistral.ai)
3. (Optional) ElevenLabs API key from [elevenlabs.io](https://elevenlabs.io) for audio features

### Installation

1. **Clone and Setup**:
   ```bash
   # Navigate to crewAI folder
   cd crewAI
   
   # Create virtual environment
   python -m venv debate_env
   source debate_env/bin/activate  # On Windows: debate_env\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   Create a `.env` file:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here  # Optional for audio
   ```

3. **Run Text-Based Debate**:
   ```bash
   python debate_system.py "Is artificial intelligence good for humanity?"
   
   # Or use the startup script
   ./start_debate.sh
   ```

4. **Run Audio-Enhanced Debate**:
   ```bash
   # Install audio dependencies first
   ./setup_audio.sh
   
   # Run audio debate
   python audio_debate_system.py "Remote work vs office work"
   
   # Conversational mode
   python audio_debate_system.py "Climate change solutions" --mode conversation
   ```

## 📁 File Structure

```
crewAI/
├── debate_system.py          # Main text-based debate system
├── audio_debate_system.py    # Audio-enhanced debate system  
├── analyze_debate_log.py     # Debate log analysis tool
├── compare_systems.py        # System comparison utility
├── test_audio.py            # Audio functionality tester
├── requirements.txt         # Python dependencies
├── start_debate.sh          # Quick start script
├── setup_audio.sh           # Audio setup script
├── AUDIO_README.md          # Audio system documentation
└── README.md               # This file
```

## 🎯 Usage Examples

### Text-Based Debates
```bash
# Quick debate
python debate_system.py "Should AI replace human teachers?"

# Interactive mode
python debate_system.py
# Enter topic when prompted
```

### Audio-Enhanced Debates
```bash
# Individual agent speeches
python audio_debate_system.py "Space exploration priority" --mode individual

# Real-time conversation
python audio_debate_system.py "Universal basic income" --mode conversation

# Mixed mode (research + audio)
python audio_debate_system.py "Renewable energy transition" --mode mixed
```

### Analysis Tools
```bash
# Analyze latest debate log
python analyze_debate_log.py

# Compare system capabilities
python compare_systems.py

# Test audio setup
python test_audio.py
```

## 🏗️ System Architecture

### Core Components
1. **DebatingSystem Class**: Main orchestrator
2. **CrewAI Framework**: Multi-agent coordination
3. **Mistral LLM**: Language model for arguments
4. **Shared Memory**: Context preservation
5. **JSON Logging**: Session recording

### Audio Components (Optional)
1. **ElevenLabs Integration**: Text-to-speech conversion
2. **Voice Personalities**: Distinct voices per agent
3. **Audio Modes**: Individual vs conversational
4. **MP3 Generation**: Audio file creation

### Agent Workflow
```
Pro Debater → Con Debater → Judge
     ↓             ↓         ↓
  Arguments → Rebuttals → Evaluation
     ↓             ↓         ↓
  Shared Memory ←─────────────┘
```

## 🎙️ Voice Configuration

The audio system uses pre-configured ElevenLabs voices:

- **Pro Debater**: Rachel (confident female voice)
- **Con Debater**: Domi (analytical male voice)  
- **Judge**: Bella (authoritative neutral voice)
- **Researcher**: Antoni (informative delivery)

## 📊 Output Files

### Text System
- `debate_log_YYYYMMDD_HHMMSS.json`: Complete debate session
- Shared memory with captured arguments and evaluation

### Audio System  
- `audio_debate_log_YYYYMMDD_HHMMSS.json`: Enhanced session log
- `audio_debate_YYYYMMDD_HHMMSS/`: Audio files directory
  - `pro_argument_HHMMSS.mp3`
  - `con_argument_HHMMSS.mp3` 
  - `judge_evaluation_HHMMSS.mp3`
  - `full_dialogue.mp3` (conversation mode)

## 🔧 Configuration

### Environment Variables
```env
MISTRAL_API_KEY=required_for_all_functionality
ELEVENLABS_API_KEY=optional_for_audio_features
```

### Customization
- Modify agent personalities in `create_agents()` method
- Adjust task descriptions in `create_tasks()` method
- Configure voice settings in `VOICE_CONFIG` (audio system)
- Update debate phases in `run_debate()` method

## 🐛 Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure `.env` file is configured correctly
2. **Audio Issues**: Run `python test_audio.py` to verify setup
3. **Import Errors**: Check virtual environment activation
4. **Permission Errors**: Ensure scripts are executable (`chmod +x *.sh`)

### Debug Tools
```bash
# Test basic functionality
python -c "from debate_system import DebatingSystem; print('✅ Import successful')"

# Test audio setup
python test_audio.py

# Validate syntax
python -m py_compile debate_system.py
```

## 📚 API Reference

### Main Classes
- `DebatingSystem`: Core debate orchestrator
- `AudioDebateSystem`: Audio-enhanced version

### Key Methods
- `run_debate(topic)`: Execute complete debate
- `create_agents()`: Initialize AI agents
- `create_tasks()`: Define debate tasks
- `capture_task_output()`: Store results in shared memory
- `save_debate_log()`: Export session data

## 🤝 Contributing

This system is designed to be modular and extensible. Key areas for enhancement:

1. **New Agent Types**: Add specialized roles (fact-checker, moderator)
2. **Enhanced Memory**: Implement persistent knowledge base
3. **Multi-Language**: Add support for non-English debates
4. **Real-time UI**: Web interface for live debates
5. **Advanced Analytics**: Sentiment analysis, argument mapping

## 📄 License

This project is part of the ProjectDebait repository. Please refer to the main repository license.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent framework
- **Mistral AI**: Language model provider
- **ElevenLabs**: Text-to-speech technology
- **ProjectDebait Team**: Collaborative development

---

For questions or issues, please refer to the main ProjectDebait repository or create an issue in the GitHub project.
