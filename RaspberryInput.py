import RPi.GPIO as GPIO
import time

pin_btn = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class RaspberryInput(object):

    def __init__(self):
        self.pin_btn = pin_btn

    def remove_static(self):
        pass

    def button_state(self):
        input_state = GPIO.input(self.pin_btn)
        if input_state is False:
            time.sleep(0.2)
            print(input_state)

