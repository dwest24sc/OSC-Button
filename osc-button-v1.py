#!/usr/bin/python3
#$/home/pi/WLC-Button-OSC/osc-button.py

#Jan. 13, 2017
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

#Print info While will send the command the whole time it's pressed
#so we won't use that command.  left here for remembering later
#while True:
#    if(GPIO.input(18) == 0):
#        print("Go")

#the below isn't working
#def printFunction(channel):
#    print("Go")
#    GPIO.add_event_detect(18, GPIO.FALLING, callback=printfunction, bouncetime=.1)
    
while True:
#REMEBER TO INDENT UNTIL THIS IS DONE
    GPIO.wait_for_edge(18, GPIO.FALLING)
    print("GO")
    client.send_message("eos/key/go", (1))
#adjust the sleep to allow for forced pause between presses
    #.5 is about the fastest it can go right now without
    #counting both up and down
    #which with wait for edge, it shouldn't be doing
    time.sleep(.5)

#below button hits don't function right, need to be in order,
#can't go go, go , go
#must happen go, stop, pause, go stop, and so on.
#

#    GPIO.wait_for_edge(27, GPIO.FALLING)
#    print("Stop")
#    client.send_message("eos/key/stop", random.random())
#    time.sleep(1)

#    GPIO.wait_for_edge(22, GPIO.FALLING)
#    print("Pause")

GPIO.cleanup()
