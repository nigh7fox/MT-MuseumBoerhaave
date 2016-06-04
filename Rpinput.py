import RPi.GPIO as GPIO
import time
from datetime import datetime
import Twitter
import Camera
import os
import Bhgame as bhgame


class RpiBoerhaave(object):

    def __init__(self, button_pin1, button_pin2, led_pin1, led_pin2, led_pin3, ldr_pin, switch_pin):
        self.button_one = button_pin1
        self.button_two = button_pin2
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        self.led_pin3 = led_pin3
        self.ldr_pin = ldr_pin
        self.switch_pin = switch_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.button_one, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_two, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin1, GPIO.OUT)
        GPIO.setup(self.led_pin2, GPIO.OUT)
        GPIO.setup(self.ldr_pin, GPIO.OUT)
        GPIO.setup(self.led_pin3, GPIO.OUT)

    def remove_static(self):
        pass

    def ldr_state(self):
        GPIO.setup(self.ldr_pin, GPIO.OUT)
        GPIO.output(self.ldr_pin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(self.ldr_pin, GPIO.IN)

        while GPIO.input(self.ldr_pin) is GPIO.LOW:
            return True
        return False

    def get_pin_state(self):
        self.remove_static()
        print("Button pin %s pressed" % str(self.button_one))

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

    def detect_player(self, interval):
        #   USED TO DETECT WETHER A PLAYER IS STANDING INFRONT OF THE CAMERA.
        #   INTERVAL: THE AMOUNT OF TIME YOU WANT TO WAIT BEFORE DETERMINING THAT A USER IS THERE.
        #   SENSITIVITY: DEPENDING ON THE AMOUNT OF LIGHT THAT THE CAMERA IS EXPOSED TOO.
        self.remove_static()
        detection_count = 0  # NO LIGHT.
        while detection_count < interval:
            if self.ldr_state() is False:
                detection_count += 1
            else:
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
        self.turn_light_off(self.led_pin3)
        time.sleep(0.2)
        self.turn_light_on(self.led_pin1)

    def led_not_ready_state(self):
        self.turn_light_off(self.led_pin1)
        time.sleep(0.2)
        self.turn_light_off(self.led_pin3)
        time.sleep(0.2)
        self.turn_light_on(self.led_pin2)

    def led_busy_state(self):
        self.turn_light_off(self.led_pin1)
        time.sleep(0.2)
        self.turn_light_off(self.led_pin2)
        time.sleep(0.2)
        self.turn_light_on(self.led_pin3)

    def get_object_state(self):
        obj_state = self.button_state(self.switch_pin)
        time.sleep(0.2)
        if obj_state is True:
            return False
        else:
            return True
