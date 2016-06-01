import Rpinput
import Bhgame
import threading

#   PINS
button_one_pin = 16
button_two_pin = 26
led_one_pin = 17
led_two_pin = 18
ldr_pin = 3

#   INITLIAZE PI INPUT CLASS.
rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, led_one_pin, led_two_pin, ldr_pin)
lock = threading.Lock()

#   USE THIS FUNCTION TO START THE GAME.
def game():
    gt = Bhgame.GameThread("GameThread", button_one_pin, button_two_pin, led_one_pin, led_two_pin, ldr_pin)
    gt.start()
    game_started = False
    user_there = 0
    while game_started is False:
        try:
            if rpi.detect_player(25) is True:
                rpi.led_ready_state()
                user_there += 1
                if gt.is_alive() is False and user_there is 2:
                    gt.start()
                else:
                    continue
            else:
                rpi.led_not_ready_state()
        except RuntimeError:
                print("nope")


game()
