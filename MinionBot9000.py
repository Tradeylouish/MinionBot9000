#!/usr/bin/env python

from time import sleep
from subprocess import Popen
import os

import cv2
import numpy as np
import imutils

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
            self.omxc = Popen(['omxplayer',filePath])
            
    def playing(self):
        if (self.omxc != None):
            if (self.omxc.poll() == None):
                return True
        return False
        
    def stopSound(self):
        os.system('killall omxplayer.bin')
    
soundPlayer = SoundPlayer()

# Connect to camera
WIDTH = 200
cam=cv2.VideoCapture(0)
banana_cascade = cv2.CascadeClassifier('BananaCascade.xml')

try:
    while 1:
        # Button press check
        if GPIO.input(TORTURE_VOLTAGE) == 1:
            soundPlayer.playSound('MinionsScreaming')
            
        ret, frame = cam.read()
        frame = imutils.resize(frame, WIDTH)
            
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.medianBlur(gray,5)
        
        bananas = banana_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=340, minSize=(55, 55))
    
        for (x,y,w,h) in bananas:
            print((x,y))
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0), 2)
            soundPlayer.playSound('Banana')
        
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) == 27:
            break  # esc to quit
            
    cv2.destroyAllWindows()
            
finally:
    cv2.destroyAllWindows()
    GPIO.cleanup() # clean up GPIO on exit
