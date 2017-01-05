#!/usr/bin/env python
import eventlet
# eventlet.monkey_patch()

import io, threading, time, csv, numpy
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, disconnect
from delta import read_delta
import OLED, BME280

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilistic'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app) 


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
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
    name, message = msg['name'], msg['message']

    if not(name) or name.isspace(): name = 'anonymous'

    socketio.emit('chat', msg, broadcast=True)

    with io.open('history.txt', 'a') as histfile:
        histfile.write( u'{}: {}\n'.format(name, message) )


def sendrpm(single=False):
    while True:
        rpmsum = 0
        with eventlet.timeout.Timeout(0.1, False):
            for i in range(10):
                rpmsum += read_delta()
        mean = rpmsum / 10
        freq = 1./mean
        OLED.disp_rpm(freq)
        socketio.emit('rpm',freq)

        if single == True: return
        eventlet.sleep(0.01)


def sendatmo(single=False):
    sensor = BME280.sensor
    n = 50    # number of samples to average
    while True:
        starttime = time.time()
        pressure_sum = 0

        # read pressure samples for averaging
        for i in range(n):
            pressure_sum += sensor.read_pressure()

        timestamp = time.time()
        temp, humidity = sensor.read_temperature(), sensor.read_humidity()
        pascals = pressure_sum / n

        socketio.emit('atmo', { 'temperature':temp, 'pressure':pascals, 'humidity':humidity })

        with open('atmolog.tsv', 'a') as atmolog:
            w = csv.writer(atmolog, delimiter='\t')
            w.writerow([timestamp, temp, pascals, humidity])

        if single == True: return
        eventlet.sleep(5 - starttime % 5)


if __name__ == '__main__':
    eventlet.spawn(sendrpm) 
    eventlet.spawn(sendatmo)
    socketio.run(app, host='0.0.0.0', debug=False)
