import Rpinput
import Bhgame

#   PINS
button_one_pin = 16
button_two_pin = 26
led_one_pin = 17
led_two_pin = 27
led_three_pin = 18
ldr_pin = 3
switch_pin = 12

#   INITLIAZE PI INPUT CLASS.
rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, led_one_pin, led_two_pin, led_three_pin, ldr_pin, switch_pin)


#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    game_bh = Bhgame.GameThread(button_one_pin, button_two_pin, led_one_pin, led_two_pin, led_three_pin, ldr_pin, switch_pin)
    while True:
        game_started = False
        #   ldr_state = rpi.ldr_state()
        while game_started is False and rpi.check_user(5) is True:
            game_bh.run()
            game_started = True
            print("Game over...")
        rpi.led_not_ready_state()

start_game()

