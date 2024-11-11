import socket
import speech_recognition as sr
import io
import time
import queue
import wave
from openai import OpenAI
import threading
from audio_processing import whisper_send_and_receive
from post_processing import scan_for_key_phrase
import led_state



ETHERNET_PORT = 49152
BUFFER_SIZE = 1024  # Size of each data packet received
SERVER_IP = '192.168.1.1'
QUEUE_SIZE = 100 # Max packets in queue

client = OpenAI()

##### SOLN 1: Recieves audio from laptop mic (PROOF OF CONCEPT) #####

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

    except KeyboardInterrupt:
       print("\nGoodbye! The Marvellous Voice Activated LED awaits your return!")



##### SOLN 2: Recieves audio from AXI bus ####
# Uses threading to account for dropped packets

def save_buffer_as_wav(buffer, sample_rate=44100, num_channels=2, sample_width=2):
    wav_data = io.BytesIO()
    with wave.open(wav_data, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(buffer)

    wav_data.seek(0)

    return wav_data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, ETHERNET_PORT))
data_queue = queue.Queue(maxsize=QUEUE_SIZE)
LED_ON_SIGNAL = 'T'
LED_OFF_SIGNAL = 'F'

def rcv_audio_data():
    while True:
        print("I AM CURRENTLY RECIEVING")
        try:
            # Receive data from AXI over Ethernet
            print("BEFORE")
            audio, addr = sock.recvfrom(BUFFER_SIZE)
            print("AFTER")
            #print(f"I CAN SEE THIS DATA: {audio}")
            if audio in b'END':
                data_queue.put(b'END')  # Signal processing thread to stop
                continue

            if not data_queue.full():
                data_queue.put(audio)
                print("i have the audio now")
            else:
                print("Warning: Queue is full. Dropping packet.")

        except Exception as e:
            print(f"Error while recieving data: {e}")

buffer = bytearray()

# Process audio data from the queue
def process_audio_data():
    while True:
        print("i am processing the audio now")
        try:
            print("getting the data")
            data = data_queue.get()

            if b'END' in data:
                if buffer:
                    response = whisper_send_and_receive(save_buffer_as_wav(buffer))
                    print("I have sent to whisper")
                    scan_for_key_phrase(response)
                    print("I tried to scan for a key phrase")
                    buffer.clear()
                continue
            print("Didn't see end, my buffer's longer now!")
            buffer.extend(data)

        except Exception as e:
            print(f"Error while processing data: {e}")

# Initialises threads and streams audio from axi bus
def stream_audio_from_axi():
    receiver_thread = threading.Thread(target=rcv_audio_data)
    receiver_thread.start()

    processor_thread = threading.Thread(target=process_audio_data)
    processor_thread.start()

    monitoring_thread = threading.Thread(target=monitor_led_state)
    monitoring_thread.start()

    receiver_thread.join()
    processor_thread.join()
    monitoring_thread.join()

# Monitors LED state and sends signal when changes
def monitor_led_state():
    while True:
        if led_state.need_to_change is True:
            if led_state.led_state == led_state.LED_OFF:
                message = LED_OFF_SIGNAL
                sock.sendto(message.encode(), (SERVER_IP, ETHERNET_PORT))
            elif led_state.led_state in [led_state.LED_LEVEL_1, led_state.LED_LEVEL_2, led_state.LED_LEVEL_3,
                                    led_state.LED_LEVEL_4, led_state.LED_LEVEL_5]:
                message = LED_ON_SIGNAL
                sock.sendto(message.encode(), (SERVER_IP, ETHERNET_PORT))
            led_state.need_to_change = False
        time.sleep(0.5)


# Turns light on and off every 10 seconds
def test_send_data():
    while True:
        try:
            message = LED_ON_SIGNAL
            sock.sendto(message.encode(), (SERVER_IP, ETHERNET_PORT))
            time.sleep(10)

            message = LED_OFF_SIGNAL 
            sock.sendto(message.encode(), (SERVER_IP, ETHERNET_PORT))
            time.sleep(10)
        except Exception as e:
            print(f"Error sending data: {e}")
            break