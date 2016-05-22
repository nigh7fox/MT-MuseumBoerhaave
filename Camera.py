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
        camera.capture("static/ext/foo.jpg")

# Waste of time. Takes pictures, let's you choose one of the ones you took... Tweet it with the time and your written tweet.
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

#   Function to take a picture if motion detection is True for X amount of time.
#   Use the invterval parameter to set the time. (1 check every 2 seconds)
#   Example. if interval = 5; it will take a picture if motion is detected for 10 seconds. (5 x 2)
def motion_with_picture(interval):
    i = 0
    
    while True:
        current_time = datetime.now().strftime('%Y-%M-%D %H:%M:%S')
        if detect_motion(100):
            i += 1
            print(str(current_time))
            if i is interval:
                #   This part can be replaced with any other function.
                #   Example -> You need to check if something a hand is inside your machine.
                #   If motion was detected for 5 seconds -> then -> activate Movie.
                print("Motion has been detected for too long! Somethings fishy..\nTaking a photo just incase. Please wait..")
                take_picture()
        else:
            print("No motion")
            i = 0

motion_with_picture(3)
