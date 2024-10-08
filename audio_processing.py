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
        response_format="text",
        prompt="you are a helpful assistant for a computer science university group project your task is to correct any spelling discrepancies in the transcribed text and make sure the phrases seperated with z can be recognised z hey doc light on z hey doc light off z stop z change it to these outputs if the words sound even remotely like it could be any of these phrases since false positives are better than false negatives dont add your own output delete all common filler words",
    )

    #return process_response(client, translation['text'])
    return translation