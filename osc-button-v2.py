#!/usr/bin/python3
#$/home/pi/WLC-Button-OSC/osc-button.py

#Jan. 14, 2017
#First Attempt at Button Inputs
#Goal is to get the program to take a button Press on GPIO18 and Print "Go" *done
#new goal: get OSC Commands to send. * Done
#Goal- figure out how to allow for non linear button hits
#goal- Figure out how to get rid of the argument stuff and just send osc commands *done

#adding OSC stuff here first
#import argparse
import time
#import random
from pythonosc import osc_message_builder
from pythonosc import udp_client

###the below was copied from python.org for learning., the aurgument number stuff was removed and
#straight IP address and port were added

#if __name__ == "__main__":
#  parser = argparse.ArgumentParser()
#  parser.add_argument("--ip", default="192.168.1.69",
 #     help="The ip of the OSC server")
 # parser.add_argument("--port", type=int, default=53001,
 #     help="The port the OSC server is listening on")
 # args = parser.parse_args()

client = udp_client.SimpleUDPClient("192.168.1.69", 53001) #args.ip, args.port) and was indented

 

###ending the osc additions

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#Go Button
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Stop Button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Pause Button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callback_1():
        global GPIO18_triggered
        set GPIO18_triggered:

def callback_2():
        global GPIO27_triggered
        set GPIO27_triggered

GPIO18_triggered = False
GPI027_triggered = False

add_event_detect(GPIO18, callback1)
add_event_detect(GPIO27, callback2)

stop = time.time() + 5

while not GPIO18_triggered and not GPIO27_triggered and time.time() <stop:
    time.sleep(.0.01)
    
cancel_event_detect(GPIO18)
cancel_event_detect(GPIO27)
    
if GPIO18_triggered:
    print("GO")
    client.send_message("eos/key/go", (1))
elif GPIO27_trigged:
    rint("Stop")
    client.send_message("eos/key/stop", random.random())
    time.sleep(1)

GPIO.cleanup()
