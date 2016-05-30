import time
from datetime import datetime
import Twitter
import Rpinput
import random
import os


def game_list():
    #   INDIVIDUAL MOVIES

    default_intro = "film1"
    default_second_film = "film2"
    movie_schoon_resultaat = "film3.mp4"
    movie_niet_schoon_resultaat = "film4.mp4"
    movie_infectie = "infectie_film.mp4"
    movie_wel_schoon_spoelen = "resulaat_schoon.mp4"
    movie_niet_schoon_spoelen = "resultaat_niet_schoon.mp4"

    #   MOVIE LISTS

    movies_wel_ziek = ["ziek_film0.mp4", "ziek_film1.mp4", "ziek_film2.mp4", movie_schoon_resultaat]
    movies_niet_ziek = ["niet_ziek0.mp4", "niet_ziek1.mp4", "niet_ziek2.mp4", movie_schoon_resultaat]
    movies_wel_infectie = ["infectie_film0.mp4", "infectie_film1.mp4", "infectie_film2", movie_niet_schoon_resultaat]
    movies_niet_infectie = ["niet_infectie_film0.mp4", "niet_infectie_film1.mp4", "niet_infectie_film2.mp4",
                            movie_niet_schoon_resultaat]

    #   LISTCEPTIONISMSTICLY

    movies_stap2 = [movie_wel_schoon_spoelen, movie_niet_schoon_spoelen]
    movies_stap3 = [movies_niet_ziek[0], movies_wel_ziek[0], movie_infectie]
    movies_stap4 = [movies_niet_ziek, movies_wel_ziek, movies_wel_infectie, movies_niet_infectie]

    #   WHAT I REALLY WANT.

    movie_route = [default_intro, default_second_film, movies_stap2, movies_stap3, movies_stap4]

    return movie_route


def unpack_movies(movie_list):
    for films in movie_list:
        print(films)


def play_film(film_name):
    os.system("omxplayer %s.mp4" % film_name)


def play_game():
    #   MAGIC.
    movie_route = game_list()
    rpi = Rpinput.RpiBoerhaave(16, 26, 17, 18)
    ziek_route = movie_route[4]
    route_selected = False

    play_film(movie_route[0])
    time.sleep(1)
    play_film(movie_route[1])
    time.sleep(1)

    print("Want to get infected?")

    while route_selected is False:
        active_btn = rpi.get_active_button(0.5)
        if active_btn is 1:
            route_selected = True
            randnum = random.randrange(0, 2)
            if randnum is 0:
                niet_ziek_list = ziek_route[0]
                unpack_movies(niet_ziek_list)
            elif randnum is 1:
                wel_ziek = ziek_route[1]
                unpack_movies(wel_ziek)
        elif active_btn is 2:
            route_selected = True
            randnum_infectie = random.randrange(2, 4)
            if randnum_infectie is 2:
                niet_infectie_list = ziek_route[2]
                unpack_movies(niet_infectie_list)
            elif randnum_infectie is 3:
                wel_infectie_list = ziek_route[3]
                unpack_movies(wel_infectie_list)
