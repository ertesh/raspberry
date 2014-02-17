#!/usr/bin/python
import io
import time
import picamera
from PIL import Image

my_stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2) # Camera warm-up time
    camera.capture('foo.jpg')
    camera.capture(my_stream, format='jpeg')

# "Rewind" the stream to the beginning so we can read its content
my_stream.seek(0)
im = Image.open(my_stream)

print im.format, im.size, im.mode
