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
            print("Game active.")
            self.play_game()
        except KeyboardInterrupt:
            GPIO.cleanup()

    def remove_static(self):
        pass

    def game_list(self):
        self.remove_static()

        #   INDIVIDUAL MOVIES
        film1 = "intro"
        film2 = "benjeziek"
        film3 = "BacteriaGrowth"
        film4 = "jodium"
        film5 = "schoonmaken"
        film6 = "spoelen2"
        film7 = "bacteriev3"
        film8 = "film8"
        film9 = "film9"
        film10 = "korstje"
        movie_route = [film1, film2, film3, film4, film5, film6, film7, film8, film9, film10]

        return movie_route

    def play_film(self, film_name):
        self.remove_static()
        os.system("omxplayer -o local /home/pi/Desktop/%s.mp4" % film_name)

    def display_still(self, image_string):
        self.remove_static()
        os.system("fbi -T 2 --noverbose %s.png" % image_string)

    def game_part_one(self):
        movie_route = self.game_list()
        route_selected = False
        count = 0
        replay_amount = 0

        print("Ben je ziek?")
        self.play_film(movie_route[1])
        self.display_still("question_still")
        while route_selected is False:
            active_btn = self.rpi.get_active_button(0.2)
            if active_btn is 1:
                route_selected = True
                self.play_film(movie_route[2])
                #   print(movie_route[7])
            elif active_btn is 2:
                route_selected = True
                self.play_film(movie_route[3])
                #   print(movie_route[2])
            else:
                count += 1
                if count is 10:
                    self.play_film(movie_route[1])
                    count = 0
                    replay_amount += 1
                    if replay_amount is 2:
                        route_selected = True

    def game_part_two(self):
        movie_route = self.game_list()
        route_selected = False
        count = 0
        replay_amount = 0

        print("Wil je, je hand schoonspoelen?")
        self.play_film(movie_route[4])
        self.display_still("question_still")
        while route_selected is False:
            active_btn = self.rpi.get_active_button(0.2)
            print(active_btn)
            if active_btn is 1:
                route_selected = True
                self.display_still("bg")
                self.play_film(movie_route[5])
                #   print(movie_route[3])
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    self.play_film(movie_route[9])
                    #   print(movie_route[5])
                elif rand_num is 1:
                    self.play_film(movie_route[9])
            elif active_btn is 2:
                route_selected = True
                self.display_still("bg")
                self.play_film(movie_route[6])
                #   print(movie_route[3])
                rand_num = random.randrange(0, 2)
                if rand_num is 0:
                    self.play_film(movie_route[9])
                    #   print(movie_route[4])
                elif rand_num is 1:
                    self.play_film(movie_route[6])
                    #   print(movie_route[6])
            else:
                count += 1
                if count is 10:
                    self.play_film(movie_route[4])
                    count = 0
                    replay_amount += 1
                    if replay_amount is 2:
                        self.display_still("bg")
                        route_selected = True

    def play_game(self):
        #   MAGIC -> I SHALL CALL YOU MICROSCOPIA
        #   PART ONE OF MICROSCOPIA
        self.rpi.led_busy_state()
        self.display_still("bg")
        self.game_part_one()
        time.sleep(1)   # AVOID BUTTON SPAM
        #   PART TWO OF MICROSCOPIA -> FIRST INPUT HERE -> BUTTON ACTION
        self.game_part_two()
        self.rpi.led_not_ready_state()
        print("Game over..")
