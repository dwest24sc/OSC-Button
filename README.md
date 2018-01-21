1/21/18
 OSC-Button verson 1.0
# OSC-Button

This is a challenge to myself to learn what a Pi is, how to code in Python
and how to get a simple OSC Command (1 command) sent to a lighting console or a QLAB machine.

Previous itterations have gone from input on contacts only to outputs in OSC.
Added a small 128x64 screen for cue numbers. That works

current version works as two scripts.  One being for the contacts to osc.  The next being the display script.  The display is an adafruit knockoff.  Current problem is the screen flickering when its doing the redraw of the background rectangle to blank out the previous text.

Previous versions deleted because the latest version is so massive and combines many things into one script.

Ideas being used from various sources.  Including cscashby/pi-showcontrol.
