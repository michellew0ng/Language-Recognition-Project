import time
from openai import OpenAI
from pydub import AudioSegment

### API INTERFACING ###

def split_audio_into_chunks(audio_file_path, chunk_size_mb=25):
    # Logic to split the audio file into chunks of specified size (25 MB default)
    pass

def whisper_send_and_receive(audio_chunk):
    client = OpenAI()
    # Send audio_chunk to Whisper API and get the response
    pass