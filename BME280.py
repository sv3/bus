from Adafruit_BME280 import *
import time

def calc_altitude(pressure, sealevel_pa=101325.0):
    altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
    return altitude

sensor = BME280(mode=BME280_OSAMPLE_8, busnum=2)

def read_all():
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    humidity = sensor.read_humidity()
    return (degrees, pascals, humidity)

def print_all(degrees, pascals, humidity):
    hectopascals = pascals / 100
    altitude = calc_altitude(pascals)
    print 'Timestamp = {0:0.3f}'.format(time.time())
    print 'Temp      = {0:0.3f} deg C'.format(degrees)
    print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
    print 'Humidity  = {0:0.2f} %'.format(humidity)
    print 'Altitude  = {0:0.2f} m'.format(altitude)

if __name__ == '__main__':
    print_all(*read_all())
