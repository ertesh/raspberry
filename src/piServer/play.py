#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
import signal
import sys
import os
import io
import picamera
from PIL import Image

class MovementManager:
    def __init__(self):
        self.prepareGPIO()

    def prepareGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(19, GPIO.OUT) #Left (switch) side forward
        GPIO.setup(21, GPIO.OUT) #Left side backward
        GPIO.setup(24, GPIO.OUT) #Right side forward
        GPIO.setup(26, GPIO.OUT) #Right side backward
        self.matrix = [{-1: 21, 1: 19}, {-1: 26, 1: 24}]
        self.revMatrix = { 19: 21, 21: 19, 24: 26, 26: 24}

    def cleanup(self):
        print('Cleanup')
        GPIO.cleanup()
    
    def setGPIO(self, leftDir, rightDir, val):
        if leftDir in self.matrix[0]:
            leftPin = self.matrix[0][leftDir]
            GPIO.output(leftPin, val)
        if rightDir in self.matrix[1]:
            rightPin = self.matrix[1][rightDir]
            GPIO.output(rightPin, val)

    def stop(self):
        self.setGPIO(1, 1, 0)
        self.setGPIO(-1, -1, 0)

    def move_forward(self):
        self.setGPIO(1, 1, 1)

    def move_backward(self):
        self.setGPIO(-1, -1, 1)

    def rotate(self, angle, clockwise):
        FULL_ROTATE = 3
        sleep_time = angle / FULL_ROTATE
        if clockwise:
            left, right = 1, -1
        else:
            left, right = -1, 1
        self.setGPIO(left, right, 1)
        time.sleep(sleep_time)
        self.setGPIO(left, right, 0)

class PhotoManager:
    def make_photo():
        my_stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(2) # Camera warm-up time
            out_dir = '/home/pi/public_html/img/'
            atime = str(datetime.now())
            atime = atime.replace(' ', '_')
            outfile = os.path.join(out_dir, atime + '.jpg')
            #acmd = 'raspistill -w 300 -h 200 -o ' + outfile
            #print acmd
            #os.system(acmd)
            camera.capture(outfile)
            camera.capture(my_stream, format='jpeg')
        my_stream.seek(0)
        im = Image.open(my_stream)
        print(im.format, im.size, im.mode)


def run_program():
    manager = MovementManager()
    while True:
        s = raw_input('--> ')
        if s is 'e':
            break
        if s is 'w':
            manager.move_forward()
        if s is 's':
            manager.move_backward()
        if s is 'a':
            manager.rotate(90, False)
        if s is 'd':
            manager.rotate(90, True)
        #if s is 'q':
        #    make_photo()
    manager.cleanup()


def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    cleanup()
    sys.exit(1)

    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_program()
