
import hardware_control
import threading

timer_thread = None
timer_active = False

# activates led on, waits the given number of seconds, then led off
# works for up to 999 seconds 
def timer_start(num_secs):
    global timer_thread, timer_active, previous_brightness 

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