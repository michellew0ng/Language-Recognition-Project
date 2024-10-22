import socket

# Brightness levels
LED_OFF = 0
LED_LEVEL_1 = 1
LED_LEVEL_2 = 2
LED_LEVEL_3 = 3
LED_LEVEL_4 = 4
LED_LEVEL_5 = 5
LED_ON = 6

ETHERNET_IP = ''
ETHERNET_PORT = 8080
BUFFER_SIZE = 4096 #4KB

# LED state dictated by levels where 0 is off, 5 is fully on, and 1-5 are discrete brightness levels
led_state = LED_OFF
previous_on_state = LED_LEVEL_5 # so when the LED turns back on, it returns to former brightness

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
    elif light_level == LED_LEVEL_5:
        print("LED on at full brightness!")
    elif light_level == LED_ON:
        pass
        #print("LED is already on!")
    else:
        print("Unknown light level choice")

# Checks that we don't send on signals when LED is on, and off signals when LED is off
def light_switch(requested_state):
    global led_state
    global previous_on_state
    #print(f"requested state {requested_state}")
    #print(f"led_state {led_state}")
    
    if requested_state == LED_ON:
        if led_state != LED_OFF:
            # If the LED is already on (brightness level 1-5), ignore the request
            print("LED is already on, no action needed")
            return
        else:
            # If the LED is off, turn it back on to the previous brightness
            send_signal(previous_on_state)
    elif requested_state == LED_OFF:
        if led_state != LED_OFF:
            # Turn off the LED and store the current brightness level
            previous_on_state = led_state
            send_signal(LED_OFF)
    else:
        # Handle brightness change (1-5)
        if led_state != requested_state:
            previous_on_state = led_state  # Update the previous state
            send_signal(requested_state)
    
def get_current_brightness():
    return led_state
