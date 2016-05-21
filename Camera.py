import picamera
import time
import Twitter
import motion_detect

def take_picture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.vflip = True
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture("static/ext/foo.jpg")


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
                picture_name = "camerapix/foo[" + str(picture_id) + "].jpg"
                camera.capture(picture_name)
                picture_id += 1
                if picture_id is 2:
                    wp = input("Which picture did you want to upload?(1 - 3): ")
                    print("Alright, so..")
                    try:
                        Twitter.tweet_with_photo("/home/pi/Desktop/MuseumBoerhaave/camerapix/foo[" + str(wp) + "].jpg")
                    except FileNotFoundError:
                        print("Error.. The picture id you entered does not match any in our database.."
                              "\nTry again..")
        else:
            print("Ok, I'll fuck off.")


def detect_motion():
    motionState = False
    motionState = motion_detect.motion()
    return motionState


