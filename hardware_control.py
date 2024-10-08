import socket

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096 #4KB

led_on = False

# Sends a command to the board
# def send_signal(command):
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#         s.sendto(command.encode(), (ETHERNET_IP, ETHERNET_PORT))
#         print(f"Sent command: {command}")

def send_off_signal():
    print("LED IS SWITCHED OFF!")
    #send_signal("LED_OFF")

def send_on_signal():
    print("LED IS SWITCHED ON!")
    #send_signal("LED_ON")

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