import socket

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096

led_on = False

def receive_data_from_axi():
    # Logic to receive data from the AXI bus
    pass

def send_on_signal():
    # Logic to send a signal to turn the LED ON
    pass

def send_off_signal():
    # Logic to send a signal to turn the LED OFF
    pass

def light_switch(requested_state):
    global led_on
    if not led_on and requested_state:
        # Turn the light ON
        send_on_signal()
        led_on = True
    elif led_on and not requested_state:
        # Turn the light OFF
        send_off_signal()
        led_on = False