import time
import random
import os
import Rpinput
import RPi.GPIO as GPIO


class GameThread(object):
    def __init__(self, button_pin1, button_pin2, button_pin3, led_one_pin, led_two_pin, led_three_pin, switch_pin):
        self.rpi = Rpinput.RpiBoerhaave(button_pin1, button_pin2, button_pin3, led_one_pin, led_two_pin,
                                        led_three_pin, switch_pin)

    def run(self):
        try:
            self.rpi.led_ready_state()
            self.are_you_ready()
        except KeyboardInterrupt:
            GPIO.cleanup()

    def remove_static(self):
        pass

    def game_list(self):
        self.remove_static()

        #   INDIVIDUAL MOVIES
        film1 = "film1"
        film2 = "film2"
        film3 = "film3"
        film4 = "film4"
        film5 = "film5"
        film6 = "film6"
        film7 = "film7"
        film8 = "film8"
        movie_route = [film1, film2, film3, film4, film5, film6, film7, film8]

        return movie_route

    def unpack_movies(self, movie_list):
        self.remove_static()
        for films in movie_list:
            print(films)
            #   self.play_film(films)

    def play_film(self, film_name):
        self.remove_static()
        os.system("omxplayer %s.mp4" % film_name)

    def are_you_ready(self):
        try:
            while True:
                active_btn = self.rpi.button_state(self.rpi.button_three)
                active_switch = self.rpi.button_state(self.rpi.switch_pin)

                if active_switch is True:
                    print("You can now play the game.")
                    time.sleep(1)
                else:
                    self.rpi.led_not_ready_state()
                    break
                if active_btn is True:
                    self.play_game()
                else:
                    pass
        except KeyboardInterrupt:
            GPIO.cleanup()

    def game_part_one(self):
        self.rpi.led_busy_state()
        movie_route = self.game_list()

        print(movie_route[0])
        #   self.play_film(movie_route[0])
        time.sleep(0.2)
        print(movie_route[1])
        #   self.play_film(movie_route[1])

    def game_part_three(self):
        movie_route = self.game_list()
        route_selected = False

        #   GAME ROUTE IS CHOSEN BY A PSUEDO RANDOM CHANCE.
        print("Wil je, je hand schoonspoelen? %s" % (movie_route[2]))
        #   self.play_film(movie_route[2])
        while route_selected is False and self.rpi.button_state(22) is True:
            active_btn = self.rpi.get_active_button(0.2)
            if active_btn is 1:
                #   self.play_film(movie_route[3])
                print(movie_route[3])
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    #   self.play_film(movie_route[5])
                    print(movie_route[5])
                    route_selected = True
                elif rand_num is 1:
                    route_selected = True
            elif active_btn is 2:
                #   self.play_film(movie_route[3])
                print(movie_route[3])
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    #   self.play_film(movie_route[4])
                    print(movie_route[4])
                    route_selected = True
                elif rand_num is 1:
                    #   self.play_film(movie_route[6])
                    print(movie_route[6])
                    route_selected = True

    def game_part_two(self):
        movie_route = self.game_list()
        route_selected = False

        #   PART TWO OF MICROSCOPIA -> FIRST INPUT HERE -> BUTTON ACTION
        print("Ben je ziek?")
        #   self.play_film(movie_route[1])
        while route_selected is False and self.rpi.button_state(22) is True:
            active_btn = self.rpi.get_active_button(0.2)
            #   WAIT FOR ACTIVE BUTTON TO DETERMINE FIRST ROUTE.
            if active_btn is 1:
                route_selected = True
                #   self.play_film(movie_route[8])
                print(movie_route[7])
                #   GAME CONTINUES IN WEL ZIEK
                self.game_part_three()
            elif active_btn is 2:
                route_selected = True
                #   self.play_film(movie_route[2])
                print(movie_route[2])
                #   GAME CONTINUES IN NIET ZIEK
                self.game_part_three()

    def play_game(self):
        #   MAGIC -> I SHALL CALL YOU MICROSCOPIA
        #   PART ONE OF MICROSCOPIA
        self.game_part_one()

        time.sleep(1)   # AVOID BUTTON SPAM

        #   PART TWO OF MICROSCOPIA -> FIRST INPUT HERE -> BUTTON ACTION
        self.game_part_two()

        self.rpi.led_not_ready_state()
        print("Game over..")
