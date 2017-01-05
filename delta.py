# delta.py - gets time between consecutive edges on GPIO

from __future__ import print_function

import pypruss
import os

import mmap
import struct
from time import sleep

PRU_ICSS = 0x4A300000
START = 0x00010000

os.system("config-pin p8.15 pruin")

pypruss.modprobe()                                  # This only has to be called once per boot
pypruss.init()                                      # Init the PRU
pypruss.open(0)                                     # Open PRU event 0 which is PRU0_ARM_INTERRUPT
pypruss.pruintc_init()                              # Init the interrupt controller
pypruss.exec_program(0, "./rpm.bin")                # Load firmware on PRU 0


def read_delta():
    # pypruss.wait_for_event(0)                           # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT

    with open('/dev/mem', 'r+b') as m:
        mem = mmap.mmap( m.fileno(), 512*1024, offset=PRU_ICSS)

        valuestring = mem[START:START+4]
        value = struct.unpack('L', valuestring)[0]
        seconds = value * 0.000000005   # 5ns per cycle

    # pypruss.clear_event(0,pypruss.PRU0_ARM_INTERRUPT)   # Clear the event
    # print(seconds)
    return seconds


if __name__ == "__main__":

    try:
        while True:
            rpm = read_delta()
            print(rpm)

            # sleep(0.1)
    except KeyboardInterrupt as e:
        print(e)
        pypruss.pru_disable(0)                             # Disable PRU 0, this is already done by the firmware
        pypruss.exit()                                     # Exit, don't know what this does.
        print("off")
