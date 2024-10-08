from hardware_control import light_switch
from openai import OpenAI
import string
import re

buffer = ""
system_prompt = """
You are a voice processing assistant. Never output a response of your own, and if you don't understand, output the transcription exactly as it appears with punctuation, filler words, and spaces removed. 
Always translate the transcription into English if needed. If any part of the string matches 'Light On', 'Light Off', or 'Hey Doc', replace those parts of the string with these exact variants regardless of the phrasing. For instance, translate 'apague la luz' or any equivalent to 'light off'. 
For everything else, remove all punctuation, filler words, and spaces between words, without altering the remaining content. Lowercase everything."""

def generate_corrected_transcript(transcription):
    print(f"Initial audio: {transcription}")
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        #temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    print(f"API Response: {response.choices[0].message.content}")
    return response.choices[0].message.content

# This function scans for the relevant key phrase
# ISSUE: What if the key phrase is caught over 2 audio chunks? How to solve? Must keep an external buffer to store this.
# FIX: buffer 
def scan_for_key_phrase(transcription):

    global buffer
  
    if not transcription:
        print("Empty transcription recieved.")
        return
    
    key_phrase_on = 'heydoclighton'
    key_phrase_off = 'heydoclightoff'
    
    transcription = generate_corrected_transcript(transcription)
    transcription = (transcription.lower()).replace(" ", "")

    print(f"Final Output: {transcription}")

    buffer += transcription

    if key_phrase_on in buffer:
        light_switch(True)
    elif key_phrase_off in buffer:
        light_switch(False)
    else:
        buffer = buffer [-len(key_phrase_on):] # keeps last part of buffer in case overlap


