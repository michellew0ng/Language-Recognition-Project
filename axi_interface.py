import socket
from audio_processing import *
from post_processing import process_response, scan_for_key_phrase

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096 #4KB

led_on = False

def stream_audio_from_axi():
    # Logic to receive data from the AXI bus
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((ETHERNET_IP, ETHERNET_PORT))
        while True:
            try:
                # Receive data from AXI over Ethernet
                audio, addr = s.recvfrom(BUFFER_SIZE)
                
                response = whisper_send_and_receive(audio)
                scan_for_key_phrase(response)
                #print(f"Response from API: {response}")

            except Exception as e:
                print(f"Error: {e}")
    pass

# Sends a command to the board
def send_signal(command):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(command.encode(), (ETHERNET_IP, ETHERNET_PORT))
        print(f"Sent command: {command}")

def send_off_signal():
    send_signal("LED_OFF")

def send_on_signal():
    send_signal("LED_ON")

# Checks that we don't send on signals when LED is on, and off signals when LED is off
def light_switch(requested_state):
    global led_on
    if not led_on and requested_state:
        # Turn the light ON
        send_on_signal()
        led_on = True
    elif led_on and not requested_state:
        send_off_signal()
        led_on = False