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
        camera.vflip = True
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
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
    picture_id = 1
    while picture_id < 2:
        ask = input("Do you want to take a picture?(Y or N): ")

        if ask == "Y" or ask == "y":
            with picamera.PiCamera() as camera:
                camera.resolution = (1024, 768)
                camera.vflip = True
                camera.start_preview()
                # Camera warm-up time
                time.sleep(2)
                picture_name = "camerapix/foo[%s].jpg" % (str(picture_id))
                camera.capture(picture_name)
                picture_id += 1
                if picture_id is 2:
                    wp = input("Which picture did you want to upload?(1 - 3): ")
                    print("Alright, so..")
                    try:
                        Twitter.tweet_with_photo("/home/pi/Desktop/MuseumBoerhaave/camerapix/foo[%s].jpg" % (wp))
                    except FileNotFoundError:
                        print("Error.. The picture id you entered does not match any in our database.."
                              "\nTry again..")
        else:
            print("Ok, I'll fuck off.")


#   Function to detect motion. Returns true if motion is detected.
#   Set sensivity according to the amount of light the camera is exposed too. ie If you're in; day-light - higher sensitivity, darker - lower
def detect_motion(sensitivity):
    # Side note. Sensitivty at 100 works great in day-light.
    motionState = motion_detect.motion(sensitivity)
    return motionState
