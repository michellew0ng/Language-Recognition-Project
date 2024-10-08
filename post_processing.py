from hardware_control import light_switch
from openai import OpenAI
import string
import re

buffer = ""

# Function to remove punctuation
def clean_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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
    
    transcription = clean_text(transcription).replace(" ", "").lower()
    print(transcription)
    buffer += transcription

    if key_phrase_on in buffer:
        light_switch(True)
    elif key_phrase_off in buffer:
        light_switch(False)
    else:
        buffer = buffer [-len(key_phrase_on):] # keeps last part of buffer in case overlap