
import re
import string
from openai import OpenAI
import hardware_control

buffer = ""
system_prompt = """
You are a voice processing assistant. Never output a response of your own, and if you don't understand, 
output the transcription exactly as it appears with punctuation, filler words, and spaces removed. 
Always translate the transcription into English if needed. If any part of the string matches or even sounds like 'Light On', 
'Light Off', 'Brightness 1', 'Max Brightness or any other number, or 'Hey Doc', replace those parts of the string with 
these exact variants regardless of the phrasing. For instance, translate 'apague la luz' or any equivalent to 'light off'. 
I will not accept any alternative translation, like 'turn off the light'.
After you're done, remove all punctuation, filler words, and spaces between words, without altering 
the remaining content. Lowercase everything."""

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

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
    key_phrase_level_1 = 'heydocbrightness1'
    key_phrase_level_2 = 'heydocbrightness2'
    key_phrase_level_3 = 'heydocbrightness3'
    key_phrase_level_4 = 'heydocbrightness4'
    key_phrase_level_5 = 'heydocbrightness5'
    key_phrase_max = 'heydocmaxbrightness'
    
    transcription = generate_corrected_transcript(transcription)
    transcription = remove_punctuation((transcription.lower()).replace(" ", "")) # Safeguards to remove all punctuation
    # ChatGPT is not reliable at doing this

    print(f"Final Output: {transcription}")

    buffer += transcription

    if key_phrase_on in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_5)
        buffer=""
    elif key_phrase_off in buffer:
        hardware_control.light_switch(hardware_control.LED_OFF)
        buffer=""
    elif key_phrase_level_1 in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_1)
        buffer=""
    elif key_phrase_level_2 in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_2)
        buffer=""
    elif key_phrase_level_3 in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_3)
        buffer=""
    elif key_phrase_level_4 in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_4)
        buffer=""
    elif key_phrase_level_5 in buffer or key_phrase_max in buffer:
        hardware_control.light_switch(hardware_control.LED_LEVEL_5)
        buffer=""
    else:
        buffer = buffer [-len(key_phrase_level_1):] # keeps last part of buffer in case overlap

    


