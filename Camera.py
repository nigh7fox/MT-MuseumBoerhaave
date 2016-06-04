import picamera
import time
import Twitter
import motion_detect
from datetime import datetime


# !!IMPORTANT!! LOOKUP piCamera MODULE !!IMPORTANT!!
# Take picture. Nada mas.
def take_picture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.hflip = True
        camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        camera.capture("foo.jpg")


#   Function to record using PiCamera
def take_video(video_description):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording('%s.h264' % (video_description))
        camera.wait_recording(60)
        camera.stop_recording()

        
# Waste of time. Takes pictures, let's you choose one of them... Tweet it with the time and your written tweet.
def picture_to_twitter():
    print("Taking your picture smile!!")
    time.sleep(1)
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        camera.capture("foo.jpg")
        Twitter.tweet_with_photo("/home/pi/Desktop/MT-MuseumBoerhaave/foo.jpg")


#   Function to detect motion. Returns true if motion is detected.
#   Set sensivity according to the amount of light the camera is exposed too.
#   ie If you're in; day-light - higher sensitivity, darker - lower
def detect_motion(sensitivity):
    # Side note. Sensitivty at 100 works great in day-light.
    motion_state = motion_detect.motion(sensitivity)
    return motion_state
