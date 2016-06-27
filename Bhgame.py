import time
import random
import os
import Rpinput


class GameThread(object):
    """

    THIS PY FILE CONTAINS THE GAME WORKER.

    THIS CLASS USES THE RPINPUT FILE TO GET INPUT FROM THE RASPBERRY PI AND USES THAT,
    INPUT TO CHANGE THE ROUTE THE GAME TAKES. EACH QUESTION AND ANSWER REPRESENT DIFFERENT VIDEOS.

    ALL VIDEO FILES ARE INSIDE THE GAME_LIST FUNCTION. USE THIS LIST TO PLAY SELECTED VIDEOS.
    GAME IS SPLIT INTO TWO PARTS. EACH PART REPRESENTING A QUESTION.

    USE FBI (FRAME BUFFER IMAGE) TO OPEN IMAGE FILES. AND KILLS THE FBI PROCESS AT THE END.

    """

    def __init__(self, button_pin1, button_pin2, button_pin3, led_one_pin, led_two_pin, led_three_pin, switch_pin):
        self.rpi = Rpinput.RpiBoerhaave(button_pin1, button_pin2, button_pin3, led_one_pin, led_two_pin,
                                        led_three_pin, switch_pin)

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
        film8 = "jodiumcleanv2"
        film9 = "jodiumviesv2"
        film10 = "bacterievirus"
        film11 = "bacteriev2"
        film12 = "bloedstolling"
        film13 = "wondjenietziek"
        film14 = "bloedhandkort"
        film15 = "korstje"
        movie_route = [film1, film2, film3, film4, film5, film6, film7, film8,
                       film9, film10, film11, film12, film13, film14, film15]
        return movie_route

    def play_film(self, film_name):
        self.remove_static()
        os.system("omxplayer -o local /home/pi/Desktop/films/%s.mp4" % film_name)

    def display_still(self, image_string):
        self.remove_static()
        os.system("fbi -T 2 --noverbose /home/pi/Desktop/films/%s.png" % image_string)

    def kill_fbi(self):
        self.remove_static()
        os.system("pkill fbi")

    def game_part_one(self):
        movie_route = self.game_list()
        route_selected = False
        count = 0
        replay_amount = 0

        print("Ben je ziek?")
        self.play_film(movie_route[13])
        self.play_film(movie_route[1])
        self.display_still("question_still")

        while route_selected is False:
            active_btn = self.rpi.get_active_button(0.2)
            if active_btn is 2:
                route_selected = True
                self.display_still("bg")

                self.play_film(movie_route[2])
                self.play_film(movie_route[11])

            elif active_btn is 3:
                route_selected = True
                self.display_still("bg")

                self.play_film(movie_route[3])
                self.play_film(movie_route[12])
            else:
                #   IF NO REPONSE FROM USER PLAY MOVIE AGAIN, WHEN PLAYED TWICE, CONTINUE GAME.
                count += 1
                if count is 20:
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
            if active_btn is 2:
                #   WILT SPOELEN
                route_selected = True
                self.display_still("bg")
                self.play_film(movie_route[5])
                self.play_film(movie_route[7])
                self.play_film(movie_route[10])
                #   LAST MOVIE DEFAULT
                self.play_film(movie_route[13])
            elif active_btn is 3:
                # WILT NIET SPOELEN
                route_selected = True
                self.display_still("bg")
                self.play_film(movie_route[8])
                self.play_film(movie_route[9])
                # LAST MOVIE DEFAULT
                self.play_film(movie_route[13])
            else:
                #   IF NO REPONSE FROM USER PLAY MOVIE AGAIN, WHEN PLAYED TWICE, CONTINUE GAME.
                count += 1
                if count is 20:
                    self.play_film(movie_route[4])
                    count = 0
                    replay_amount += 1
                    if replay_amount is 2:
                        self.display_still("bg")
                        route_selected = True

    def play_game(self):
        #   MAGIC -> I SHALL CALL YOU MICROSCOPIA
        print("Game active.")
        self.rpi.led_busy_state()

        #   PART ONE OF MICROSCOPIA
        self.game_part_one()

        time.sleep(1)   # AVOID BUTTON SPAM

        #   PART TWO OF MICROSCOPIA
        self.game_part_two()
        print("Game over..")
