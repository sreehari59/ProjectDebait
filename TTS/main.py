from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream
import os

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion. What you do next is what determines the outcome.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)

# Uncomment the below code inorder to stream audio instead of converting the whole audio at once. 
# audio_stream = client.text_to_speech.stream(
#     text="This is a test",
#     voice_id="JBFqnCBsd6RMkjVDRZzb",
#     model_id="eleven_multilingual_v2"
# )

# # option 1: play the streamed audio locally
# stream(audio_stream)

# # option 2: process the audio bytes manually
# for chunk in audio_stream:
#     if isinstance(chunk, bytes):
#         print(chunk)