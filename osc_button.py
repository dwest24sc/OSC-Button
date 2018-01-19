#!/usr/bin/python3
#$/home/pi/WLC-Button-OSC/osc-button.py


#adding OSC stuff here first
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher
#addeded for osc as well
import socketserver

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration: (not used on our screen but code needs it
RST = 24
#display type
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

width = disp.width
height = disp.height

image = Image.new('1', (width,height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("FreeSans.ttf", 26)

#the below IP addres is what you are talking to and the listening port
client = udp_client.SimpleUDPClient("192.168.1.95", 53000)
#def send_osc(oscCommand):
 #   for server, m in oscCommands.items():
  #      ip = [192/.168/.1/.107]
   #     port = [53001]
 
 
 # the below is commented since it does nothing
"""def get_cuename():
    send_osc("/cue/selected/displayname")"""
             

#server info
"""
def _call_handlers_for_packet(data, dispatcher):
    try:
        packet=osc_packet.OscPacket(data)
        for timed_msg in packet.messages:
            now = time.time()
            handlers = dispatcher.handlers_for_address(
                timed_msg.message.address)
            if not handlers:
                continue
            if timed_msg.time > now:
                time.sleep(timed_msg.time - now)
            for handler in handlers:
                if handler.args:
                    handler.callback(
                        timed_msg.message.address, handler.args, *timed_msg.messgae)
                else:
                    handler.callback(timed_msg.message.address, *timed_msg.message)
    except osc_packet.ParseError:
        pass
class _UDPHandeler(socketserver.BaseRequestHandler):
    def handle(self):
        _callhandlers_for_packet(self.request[0], self.sever.dispatcher)
def _is_valid_request(request):
    data = request[0]
    return (
        osc_bundle.OscBundle.dgram_is_bundle(data)
        or osc_message.OscMessage.dgram_is_message(data))
class OSCUDPServer(socketserver.UDPServer):
    def __init__(self, server_address, dispatcher):
        super().__init__(server_address, _UDPHandler)
        self.dispatcher = dispatcher
        
    def verify_request(self, request, client_address):
        return _is_valid_request(request)
    
    @property
    def dispatcher(self):
        return self._dispatcher

class BlockingOSCUDPServer(OSCUDPServer):
    @property
    def dispatcher(self):
        return self._dispatcher
###ending the osc server setup
"""
"""
cue = str
pend = str

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/eos/out/active/cue*", cue)
dispatcher.map("/eos/out/pending/cue*", pend)
"""


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
disp.begin()

# Clear display.
disp.clear()
disp.display()

draw.text((0,-0),    'Live', font=font, fill=1)
draw.text((0,30),   'Next', font=font, fill=1)


# Display image.
disp.image(image)
disp.display()

while True:
    if GPIO.event_detected(18):
        print("GO")
#        disp.clear()
#        disp.display()
        draw.rectangle((55,0,width,height), outline=0, fill = 0)
        draw.text((55,-0),    'cue', font=font, fill=255)
        draw.text((55,30),   'pend', font=font, fill=255)
        client.send_message("/go",(1))
        client.send_message("/eos/key/go", (1))
        disp.image(image)
        disp.display()
    if GPIO.event_detected(27):
        print("Stop")
#        disp.clear()
#        disp.display()
        draw.rectangle((55,0,width,height), outline=0, fill = 0)
        draw.text((55,-0),    'STOP', font=font, fill=255)
        draw.text((55,30),   'Hold', font=font, fill=255)
        client.send_message("/stop", (1))
        client.send_message("/eos/key/stop", (1))
        disp.image(image)
        disp.display()
    if GPIO.event_detected(22):
        print("Pause")
        client.send_message("pause",(1))
#EOS doesn't have a pause so it's sneak enter
        client.send_message("eos/key/sneak", (1))
        client.send_message("eos/key/enter", (1))
    time.sleep(0.01)
 
GPIO.cleanup()
server.shutdown()