import Camera
import RPi.GPIO as GPIO
import time
from datetime import datetime
import Rpinput
import os

pin1 = 4
pin2 = 18


#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    rpi = Rpinput.RpiBoerhaave(23, 0, 4, 18)
    while True:
        rpi.game_ready(4, 18)

start_game()
