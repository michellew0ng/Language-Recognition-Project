from hardware_control import light_switch
from openai import OpenAI

# This function scans for the relevant key phrase
# ISSUE: What if the key phrase is caught over 2 audio chunks? How to solve? Must keep an external buffer to store this.
def scan_for_key_phrase(transcription):
  
    key_phrase_on = 'Hey Sam Light On'
    key_phrase_off = 'Hey Sam Light Off'

    if transcription:
        if key_phrase_on.lower() in transcription.lower():
            light_switch(True)
        elif key_phrase_off.lower() in transcription.lower():
            light_switch(False)

    