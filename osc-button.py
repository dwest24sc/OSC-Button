#!/usr/bin/python3
#$/home/pi/WLC-Button-OSC/osc-button.py

#Jan. 14, 2017
#Third Attempt at Button Inputs
#Goal is to get the program to take a button Press on GPIO18 and Print "Go" *done
#new goal: get OSC Commands to send. * Done
#Goal- figure out how to allow for non linear button hits *done
#goal- Figure out how to get rid of the argument stuff and just send osc commands *done
#next version may be for OSC feedback then a screen for displaying it

#adding OSC stuff here first
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client

#the below IP addres is what you are talking to and the listening port
client = udp_client.SimpleUDPClient("192.168.1.69", 53001)

###ending the osc setup

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


start = time.time()
while True:
    if GPIO.event_detected(18):
        print("GO")
        client.send_message("eos/key/go", (0))
    if GPIO.event_detected(27):
        print("Stop")
        client.send_message("eos/key/stop", (0))
    if GPIO.event_detected(22):
        print("Pause")
        client.send_message("eos/key/pause", (0))
    time.sleep(0.01)
    
GPIO.cleanup()