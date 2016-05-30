import RPi.GPIO as GPIO
import time
from datetime import datetime
import Camera
import os


class RpiBoerhaave(object):

    def __init__(self, button_pin1, button_pin2, led_pin1, led_pin2):
        self.button_one = button_pin1
        self.button_two = button_pin2
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        GPIO.setmode(GPIO.BCM)
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
                    return 0  # NO BUTTON IS BEING PRESSED.
        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()

    def detect_player(self, interval, sensitivity):
        #   USED TO DETECT WETHER A PLAYER IS STANDING INFRONT OF THE CAMERA.
        #   INTERVAL: THE AMOUNT OF TIME YOU WANT TO WAIT BEFORE DETERMINING THAT A USER IS THERE.
        #   SENSITIVITY: DEPENDING ON THE AMOUNT OF LIGHT THAT THE CAMERA IS EXPOSED TOO.
        self.remove_static()
        detection_count = 0
        while detection_count < interval:
            if Camera.detect_motion(sensitivity) is True:
                detection_count += 1
            else:
                detection_count = 0
                return False
        return True

    def log_game_route(self, check_delay):
        #   LOG THE GAME ROUTE - SAVE THE ROUTE OF THE GAME IN A LIST/TXT FILE.
        #   SELECT ROUTES LEAD TO ACCORDING CONSQUENCES.
        #   OK. GO.
        routes = []

        button1 = self.button_state(self.button_one)
        button2 = self.button_state(self.button_two)
        button_list = [button1, button2]
        button_times_pressed = 0
        MAX_INPUT = 4  # BASICLY.... THE ROUTE OF THE LENGTH.

        while button_times_pressed < MAX_INPUT:
            active_tool = self.get_active_button(check_delay)
            if active_tool is 1 or active_tool is 2:
                routes.append(active_tool)
                button_times_pressed += 1
            else:
                print("Waiting for input")
        GPIO.cleanup()
        return routes

    def turn_light_on(self, led_pin):
        self.remove_static()
        while True:
            try:
                time.sleep(0.2)
                GPIO.output(led_pin, True)
            except KeyboardInterrupt:
                GPIO.cleanup()

    def movies_list(self):
        #   GENERATOR EXAMPLE FUNCTION.
        movie1 = "film1.mp4"
        movie2 = "film2.mp4"
        ml = [movie1, movie2]

        for movie in ml:
            yield (movie)
        self.remove_static()

    def game_ready(self, led_ready_pin, led_not_ready_pin):
        try:
            if self.detect_player(2, 150):
                time.sleep(0.2)
                GPIO.output(led_ready_pin, True)
            else:
                time.sleep(0.2)
                GPIO.output(led_not_ready_pin)
                print("No one wants to play!")
        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()
