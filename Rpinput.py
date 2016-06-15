import RPi.GPIO as GPIO
import time


class RpiBoerhaave(object):

    def __init__(self, button_pin1, button_pin2, button_pin3, led_pin1, led_pin2, led_pin3, switch_pin):
        self.button_one = button_pin1
        self.button_two = button_pin2
        self.button_three = button_pin3
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        self.led_pin3 = led_pin3
        self.switch_pin = switch_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.button_one, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_two, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_three, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin1, GPIO.OUT)
        GPIO.setup(self.led_pin2, GPIO.OUT)
        GPIO.setup(self.led_pin3, GPIO.OUT)

    def remove_static(self):
        pass

    def button_state(self, button_pin):
        input_state = GPIO.input(button_pin)
        time.sleep(0.2)
        try:
            if input_state is 0:
                return True
            else:
                return False
        except KeyboardInterrupt:
            GPIO.cleanup()
            self.remove_static()

    def get_active_button(self, check_delay):
        #   EACH BUTTON REPRESENTS A OBJECT. IN THIS UGLY PART WE COMPARE THE CURRENT STATES AND RETURN A NUMBER.
        #   IF A STATE IS FOUND TO BE FALSE -> IT WILL RETURN ITS NUMBER (BUTTON NUMBER)
        #   FOR EXAMPLE -> IF IT RETURNS 2 MEANS THAT SWITCH "2" IS NOT PRESSED -> ACTIVE.
        try:
            button1 = self.button_state(self.button_one)
            button2 = self.button_state(self.button_two)
            button3 = self.button_state(self.button_three)

            if button1 is True:
                time.sleep(check_delay)
                return 1
            elif button2 is True:
                time.sleep(check_delay)
                return 2  # BUTTON 2 PRESSED AND ...
            elif button3 is True:
                time.sleep(check_delay)
                return 3
            else:
                return None  # NO BUTTON IS BEING PRESSED.

        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()

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

    def led_list(self):
        led_list = (self.led_pin1,
                    self.led_pin2,
                    self.led_pin3)
        return led_list

    def led_ready_state(self):
        GPIO.output(self.led_list(), (GPIO.HIGH, GPIO.LOW, GPIO.LOW))

    def led_not_ready_state(self):
        GPIO.output(self.led_list(), (GPIO.LOW, GPIO.HIGH, GPIO.LOW))

    def led_busy_state(self):
        GPIO.output(self.led_list(), (GPIO.LOW, GPIO.LOW, GPIO.HIGH))

    def all_led_on(self):
        GPIO.output(self.led_list(), (GPIO.HIGH, GPIO.HIGH, GPIO.HIGH))

    def all_led_off(self):
        GPIO.output(self.led_list(), (GPIO.LOW, GPIO.LOW, GPIO.LOW))

    def check_user(self, timer):
        self.remove_static()
        return None
