#!/usr/bin/env python
import eventlet
eventlet.monkey_patch()

import io, threading, time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, disconnect
from rpm import readrpm
import OLED

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilistic'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app) 

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else: return ('', 204)


def sendrpm():
    seconds_prev = None
    while True:
        seconds = readrpm()
        freq = 1./seconds
        OLED.disp_rpm(freq)
        # print( r'{} seconds'.format(seconds) )
        if seconds != seconds_prev:
            socketio.send(freq)
            seconds_prev = seconds
        eventlet.sleep(0.05)
    return


if __name__ == '__main__':
    eventlet.spawn(sendrpm) 
    socketio.run(app, host='0.0.0.0')
