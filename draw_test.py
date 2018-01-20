#!/usr/bin/python3
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import argparse
import math

#from pythonosc import osc_message_builder
#from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

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
#client = udp_client.SimpleUDPClient("192.168.1.95", 53000)

start = time.time()
disp.begin()


disp.clear()
disp.display()

disp.image(image)
disp.display()
def print_cue_handler(str, args, cue,):
    cue_playing = ("{1}".format(args[0], cue))
    print("{1}".format(args[0], cue))
    draw.rectangle((0,0,width,26), outline=0, fill = 0)
    draw.text((0,-0),    cue_playing, font=font, fill=1)
    disp.image(image)
    disp.display()
      
def print_next_handler(str, args,  cue,):
    cue_next = ("{1}".format(args[0], cue))
    print("{1}".format(args[0], cue))
    draw.rectangle((0,27,width,height), outline=0, fill = 0)
    draw.text((0,27),    cue_next, font=font, fill=1)
    disp.image(image)
    disp.display()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
    default="192.168.1.108", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=53001, help="The port to listen to")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/eos/out/active/cue/text", print_cue_handler, "cue")
    dispatcher.map("/eos/out/pending/cue/text", print_next_handler, "cue")
 
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


disp.image(image)
disp.display()