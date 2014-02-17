#!/usr/bin/python

from datetime import datetime
import os
import time

def run():
    out_dir = '/home/pi/public_html/img/'
    atime = str(datetime.now())
    atime = atime.replace(' ', '_')
    outfile = os.path.join(out_dir, atime + '.jpg')
    acmd = 'raspistill -w 300 -h 200 -o ' + outfile
    print acmd
    os.system(acmd)

for i in range(3):
    run()
    time.sleep(1)
