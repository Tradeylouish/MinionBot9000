#!/usr/bin/env python

from time import sleep
from subprocess import Popen
import os

import cv2
import numpy as np
import imutils
from collections import deque

import serial
import serial.tools.list_ports

import pygame

RPi = False
soundspath = "Sounds/"

if RPi:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    soundspath = "/home/pi/MinionBot9000/Sounds/"
    
# Pygame audio setup
pygame.init()
pygame.mixer.init()

class MinionBot:
    def __init__(self):
        self.ser = self.setupSerial()

        # Connect to camera
        self.WIDTH = 200
        self.cam=cv2.VideoCapture(0)
        #banana_cascade = cv2.CascadeClassifier('BananaCascade.xml')
        self.banana_cascade = cv2.CascadeClassifier('banana_classifier.xml')

        self.MIN_BANANA_FRAMES = 5
        self.bananaFrameCount = 0
        

    def setupSerial(self):
        # Serial setup - hacky fix for finding Arduino
        ser = None
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
        # "USB" for CH340 serial driver, "ACM" for Atmel driver
            if "USB" in p.device or "ACM" in p.device:
                ser = serial.Serial(p.device,9600)
                print("Established serial connection with " + p.device)
                ser.flushInput()
                break
        return ser

    def readSerial(self):
        # Read analog voltage over serial
        if (self.ser.inWaiting()>0):
            # Read line over serial, strip whitespace and decode
            msg = self.ser.readline()
            msg = msg.strip()
            msg = msg.decode('utf-8')
            try:
                voltage = float(msg)
                if voltage > 0:
                    print(voltage)
                    volume = voltage/5.0
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(soundspath + "MinionsScreaming.mp3")
                        pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(volume)
                    
            except ValueError:
                print('Not a float')

    def readCamera(self):
        ret, frame = self.cam.read()
        frame = imutils.resize(frame, self.WIDTH)
            
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.medianBlur(gray,5)
        
        #bananas = banana_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=340, minSize=(55, 55))
        bananas = self.banana_cascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=4, minSize=(40, 40))
    
        for (x,y,w,h) in bananas:
            print((x,y))
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0), 2)
            #soundPlayer.playSound('Banana')
        
        if list(bananas):
            self.bananaFrameCount += 1
            if self.bananaFrameCount >= self.MIN_BANANA_FRAMES and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(soundspath + "Banana.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.6)
        else:
            self.bananaFrameCount = 0
        
        cv2.imshow('frame',frame)

    def run(self):
        while 1:
            if self.ser: 
                self.readSerial()
            if self.cam: 
                self.readCamera()
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                break  # esc to quit
        cv2.destroyAllWindows()


minion_bot = MinionBot()
minion_bot.run()


