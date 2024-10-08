import socket

# Brightness levels
LED_OFF = 0
LED_LEVEL_1 = 1
LED_LEVEL_2 = 2
LED_LEVEL_3 = 3
LED_LEVEL_4 = 4
LED_ON = 5

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096 #4KB

# LED state dictated by levels where 0 is off, 5 is fully on, and 1-5 are discrete brightness levels
led_state = LED_OFF
previous_on_state = LED_ON # so when the LED turns back on, it returns to former brightness

# Sends a command to the board
# def send_signal(command):
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#         s.sendto(command.encode(), (ETHERNET_IP, ETHERNET_PORT))
#         print(f"Sent command: {command}")

def send_signal(light_level):
    global led_state
    led_state = light_level
    if light_level == LED_OFF:
        print("LED turned off!")
    elif light_level == LED_LEVEL_1:
        print("LED on at brightness 1!")
    elif light_level == LED_LEVEL_2:
        print("LED on at brightness 2!")
    elif light_level == LED_LEVEL_3:
        print("LED on at brightness 3!")
    elif light_level == LED_LEVEL_4:
        print("LED on at brightness 4!")
    elif light_level == LED_ON:
        print("LED on at full brightness!")
    else:
        print("Unknown light level choice")

# Checks that we don't send on signals when LED is on, and off signals when LED is off
def light_switch(requested_state):
    global led_state
    global previous_on_state
    print(f"Requested state: {requested_state}")
    print(f"Current led state: {led_state}")
    if requested_state != led_state:
        if led_state == LED_OFF and requested_state == LED_ON:
            send_signal(previous_on_state)
        elif requested_state == LED_OFF:
            previous_on_state = led_state 
            send_signal(requested_state)
        else:
            previous_on_state = led_state
            send_signal(requested_state)

    print(f"Current previous on: {previous_on_state}")
    
            


        
