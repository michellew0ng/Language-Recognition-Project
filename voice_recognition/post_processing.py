
import re
import string
from openai import OpenAI
import led_state
import hardware_control
import light_timer
import key_phrase

buffer = ""
system_prompt = """
You are a voice processing assistant. You will never generate any responses of your own. If you don't understand 
the transcription, output the transcription exactly as it appears with all punctuation, filler words, and spaces removed. 
Always translate the transcription into English if needed.

If any part of the string matches or sounds like 'Light On', 'Light Off', 'Brightness 1' or any other number, 
'Timer 1' or any other number, 'Light Dim 1' or any other number, 'Max Brightness', 'Hey Doc', or 'Timer Cancel', including misspellings or homophones 
(e.g., 'hey dock', 'hey doch', 'timer cansel', etc.), replace those parts of the string with these exact variants.

You must:
- Filter out phrases such as 'thanks for watching', 'thank you', 'you', or similar noise that may occur when there is no meaningful audio input and replace with nothing.
- Replace 'hey doc timer cancel', or any variation with 'heydoctimercancel'.
- Translate 'apague la luz' or any equivalent to 'light off' (no alternative translations like 'turn off the light').
- For numbers, ensure the numerical version is used (i.e., use '10' instead of 'ten').
- Replace the recognized parts with the exact variants specified, and remove all punctuation and filler words, without altering the remaining content. 
Finally, lowercase everything.
"""

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def generate_corrected_transcript(transcription):
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
    return response.choices[0].message.content

# This function scans for the relevant key phrase
# ISSUE: What if the key phrase is caught over 2 audio chunks? How to solve? Must keep an external buffer to store this.
# FIX: buffer 
def scan_for_key_phrase(transcription):

    global buffer
  
    if not transcription:
        print("Empty transcription recieved.")
        return

    # Safeguards to remove all punctuation
    transcription = generate_corrected_transcript(transcription)
    transcription = remove_punctuation((transcription.lower()).replace(" ", "")) 
    # ChatGPT is not reliable at doing this

    print(f"Interpreted: {transcription}")

    buffer += transcription

    if light_timer.timer_active:
        if key_phrase.timer_cancel in buffer:
            light_timer.timer_cancel()
            buffer = ""
        #else:
        #    print("Timer is running. Ignoring other commands.")
        #    return  # Ignore all other inputs while the timer is active

    if light_timer.dimmer_active:
        if key_phrase.dimmer_cancel in buffer:
            light_timer.timer_dim_cancel()
            buffer = ""

    else:
        if key_phrase.on in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_5)
            buffer=""
        elif key_phrase.off in buffer:
            hardware_control.light_switch(led_state.LED_OFF)
            buffer=""
        elif key_phrase.level_1 in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_1)
            buffer=""
        elif key_phrase.level_2 in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_2)
            buffer=""
        elif key_phrase.level_3 in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_3)
            buffer=""
        elif key_phrase.level_4 in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_4)
            buffer=""
        elif key_phrase.level_5 in buffer or key_phrase.max_brightness in buffer:
            hardware_control.light_switch(led_state.LED_LEVEL_5)
            buffer=""
        elif key_phrase.timer_cancel in buffer:
            light_timer.timer_cancel()
            buffer=""
        else:
            # Runs timer command
            match = re.search(key_phrase.timer_pattern, buffer)
            if match:
                timer_secs = int(match.group(1))
                light_timer.timer_start(timer_secs)
                buffer = ""

            # Runs dimmer command
            match = re.search(key_phrase.dimmer_pattern, buffer)
            if match:
                timer_secs = int(match.group(1))
                light_timer.timer_dim(timer_secs)
                buffer = ""


            buffer = buffer [-len(key_phrase.level_1):] # keeps last part of buffer in case overlap