#!/usr/bin/env python

import time
from time import sleep
import sys
import os
from subprocess import Popen
import SimpleMFRC522

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Set up card reader - Reserves GPIO 8, 9, 10, 11, 25
reader = SimpleMFRC522.SimpleMFRC522()
cardPresent = False
lastCardTime = time.time()

# Button input
TAPE_SWITCH = 26
GPIO.setup(TAPE_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Internal pullup

# Maglock output
MAGLOCK = 12
GPIO.setup(MAGLOCK, GPIO.OUT)
LOCK = 1
UNLOCK = 0
GPIO.output(MAGLOCK, LOCK)
lockState = LOCK

lastState = 1 # for detecting falling edges (when switch pressed)

movie = ("/home/pi/EscobarVHS/VHS.mp4")
playing = False
omxc = None
timer = time.time()
trigger = False

def checkCardPlaced(timestamp, present):
        id = reader.read_id_no_block()
        if (id is not None):
                timestamp = time.time()
                if not present:
                        present = True
                        return (True, timestamp, present)

        if time.time() - timestamp > 1:
                present = False

        return (False, timestamp, present)

print ("Started")

try:
        while 1:
                # Button press check
                if GPIO.input(TAPE_SWITCH) == 0 and lastState == 1:
                        print ("Switch triggered, begin playing video, unlock door")
                        timer = time.time()
                        trigger = True
                        omxc = Popen(['omxplayer', '-b', movie])
                        playing = True
                
                elif GPIO.input(TAPE_SWITCH) == 1 and playing:
                        os.system('killall omxplayer.bin')
                        playing = False
                lastState = GPIO.input(TAPE_SWITCH)

                if (omxc != None and playing):
                        if (omxc.poll() != None):
                                omxc = Popen(['omxplayer', '-b', movie])

                if ((time.time() - timer > 10) & trigger):
                        GPIO.output(MAGLOCK,UNLOCK)
                        lockState = UNLOCK
                        
                (placed, lastCardTime, cardPresent) = checkCardPlaced(lastCardTime, cardPresent)
                if placed:
                        print ("Card placed, toggling door")
                        GPIO.output(MAGLOCK, not lockState)
                        lockState = not lockState
                        trigger = False


finally:
	GPIO.cleanup() # clean up GPIO on exit
