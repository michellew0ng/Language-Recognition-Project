import socket
import speech_recognition as sr
import io
import time
from openai import OpenAI
from audio_processing import whisper_send_and_receive
from post_processing import scan_for_key_phrase

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096 #4KB

client = OpenAI()

def stream_audio_from_mic(chunk_duration=3):
    r = sr.Recognizer()
    source = sr.Microphone()

     # Initialisation

    with source:  # This is where you enter the microphone context
        print("Callibrating for ambient noise...")
        r.adjust_for_ambient_noise(source)
    print("Calibrated. Say something!")               
            
    # Continuously takes in audio in 3s chunks
    try:
        while True:
            try:
                with source:
                    audio = r.listen(source, phrase_time_limit=chunk_duration)  # Capture a 3-second chunk of audio
                
                # Convert the AudioData instance into a WAV file
                wav_data = audio.get_wav_data()
                wav_file = io.BytesIO(wav_data)
                wav_file.name = "audio.wav"

                transcription = whisper_send_and_receive(client, wav_file)
                scan_for_key_phrase(transcription)
            
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Error with speech recognition: {e}")
            except Exception as e:
                print(f"Error during transcription: {e}")

            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nGoodbye! The Marvellous Voice Activated LED awaits your return!")

# def stream_audio_from_axi():
#     # Logic to receive data from the AXI bus
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#         s.bind((ETHERNET_IP, ETHERNET_PORT))
#         while True:
#             try:
#                 # Receive data from AXI over Ethernet
#                 audio, addr = s.recvfrom(BUFFER_SIZE)
                
#                 response = whisper_send_and_receive(audio)
#                 scan_for_key_phrase(response)
#                 #print(f"Response from API: {response}")

#             except Exception as e:
#                 print(f"Error: {e}")
#     pass

