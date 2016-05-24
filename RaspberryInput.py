import RPi.GPIO as GPIO
import time

#   SWITCH PINS
switch_pin_obj1 = 4
switch_pin_obj2 = 18

#   BUTTONS OBJECTS LIST
buttons_tool_pin = 16

#   BOARD PIN SETUP
GPIO.setmode(GPIO.BCM)

#   GPIO SETUPS
GPIO.setup(switch_pin_obj1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_pin_obj2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttons_tool_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#   *TEST* RETURN STATE OF BUTTONS
def button_test():

    button_pressed = False
    
    while True:
        #   INITIALIZE BUTTON INPUTS IN WHILE LOOP OR IT WON'T WORK.
        switch_state1 = GPIO.input(switch_pin_obj1)
        switch_state2 = GPIO.input(switch_pin_obj2)
        
        button_state1 = GPIO.input(buttons_tool_pin)

        #   WHILE -> ENDLESS CHECKING IF BUTTON IS PRESSED OR NOT
        if switch_state1 is 0 and button_pressed is False:
            print("Switch 1 Activated")
            button_pressed = True
            time.sleep(2.5)
            button_pressed = False
        elif switch_state2 is 0 and button_pressed is False:
            print("Switch 2 Activated")
            button_pressed = True
            time.sleep(2.5)
            button_pressed = False
        elif button_state1 is 0 and button_pressed is False:
            print("Button 1 Pressed")
            button_pressed = True
            time.sleep(2.5)
            button_pressed = False

#   USE THIS FUNCTION TO RETURN STATE OF PIN.
def button_state(button_pin):
    input_state = GPIO.input(button_pin)
    if input_state is 0:
        return True
    else:
        return False

def check_all_switches():
    switch1 = button_state(switch_pin_obj1)
    switch2 = button_state(switch_pin_obj2)
    while switch1 is True and switch2 is True:
        time.sleep(0.5)
        return True
    time.sleep(0.5)
    return False
          
#   CLEAN BOARD 
GPIO.cleanup()
