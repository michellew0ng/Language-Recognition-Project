
import hardware_control
import threading

timer_thread = None
timer_active = False

dimmer_active = False
dim_threads = []

# activates led on, waits the given number of seconds, then led off
# works for up to 999 seconds 
def timer_start(num_secs):
    global timer_thread, timer_active

    previous_brightness = hardware_control.get_current_brightness()

    hardware_control.light_switch(hardware_control.LED_ON)

    timer_thread = threading.Timer(num_secs, timer_expired)
    timer_active = True
    print(f"Timer for {num_secs} set!")
    timer_thread.start()


def timer_expired():
    global timer_active
    print(f"Timer has expired!")
    hardware_control.light_switch(hardware_control.LED_OFF)
    timer_active = False


def timer_cancel():
    global timer_thread, timer_active, previous_brightness
    
    if timer_active and timer_thread is not None:
        # Cancel the active timer
        timer_thread.cancel()
        print(f"Timer canceled! Light on at brightness {hardware_control.led_state}")
        hardware_control.light_switch(hardware_control.LED_ON)
        timer_active = False
    else:
        print("No active timer to cancel.")

# Dims the lights from full brightness to off over the course of num_secs
def timer_dim(num_secs):
    global dimmer_active
    dimmer_active = True
    interval = num_secs / 5
    
    def set_brightness(level):
        global dimmer_active
        if level >= 0 and dimmer_active:
            hardware_control.light_switch(level)
            print(f"Brightness dimmed to level {level}")
            # Schedule the next brightness change
            if level > 0:
                thread = threading.Timer(interval, set_brightness, [level - 1])
                thread.start()
                dim_threads.append(thread)
            else:
                print(f"Light is completely dimmed. Goodnight!")


    print(f"Dimming the lights over {num_secs} seconds.")
    set_brightness(hardware_control.LED_LEVEL_5)

def timer_dim_cancel():
    global dimmer_active
    
    if dimmer_active:
        dimmer_active = False
        # Cancel all active dimming timers
        for thread in dim_threads:
            thread.cancel()
        dim_threads.clear()  # Clear the list of threads 
    else:
        print("No dimming in progress to cancel.")

