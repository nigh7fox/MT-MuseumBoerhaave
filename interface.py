from flask import (Flask, render_template, request, flash)
import RPi.GPIO as GPIO
import os
import time
import threading
import thread
from threading import Thread
 
app = Flask(__name__) 

GPIO.setmode(GPIO.BCM)

##PINS
coil_A_1_pin = 17
coil_A_2_pin = 22
coil_B_1_pin = 24
coil_B_2_pin = 23
pin_button = 18
pin_led = 21
pin_ldr = 3

GPIO.setwarnings(False)

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_led, GPIO.OUT)

forward_seq = ['1000', '0100','0010', '0001']

#GLOBAL VARIABLES
global end_reach 
end_reach = 0
rotate_max = 3
ball_max = (512 * rotate_max)
light_on = 0
foo = 0
default_ball_delay = (2.5 / 1000.0)
work = 1
global stop_now
stop_now = 0
reverse_seq = list(forward_seq) # to copy the list
reverse_seq.reverse() #reverse for downwards

def checkLight ():
  # Discharge capacitor
  GPIO.setup(pin_ldr, GPIO.OUT)
  GPIO.output(pin_ldr, GPIO.LOW)
  measurement = 0
  time.sleep(0.5)

  GPIO.setup(pin_ldr, GPIO.IN)
  
  # Count loops until voltage across
  # capacitor reads high on GPO
 
  if(GPIO.input(pin_ldr) == GPIO.LOW):
    measurement = 1  

  return measurement

#CHECK IF BTN IS PRESSED
def checkState():
 return GPIO.input(pin_button)

#TURN LED LIGHT ON / OFF
def turnLightOn():
 GPIO.output(pin_led, GPIO.HIGH)
 time.sleep(0.2)

def turnLightOff():
 GPIO.output(pin_led, GPIO.LOW)
 time.sleep(0.2)

#MOTOR MOVE FUNCTIONS

#MOVE UP
def up(delay, steps):
   for i in range(steps):
    if(checkState() == 0):
     break
    for step in reverse_seq:
      if(stop_now == 1):
        global stop_now
        stop_now = 0
        thread.exit()
        GPIO.cleanup()
      else:
        set_step(step)
        time.sleep(delay)

#MOVE DOWN
def down(delay, steps):
  for i in range(steps):
   if(i == (512*rotate_max)):
     global end_reach
     end_reach = 1
     time.sleep(0.2)
   for step in forward_seq:
      if(stop_now == 1):
        global stop_now
        stop_now = 0
        thread.exit()
        GPIO.cleanup()
      else:  
        set_step(step)
        time.sleep(delay)

#COMBO FUNCTION: UP & DOWN (PARAMETERS ROTATIONS (512*rotations))
def move(start,rotations):
        go_up = "up"
        go_down = "down"
        if(start==go_up):
         up(default_ball_delay, (512*rotations))
        elif(start==go_down):
         down(default_ball_delay, (512*rotations))

##CHECK WHERE I AM
def up_or_down():
        if(end_reach == 1):
         time.sleep(0.2)
         global end_reach
         end_reach = 0
         up(default_ball_delay, (600*rotate_max))
        elif(checkLight() == 1):
         if(checkState() == 0):
          down(default_ball_delay, (512*rotate_max))

#RETURN TOP credits: Mustafa uit groep 31
def goHome():
  while True:
        if(checkState() == 0):
          break
        else:
          steps = 1 
          up(default_ball_delay, steps)

##FUNCTIONS TO RUN MOTOR.
def run():
    time.sleep(0.2)
    move("up", 3)
    up_or_down()

#ANIMATE THE RUN IN WHILE TRUE TO GO UNTIL LIGHT IS OFF.
def animate():
  while True:
    while (checkLight() == 1 and stop_now == 0): ##ALS ER LICHT IS MAG IK PAS BEWEGEN
     turnLightOn()
     time.sleep(4.5) ##DELAY VOOR IEDER PI OM ANIMATIE TE CREEEREN.
     set_step('0000')
     run()
    else:
     turnLightOff()
     goHome()

def stop():
  global stop_now
  stop_now = 1


def set_step(step):
  GPIO.output(coil_A_1_pin, step[0] == '1')
  GPIO.output(coil_A_2_pin, step[1] == '1')
  GPIO.output(coil_B_1_pin, step[2] == '1')
  GPIO.output(coil_B_2_pin, step[3] == '1')

##FLASK CODE STARTS HERE EACH BUTTON REPRESENTS A PAGE.
@app.route("/")
def index():
	return render_template('index.htm')

@app.route("/led_off.htm")
def led_off():
	 turnLightOff()
	 return render_template('index.htm')

@app.route("/led_on.htm")
def led_on():
	 turnLightOn()
	 return render_template('index.htm')

@app.route("/home.htm")
def go_home():
	 goHome()
	 return render_template('index.htm')

@app.route("/auto_on.htm")
def auto_on():
   ##turnLightOn()
   global stop_now
   stop_now = 0   
   thread.start_new_thread(animate, ())
   return render_template('index.htm')

@app.route("/auto_off.htm")
def auto_off():
   ##turnLightOff()
   stop()
   return render_template('index.htm')

@app.route("/shutdown.htm")
def shutdown():
	os.system("sudo poweroff")
 	return render_template('index.htm')

@app.route("/reboot.htm")
def reboot():
	os.system("sudo reboot")
 	return render_template('index.htm')

@app.route("/down.htm", methods=['GET'])
def go_down(): 
  s = (int)(request.args.get('steps'))
  down(default_ball_delay, s)
  return render_template('index.htm')

@app.route("/up.htm", methods=['GET'])
def go_up():
  s = (int)(request.args.get('steps'))
  up(default_ball_delay, s)
  return render_template('index.htm')

@app.route("/xpos.htm")
def xpos():
  x = open('/boot/x.txt', 'r')
  for line in x:
    print line
    return line

@app.route("/ypos.htm")
def ypos():
  y = open('/boot/y.txt', 'r')
  for line in y:
    print line
    return line

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 

GPIO.cleanup()