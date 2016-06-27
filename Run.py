import Rpinput
import Bhgame
import RPi.GPIO as GPIO
import time

#   PINS
button_one_pin = 26
button_two_pin = 12
button_three_pin = 16
led_one_pin = 27
led_two_pin = 18
led_three_pin = 17
switch_pin = 22

#   INITLIAZE PI INPUT CLASS.
rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, button_three_pin,
                           led_one_pin, led_two_pin, led_three_pin, switch_pin)

game_bh = Bhgame.GameThread(button_one_pin, button_two_pin, button_three_pin, led_one_pin,
                            led_two_pin, led_three_pin, switch_pin)


#   ok
#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    try:
        game_bh.display_still("bg")
        video_list = game_bh.game_list()
        while True:
            game_started = False
            while game_started is False:
                switch_state = rpi.button_state(switch_pin)
                if switch_state is False:
                    rpi.led_ready_state()
                    game_bh.play_film(video_list[0])
                else:
                    game_bh.play_game()
                    game_bh.kill_fbi()
                    time.sleep(5)
                    game_started = True
    except KeyboardInterrupt:
        GPIO.cleanup()

"""
def pre_game():
    rpi.led_not_ready_state()
    game_bh.display_still("bg")
    while True:
        switch_state = rpi.button_state(button_one_pin)
        if switch_state is True:
            time.sleep(2)
            start_game()
"""
#   MAGIC.
rpi.led_not_ready_state()
start_game()

