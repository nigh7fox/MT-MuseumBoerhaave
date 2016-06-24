import Rpinput
import Bhgame
import RPi.GPIO as GPIO
import time

#   PINS
button_one_pin = 16
button_two_pin = 26
button_three_pin = 12
led_one_pin = 18
led_two_pin = 27
led_three_pin = 17
switch_pin = 22

#   INITLIAZE PI INPUT CLASS.
rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, button_three_pin,
                           led_one_pin, led_two_pin, led_three_pin, switch_pin)


#   ok
#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    try:
        game_bh = Bhgame.GameThread(button_one_pin, button_two_pin, button_three_pin, led_one_pin,
                                    led_two_pin, led_three_pin, switch_pin)
        video_list = game_bh.game_list()
        game_bh.display_still("bg")
        while True:
            game_started = False
            while game_started is False:
                switch_state = rpi.button_state(switch_pin)
                if switch_state is False:
                    rpi.led_ready_state()
                    game_bh.play_film(video_list[0])
                else:
                    game_bh.run()
                    game_started = True
    except KeyboardInterrupt:
        GPIO.cleanup()

while True:
    switch_state = rpi.button_state(switch_pin)
    if switch_state is True:
        time.sleep(3)
        start_game()

