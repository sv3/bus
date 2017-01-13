import Adafruit_BBIO.GPIO as GPIO


def init():
    LEDstate = [0,0,0,0]
    for i in range(4):
        GPIO.setup("USR%i" % i, GPIO.OUT)
        GPIO.output("USR%i" % i, LEDstate[i])

if __name__ == '__main__':
    init()
