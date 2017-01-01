#!/usr/bin/env python
import eventlet
eventlet.monkey_patch()

import io, threading, time
import numpy as np
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, disconnect
from rpm import readrpm
import OLED, BME280

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilistic'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app) 


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        sendrpm(single=True)
        return render_template('index.html')
    else: return ('', 204)


@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method == 'GET':
        try:
            with io.open('history.txt') as histfile:
                history = [ line.rstrip().split(':',1) for line in histfile ]
        except IOError as e:
            history = ''
        return render_template('chat.html', async_mode=socketio.async_mode,hist=history)
    else: return ('', 204)


@socketio.on('chat')
def broadcast_message(msg):
    print msg
    if not(msg['name']) or msg['name'].isspace():
        msg['name'] = 'anonymous'
    entry = u'{}: {}\n'.format(msg['name'], msg['message'])
    with io.open('history.txt', 'a') as histfile:
        histfile.write(entry)
    socketio.emit('chat', msg, broadcast=True)


def sendrpm(single=False):
    while True:
        hist = []
        with eventlet.timeout.Timeout(0.1, False):
            for i in range(10):
                hist.append(readrpm())
        mean = np.mean(hist)
        freq = 1./mean
        OLED.disp_rpm(freq)
        socketio.emit('rpm',freq)
        if single == True: return
        eventlet.sleep(0.01)

def sendatmo(single=False):
    global sealevel_pa
    while True:
        temp, pascals, humidity = BME280.read_all()
        altitude = BME280.calc_altitude(pascals)
        BME280.print_all(temp, pascals, humidity)
        if single == True: return
        eventlet.sleep(1)
        

if __name__ == '__main__':
    eventlet.spawn(sendrpm) 
    eventlet.spawn(sendatmo)
    socketio.run(app, host='0.0.0.0', debug=False)
