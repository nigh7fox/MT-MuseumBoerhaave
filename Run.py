import Camera
import RPi.GPIO as GPIO
import time
from datetime import datetime
import Rpinput
import os


#   USE THIS FUNCTION TO START THE GAME.
def start_game():
    rpi = Rpinput.RpiBoerhaave(16, 26, 17, 18)
    rpi.turn_list_on()

start_game()
