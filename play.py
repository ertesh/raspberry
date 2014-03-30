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

def prepare():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(19, GPIO.OUT) #Left (switch) side forward
    GPIO.setup(21, GPIO.OUT) #Left side backward
    GPIO.setup(24, GPIO.OUT) #Right side forward
    GPIO.setup(26, GPIO.OUT) #Right side backward

def cleanup():
    print 'Cleanup'
    GPIO.cleanup()

def go(x, y):
    print x, y
    sleep_time = 0.75
    if x == -1:
        GPIO.output(19, 1)
        GPIO.output(24, 1)
        time.sleep(sleep_time)
        GPIO.output(19, 0)
        GPIO.output(24, 0)
    if x == 1:
        GPIO.output(21, 1)
        GPIO.output(26, 1)
        time.sleep(sleep_time)
        GPIO.output(21, 0)
        GPIO.output(26, 0)
    if y == 1:
        GPIO.output(19, 1)
        GPIO.output(26, 1)
        time.sleep(sleep_time)
        GPIO.output(19, 0)
        GPIO.output(26, 0)
    if y == -1:
        GPIO.output(21, 1)
        GPIO.output(24, 1)
        time.sleep(sleep_time)
        GPIO.output(21, 0)
        GPIO.output(24, 0)

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
    print im.format, im.size, im.mode

def run_program():
    prepare()
    while True:
        s = raw_input('--> ')
        if s is 'e':
            break
        if s is 'w':
            go(1, 0)
        if s is 's':
            go(-1, 0)
        if s is 'a':
            go(0, -1)
        if s is 'd':
            go(0, 1)
        if s is 'q':
            make_photo()
    cleanup()


def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    cleanup()
    sys.exit(1)

    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_program()
