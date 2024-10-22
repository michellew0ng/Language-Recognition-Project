from axi_interface import light_switch
import openai

def process_response(client, transcription):
    # Use GPT to process and correct the transcription
    system_prompt = "You are a helpful assistant for a computer science university group project. Your task is to correct any spelling discrepancies in the transcribed text. Make sure the phrases: Hey Doc, Light On, and Light Off are output if the words sound even remotely like it could be any of these phrases - false positives are better than false negatives."

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
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
    corrected_text = response.choices[0].message.content

    return corrected_text

# This function scans for the relevant key phrase
# ISSUE: What if the key phrase is caught over 2 audio chunks? How to solve? Must keep an external buffer to store this.
def scan_for_key_phrase(transcription):
    
    key_phrase_on = 'Hey Doc Light On'
    key_phrase_off = 'Hey Doc Light Off'

    if 'text' in transcription: 
        if key_phrase_on.lower() in transcription['text'].lower():
            light_switch(True)
        elif key_phrase_off.lower() in transcription['text'].lower():
            light_switch(False)

    