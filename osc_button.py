#!/usr/bin/python3
#$/home/pi/WLC-Button-OSC/osc-button.py
import time


import math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher


#the below IP addres is what you are talking to and the listening port
client = udp_client.SimpleUDPClient("192.168.1.95", 53000)



### Input setup here:
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#Go Button
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Stop Button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Pause Button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#changed to event detection to allow for non linear pressing of buttons
#Falling equals when you press rising equal release.
#You could standby with a press and go with release.
#

GPIO.add_event_detect(18, GPIO.FALLING, bouncetime=500)
GPIO.add_event_detect(27, GPIO.FALLING, bouncetime=500)
GPIO.add_event_detect(22, GPIO.FALLING, bouncetime=500)

#adding power off code 
from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown():
	check_call(['sudo', 'poweroff'])

shutdown_btn = Button(21, hold_time=6)
shutdown_btn.when_held = shutdown

#pause()
#end power off snippet

start = time.time()


while True:
    if GPIO.event_detected(18):
        print("GO")

        client.send_message("/go",(1))
        client.send_message("/eos/key/go", (1))

    if GPIO.event_detected(27):
        print("Stop")

        client.send_message("/stop", (1))
        client.send_message("/eos/key/stop", (1))

    if GPIO.event_detected(22):
        print("Pause")
        client.send_message("pause",(1))
#EOS doesn't have a pause so it's sneak enter
        client.send_message("eos/key/sneak", (1))
        client.send_message("eos/key/enter", (1))
    time.sleep(0.01)
 
GPIO.cleanup()
server.shutdown()