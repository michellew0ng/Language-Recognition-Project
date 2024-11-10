# This file holds the LED state and previous LED state to be accessed across the file system.

# Brightness levels
LED_OFF = 0
LED_LEVEL_1 = 1
LED_LEVEL_2 = 2
LED_LEVEL_3 = 3
LED_LEVEL_4 = 4
LED_LEVEL_5 = 5
LED_ON = 6

# LED state dictated by levels where 0 is off, 5 is fully on, and 1-5 are discrete brightness levels
led_state = LED_OFF
previous_on_state = LED_LEVEL_5

# Set to True when the LED needs to change. Notifies a listening thread.
need_to_change = False 