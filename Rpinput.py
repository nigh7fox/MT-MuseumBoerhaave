import RPi.GPIO as GPIO
import time
from datetime import datetime
import Camera
import os
import Bhgame as bhgame
import thread


class RpiBoerhaave(object):

    def __init__(self, button_pin1, button_pin2, led_pin1, led_pin2):
        self.button_one = button_pin1
        self.button_two = button_pin2
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.button_one, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_two, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin1, GPIO.OUT)
        GPIO.setup(self.led_pin2, GPIO.OUT)

    def remove_static(self):
        pass

    def button_state(self, button_pin):
        input_state = GPIO.input(button_pin)
        try:
            if input_state is 0:
                return True
            else:
                return False
        except KeyboardInterrupt:
            GPIO.cleanup()
            self.remove_static()
    GPIO.cleanup()

    def get_active_button(self, check_delay):
        #   EACH BUTTON REPRESENTS A OBJECT. IN THIS UGLY PART WE COMPARE THE CURRENT STATES AND RETURN A NUMBER.
        #   IF A STATE IS FOUND TO BE FALSE -> IT WILL RETURN ITS NUMBER (BUTTON NUMBER)
        #   FOR EXAMPLE -> IF IT RETURNS 2 MEANS THAT SWITCH "2" IS NOT PRESSED -> ACTIVE.
        try:
            button1_tool = self.button_state(self.button_one)
            button2_tool = self.button_state(self.button_two)
            tool_used = False

            if tool_used is False:
                if button1_tool is True:
                    tool_used = True
                    time.sleep(check_delay)
                    return 1
                elif button2_tool is True:
                    tool_used = True
                    time.sleep(check_delay)
                    return 2  # BUTTON 2 PRESSED AND ...
                else:
                    tool_used = False
                    return None  # NO BUTTON IS BEING PRESSED.
        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()

    def detect_player(self, sensitivity):
        #   USED TO DETECT WETHER A PLAYER IS STANDING INFRONT OF THE CAMERA.
        #   INTERVAL: THE AMOUNT OF TIME YOU WANT TO WAIT BEFORE DETERMINING THAT A USER IS THERE.
        #   SENSITIVITY: DEPENDING ON THE AMOUNT OF LIGHT THAT THE CAMERA IS EXPOSED TOO.
        self.remove_static()
        detection_count = 0
        interval = 2
        while detection_count < interval:
            if Camera.detect_motion(sensitivity) is True:
                detection_count += 1
            else:
                detection_count = 0
                return False
        return True

    def turn_light_on(self, led_pin):
        self.remove_static()
        try:
            time.sleep(0.2)
            GPIO.output(led_pin, True)
        except KeyboardInterrupt:
            GPIO.cleanup()

    def turn_light_off(self, led_pin):
        self.remove_static()
        try:
            time.sleep(0.2)
            GPIO.output(led_pin, False)
        except KeyboardInterrupt:
            GPIO.cleanup()

    def led_ready_state(self):
        self.turn_light_off(self.led_pin2)
        time.sleep(0.2)
        self.turn_light_on(self.led_pin1)

    def led_not_ready_state(self):
        self.turn_light_off(self.led_pin1)
        time.sleep(0.2)
        self.turn_light_on(self.led_pin2)

    def player_is_present(self, sensitivity):
        if self.detect_player(sensitivity) is True:
            return True
        else:
            return False

    def game_ready(self):
        game_played = False
        try:
            while True:
                detect = self.player_is_present(100)
                while detect is True:
                    self.led_ready_state()
                    if game_played is False:
                        bhgame.play_game()
                        game_played = True
                    else:
                        break
                    time.sleep(1)
                print("Waiting")
                self.led_not_ready_state()
        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()

