import time
import random
import os
import Rpinput
import RPi.GPIO as GPIO


class GameThread(object):
    def __init__(self, button_one_pin, button_two_pin, led_one_pin, led_two_pin, led_three_pin, ldr_pin, switch_pin):
        self.rpi = Rpinput.RpiBoerhaave(button_one_pin, button_two_pin, led_one_pin, led_two_pin,
                                        led_three_pin, ldr_pin, switch_pin)

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

        default_intro = "intro3"
        default_second_film = "film_intro"

        movie_schoon_resultaat = "korstje"
        movie_niet_schoon_resultaat = "korstje"

        movie_infectie = "infectie_film.mp4"

        movie_ziek = "film_intro"
        movie_niet_ziek = "film1"

        #   MOVIE LISTS

        movies_wel_ziek = ["film_intro", "ziek_film1.mp4", "ziek_film2.mp4", movie_schoon_resultaat]
        movies_niet_ziek = ["film_intro", "niet_ziek1.mp4", "niet_ziek2.mp4", movie_schoon_resultaat]
        movies_wel_infectie = ["film_intro", "infectie_film1.mp4", "infectie_film2", movie_niet_schoon_resultaat]
        movies_niet_infectie = ["film_intro", "niet_infectie_film1.mp4", "niet_infectie_film2.mp4",
                                movie_niet_schoon_resultaat]

        #   LISTCEPTIONISMSTICLY

        movies_stap2 = [movie_ziek, movie_niet_ziek]
        movies_stap3 = [movies_niet_ziek[0], movies_wel_ziek[0], movie_infectie]
        movies_stap4 = [movies_wel_ziek, movies_niet_ziek, movies_wel_infectie, movies_niet_infectie]

        #   WHAT I REALLY WANT.

        movie_route = [default_intro, default_second_film, movies_stap2, movies_stap3, movies_stap4]

        return movie_route

    def unpack_movies(self, movie_list):
        self.remove_static()
        for films in movie_list:
            #   self.play_film(films)
            print(films)

    def play_film(self, film_name):
        self.remove_static()
        os.system("omxplayer %s.mp4" % film_name)

    def are_you_ready(self):
        try:
            while True:
                active_btn = self.rpi.button_state(self.rpi.button_one)
                if active_btn is True:
                    self.play_game()
                    return None
                else:
                    pass
        except KeyboardInterrupt:
            GPIO.cleanup()

    def game_part_one(self):
        self.rpi.led_busy_state()
        movie_route = self.game_list()

        print(movie_route[0])
        #   self.play_film(movie_route[0])
        time.sleep(0.1)
        print(movie_route[1])
        #   self.play_film(movie_route[1])
        time.sleep(0.1)

    def game_part_three(self, movies_list_wel_ziek, movies_list_niet_ziek, movies_list_wel_infectie, movies_list_niet_infectie):
        route_selected = False
        #   GAME ROUTE IS CHOSEN BY A PSUEDO RANDOM CHANCE.
        print("Wil je, je hand schoonspoelen?")
        while route_selected is False and self.rpi.check_user(5) is True:
            active_btn = self.rpi.get_active_button(0.2)
            if active_btn is 1:
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    self.unpack_movies(movies_list_wel_ziek)
                    route_selected = True
                elif rand_num is 1:
                    self.unpack_movies(movies_list_niet_ziek)
                    route_selected = True
            elif active_btn is 2:
                time.sleep(3)
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    self.unpack_movies(movies_list_wel_infectie)
                    route_selected = True
                elif rand_num is 1:
                    self.unpack_movies(movies_list_niet_infectie)
                    route_selected = True

    def game_part_two(self):
        movie_route = self.game_list()
        stap2 = movie_route[2]
        stap4 = movie_route[4]
        route_selected = False

        #   PART TWO OF MICROSCOPIA -> FIRST INPUT HERE -> BUTTON ACTION
        print("Ben je ziek?")
        while route_selected is False and self.rpi.check_user(5) is True:
            active_btn = self.rpi.get_active_button(0.2)
            #   WAIT FOR ACTIVE BUTTON TO DETERMINE FIRST ROUTE.
            if active_btn is 1:
                route_selected = True
                #   self.play_film(stap2[0])
                print(stap2[0])
                #   GAME CONTINUES IN WEL ZIEK
                self.game_part_three(stap4[0], stap4[1], stap4[2], stap4[3])
            elif active_btn is 2:
                route_selected = True
                #   self.play_film(stap2[1])
                print(stap2[1])
                #   GAME CONTINUES IN NIET ZIEK
                self.game_part_three(stap4[0], stap4[1], stap4[2], stap4[3])

    def play_game(self):
        #   MAGIC -> I SHALL CALL YOU MICROSCOPIA
        #   PART ONE OF MICROSCOPIA
        self.game_part_one()

        time.sleep(2)   # AVOID BUTTON SPAM

        #   PART TWO OF MICROSCOPIA -> FIRST INPUT HERE -> BUTTON ACTION
        self.game_part_two()
