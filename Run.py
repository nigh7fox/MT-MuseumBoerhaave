import Rpinput
import Bhgame
import RPi.GPIO as GPIO

#   PINS
button_one_pin = 16
button_two_pin = 26
button_three_pin = 12
led_one_pin = 27
led_two_pin = 17
led_three_pin = 18
switch_pin = 22

#   INITLIAZE PI INPUT CLASS.
rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, button_three_pin,
                           led_one_pin, led_two_pin, led_three_pin, switch_pin)


#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    try:
        game_bh = Bhgame.GameThread(button_one_pin, button_two_pin, button_three_pin, led_one_pin,
                                    led_two_pin, led_three_pin, switch_pin)
        video_list = game_bh.game_list()
        while True:
            game_started = False
            switch_state = rpi.button_state(switch_pin)
            print("Play idle movie! %s " % (video_list[0]))
            #   game_bh.play_film(video_list[0])
            while game_started is False and switch_state is True:
                game_bh.run()
                game_started = True
            rpi.led_not_ready_state()
    except KeyboardInterrupt:
        GPIO.cleanup()

start_game()

