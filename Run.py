import Camera
import RaspberryInput
import RPi.GPIO as GPIO
import time

#   SWITCH PINS
switch_pin_obj1 = 4
switch_pin_obj2 = 18

#   BUTTONS OBJECTS LIST
button_pin_tool1 = 16

#   BOARD PIN SETUP
GPIO.setmode(GPIO.BCM)

#   GPIO SETUPS
GPIO.setup(switch_pin_obj1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_pin_obj2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin_tool1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#   USE THIS FUNCTION TO RETURN STATE OF PIN.
def button_state(button_pin):
    input_state = GPIO.input(button_pin)
    if input_state is 0:
        return True
    else:
        return False

def check_all_switches():
    #   GIVE EACH SWITCH IT'S STATE. ADD SWITCH TO LIST.
    switch1 = button_state(switch_pin_obj1)
    switch2 = button_state(switch_pin_obj2)
    switch_list = [switch1, switch2]

    #   CHECK ALL SWITCHES IN THE LIST - EACH SWITCH THAT IS TRUE +1 - COMPARE TO LENGTH OF LIST (ALL SWITCHES)
    switches_on = 0
    for switches in switch_list:
        while switches is True:
            switches_on += 1
            time.sleep(0.5)
            if switches_on is len(switch_list):
                return True
    time.sleep(0.5)
    return False

def get_active_subject():
    #   EACH SWITCH REPRESENTS A OBJECT. IN THIS UGLY PART WE COMPARE THE CURRENT STATES AND RETURN A NUMBER.
    #   IF A STATE IS FOUND TO BE FALSE -> IT WILL RETURN ITS NUMBER (SWITCH NUMBER)
    #   FOR EXAMPLE -> IF IT RETURNS 2 MEANS THAT SWITCH "2" IS NOT PRESSED -> ACTIVE.

    #   GET SWITCH STATES.
    switch1 = button_state(switch_pin_obj1)
    switch2 = button_state(switch_pin_obj2)
    
    if switch1 is False and switch2 is False:
        return(3) # ALWAYS HIGHEST NUMBER -> ALL ITEMS ARE MISSING. WTF?
    elif switch1 is False:
        return(1)   #   SWITCH 1 IS NOT PRESSED - ACTIVE 
    elif switch2 is False:
        return(2)   #   SWITCH 2 AND SO ON....DOTDOTDOT
    else:
        return(0) # ALL OF THEM ARE PRESSED - NOT ACTIVE

def get_active_tool():
    button1_tool = button_state(button_pin_tool1)
    tool_used = False
    if button1_tool is True and tool_used is False:
        return(1)   #   BUTTON 1 PRESSED AND TOOL USED CHANGED TO TRUE - KEEP TRACK OF TOOLS BEING USED. -> GAME LOGIC.
        tool_used = True
    elif tool_used is True:
        return(2) # ALWAYS THE HIGHEST NUMBER -> TOOL HAS BEEN USED -> LOG -> RESET(COMING SOON)
    else:
        return(0)
    
def detect_player(interval, sensitivity):
    #   USED TO DETECT WETHER A PLAYER IS STANDING INFRONT OF THE CAMERA.
    #   INTERVAL: THE AMOUNT OF TIME YOU WANT TO WAIT BEFORE DETERMINING THAT A USER IS THERE.
    #   SENSITIVITY: DEPENDING ON THE AMOUNT OF LIGHT THAT THE CAMERA IS EXPOSED TOO.
    detection_count = 0
    while detection_count < interval:
        if Camera.detect_motion(sensitivity) is True:
            detection_count += 1
        else:
            detection_count = 0
            return False
    return True
       
def check_run_status(interval, sensitivity):
    #   UNFINISHED FUNCTION USED TO DETERMINE WHEN THE GAME IS READY TO START -> THERE IS A PLAYER PRESENT.
    #   METALLICA - ONE
     while True:
        if detect_player(interval, sensitivity) is True and check_all_switches():
            print("Possible player wants to play\nShall we ask? ...")
        elif check_all_switches() is False:
            print("Where'd my stuff go?!")
        else:
            print("No one wants to play")

print(check_all_switches())
