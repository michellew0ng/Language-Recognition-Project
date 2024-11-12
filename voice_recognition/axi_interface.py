import socket
import speech_recognition as sr
import io
import signal
import time
import queue
import wave
import sys
import zlib
from collections import OrderedDict

from openai import OpenAI
import threading
from audio_processing import whisper_send_and_receive
from post_processing import scan_for_key_phrase
import led_state



ETHERNET_PORT = 49152
BUFFER_SIZE = 65507  # Size of each data packet received
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
                wav_file.seek(0)
                
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

data_queue = queue.Queue(maxsize=QUEUE_SIZE)
LED_ON_SIGNAL = 'T'
LED_OFF_SIGNAL = 'F'

stop_event = threading.Event()

def rcv_audio_data(sock):

    while True:
       # print("I AM CURRENTLY RECIEVING")
        try:
            # Receive data from AXI over Ethernet
           # print("BEFORE")
            audio, addr = sock.recvfrom(BUFFER_SIZE)
           # print("AFTER")
            #print(f"I CAN SEE THIS DATA: {audio}")
            if audio == b'END':
                data_queue.put(b'END')  # Signal processing thread to stop
                continue

             # Ensure the packet is large enough to contain the sequence number and data
            if len(audio) < 2:
                print("Received packet is too small, skipping.")
                continue
             # Extract the 2-byte sequence number from the start of each packet
            seq_num = (audio[0] << 8) + audio[1]
            data = audio[2:]  # The remaining bytes are the compressed audio data

            if not data_queue.full():
                data_queue.put((data, seq_num))
                print("i have the audio now")
            else:
                print("Warning: Queue is full. Dropping packet.")

        except Exception as e:
            print(f"Error while recieving data: {e}")

#buffer = bytearray()

# Process audio data from the queue
def process_audio_data():
    compressed_data = bytearray()
    packet_buffer = OrderedDict()  # Buffer to store packets by sequence number
    expected_seq = 0  # Expected sequence number for ordering
    
    while not stop_event.is_set():
        print("i am processing the audio now")
        try:
            print("getting the data")
            item = data_queue.get()
            #data = data_queue.get()

            if item == b'END':
                # Concatenate buffered packets in the correct order
                for seq, chunk in sorted(packet_buffer.items()):
                    if seq == expected_seq:
                        compressed_data.extend(chunk)
                        expected_seq += 1
                    else:
                        print(f"Warning: Missing packet with sequence {expected_seq}")
                        break  # Exit if a packet is missing to avoid corrupt data

                if compressed_data:
                    try:
                        decompressed_data = zlib.decompress(compressed_data, wbits=-15)
                        conv_audio = io.BytesIO(decompressed_data)
                        conv_audio.seek(0)
                        response = whisper_send_and_receive(client, conv_audio)
                        scan_for_key_phrase(response)
                        print("I tried to scan for a key phrase")
                        compressed_data.clear()
                    except zlib.error as e:
                        print(f"Decompression error: {e}")
                    compressed_data.clear()  # Clear data if decompression fails
                    packet_buffer.clear()
                    expected_seq = 0
                continue

            data, seq_num = item
            print("Didn't see end, my buffer's longer now!")
            # Store the packet in the buffer based on its sequence number
            if seq_num == expected_seq:
                compressed_data.extend(data)
                expected_seq += 1
            else:
                packet_buffer[seq_num] = data
           
        except Exception as e:
            print(f"Error while processing data: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

# Initialises threads and streams audio from axi bus
def stream_audio_from_axi():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, ETHERNET_PORT))
    
    receiver_thread = threading.Thread(
        target=rcv_audio_data, kwargs={'sock': sock}
    )
    receiver_thread.start()

    processor_thread = threading.Thread(target=process_audio_data)
    processor_thread.start()

    monitoring_thread = threading.Thread(
        target=monitor_led_state, kwargs={'sock': sock}
    )
    monitoring_thread.start()

    try:
        receiver_thread.join()
        processor_thread.join()
        monitoring_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_event.set()
        sys.exit(0)

# Monitors LED state and sends signal when changes
def monitor_led_state(sock):
    while not stop_event.is_set():
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


# Implements the signal for CTRL+C to kill the program
def signal_handler(sig, frame):
    print("\nCaught SIGINT (Ctrl+C), shutting down gracefully...")
    stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

############### TESTS ###################

# Turns light on and off every 10 seconds
def test_send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, ETHERNET_PORT))

    while not stop_event.is_set():
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