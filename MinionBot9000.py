#!/usr/bin/env python

from time import sleep
from subprocess import Popen
import os

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Button input
TORTURE_VOLTAGE = 26
GPIO.setup(TORTURE_VOLTAGE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Internal pullup

class SoundPlayer:
    def __init__(self):
        # Initial video setup
        self.omxc = None
        
    def playSound(self, soundFile):
        # If already playing, check if it has finished and needs to restart the loop
        if not self.playing():
            filePath = "/home/pi/MinionBot9000/Sounds/" + soundFile + ".mp3"
            self.omxc = Popen(['omxplayer',v filePath])
            
    def playing(self):
        if (self.omxc != None):
            if (self.omxc.poll() == None):
                return True
        return False
        
    def stopSound(self):
        os.system('killall omxplayer.bin')
    
soundPlayer = SoundPlayer()

try:
    while 1:
        # Button press check
        if GPIO.input(TORTURE_VOLTAGE) == 1:
            soundPlayer.playSound('MinionsScreaming')
            
        sleep(0.05)
            
finally:
    GPIO.cleanup() # clean up GPIO on exit
