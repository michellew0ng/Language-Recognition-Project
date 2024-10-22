import time
import os 
from openai import OpenAI

### API INTERFACING ###

# Unsure if this is needed 
def split_audio_into_chunks(audio_file_path, chunk_size_mb=1):
    # Logic to split the audio file into chunks of specified size (25 MB default)
    pass

# Send audio_chunk to Whisper API and get the response, which is a translation if needed
def whisper_send_and_receive(client, audio_chunk):
    
    translation = client.audio.translations.create(
        model="whisper-1", 
        file=audio_chunk,
        temperature=0,
    )

    #return process_response(client, translation['text'])
    return translation.text