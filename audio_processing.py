import time
from openai import OpenAI
from pydub import AudioSegment
from post_processing import scan_for_key_phrase

### API INTERFACING ###

client = OpenAI()

# Unsure if this is needed 
def split_audio_into_chunks(audio_file_path, chunk_size_mb=1):
    # Logic to split the audio file into chunks of specified size (25 MB default)

    audio_file= open("/path/to/file/audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    pass

# Send audio_chunk to Whisper API and get the response, which is a translation if needed
def whisper_send_and_receive(audio_chunk):
    client = OpenAI()
  
    translation = client.audio.translations.create(
        model="whisper-1", 
        file=audio_chunk
    )

    return translation 