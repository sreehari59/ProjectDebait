from langgraph_for_api import LangGraphDebateSystem, DebateState
from flask import Flask, Response, request, jsonify
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
import os

load_dotenv()
app = Flask(__name__)
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Voice IDs for different speakers
VOICES = {
    "side_a": "JBFqnCBsd6RMkjVDRZzb",  # Josh
    "side_b": "ThT5KcBeYPX3keUQqHPh",   # Arnold
    "judge": "VR6AewLTigWG4xSOukaG",    # Rachel
    "narrator": "ErXwobaYiN019PkySvjV"   # Bella
}

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; margin-bottom: 5px; }
                .form-group input, .form-group textarea { width: 100%; padding: 8px; }
                .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .side-a { background-color: #e3f2fd; }
                .side-b { background-color: #ffebee; }
                .judge { background-color: #f5f5f5; }
                .narrator { background-color: #f0f4c3; }
                #transcript { margin: 20px 0; }
                .controls { margin: 20px 0; }
                button { padding: 10px 20px; margin-right: 10px; }
            </style>
        </head>
        <body>
            <h1>AI Debate System</h1>
            <form id="debateForm">
                <div class="form-group">
                    <label for="topic">Debate Topic:</label>
                    <input type="text" id="topic" value="cats vs dogs" required>
                </div>
                <div class="form-group">
                    <label for="side_a_point">Side A Point:</label>
                    <input type="text" id="side_a_point" value="cats are better pets" required>
                </div>
                <div class="form-group">
                    <label for="side_b_point">Side B Point:</label>
                    <input type="text" id="side_b_point" value="dogs are better pets" required>
                </div>
                <div class="form-group">
                    <label for="rounds">Number of Rounds:</label>
                    <input type="number" id="rounds" value="2" min="1" max="5" required>
                </div>
                <button type="submit">Start Debate</button>
            </form>

            <div id="transcript"></div>
            <audio id="audio" controls style="width: 100%; margin-top: 20px;"></audio>

            <script>
                let currentMessageIndex = 0;
                let debateMessages = [];
                let isPlaying = false;

                document.getElementById('debateForm').onsubmit = async (e) => {
                    e.preventDefault();
                    const form = e.target;
                    const transcript = document.getElementById('transcript');
                    transcript.innerHTML = '';
                    currentMessageIndex = 0;

                    // Get debate parameters
                    const params = {
                        topic: form.topic.value,
                        side_a_point: form.side_a_point.value,
                        side_b_point: form.side_b_point.value,
                        rounds: form.rounds.value
                    };

                    // Start the debate
                    const response = await fetch('/start_debate?' + new URLSearchParams(params));
                    const result = await response.json();
                    debateMessages = result.messages;

                    // Start playing
                    playNextMessage();
                };

                async function playNextMessage() {
                    if (currentMessageIndex >= debateMessages.length) {
                        return;
                    }

                    const message = debateMessages[currentMessageIndex];
                    const transcript = document.getElementById('transcript');
                    const audio = document.getElementById('audio');

                    // Add message to transcript
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${getSpeakerClass(message)}`;
                    messageDiv.textContent = `${getSpeakerEmoji(message)} ${message}`;
                    transcript.appendChild(messageDiv);
                    transcript.scrollTop = transcript.scrollHeight;

                    // Play audio
                    audio.src = `/stream_message?message=${encodeURIComponent(message)}`;
                    await audio.play();

                    audio.onended = () => {
                        currentMessageIndex++;
                        setTimeout(playNextMessage, 500);  // Add small pause between messages
                    };
                }

                function getSpeakerClass(message) {
                    if (message.startsWith('side_a:')) return 'side-a';
                    if (message.startsWith('side_b:')) return 'side-b';
                    if (message.startsWith('VERDICT:')) return 'judge';
                    return 'narrator';
                }

                function getSpeakerEmoji(message) {
                    if (message.startsWith('side_a:')) return '🔵';
                    if (message.startsWith('side_b:')) return '🔴';
                    if (message.startsWith('VERDICT:')) return '⚖️';
                    return '📢';
                }
            </script>
        </body>
    </html>
    '''

@app.route('/start_debate')
def start_debate():
    topic = request.args.get('topic', 'cats vs dogs')
    side_a_point = request.args.get('side_a_point', 'cats are better pets')
    side_b_point = request.args.get('side_b_point', 'dogs are better pets')
    rounds = int(request.args.get('rounds', 2))

    # Create and run debate
    debate = LangGraphDebateSystem(
        topic=topic,
        side_a_point=side_a_point,
        side_b_point=side_b_point,
        rounds=rounds
    )

    # Initialize state
    state = DebateState(
        history=[f"Welcome to today's debate on {topic}.",
                f"Side A will argue that {side_a_point}",
                f"Side B will argue that {side_b_point}"],
        round=0,
        max_rounds=rounds
    )

    # Run debate
    final_state = debate.workflow.invoke(state)

    return jsonify({
        'messages': final_state['history']
    })

@app.route('/stream_message')
def stream_message():
    message = request.args.get('message', '')

    # Determine which voice to use based on the message prefix
    voice_id = VOICES['narrator']  # default voice
    if message.startswith('side_a:'):
        voice_id = VOICES['side_a']
        message = message[7:].strip()  # Remove prefix
    elif message.startswith('side_b:'):
        voice_id = VOICES['side_b']
        message = message[7:].strip()  # Remove prefix
    elif message.startswith('VERDICT:'):
        voice_id = VOICES['judge']
        message = message[8:].strip()  # Remove prefix

    def generate():
        audio_stream = client.text_to_speech.stream(
            text=message,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2"
        )

        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                yield chunk

    return Response(generate(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
