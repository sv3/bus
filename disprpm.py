#!/usr/bin/env python
#import eventlet
#eventlet.monkey_patch()

import io, threading, time
from rpm import readrpm
import OLED

def sendrpm():
    seconds_prev = None
    while True:
        seconds = readrpm()
        freq = 1./seconds
        OLED.disp_rpm(freq)
        # print( r'{} seconds'.format(seconds) )
        # eventlet.sleep(0.1)
    return


if __name__ == '__main__':
    #eventlet.spawn(sendrpm) 
    sendrpm()

