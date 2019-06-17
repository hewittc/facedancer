#!/usr/bin/env python3
#
# facedancer-microlan.py

from facedancer import FacedancerUSBApp
from USBMicroLAN import *

class DS1996(OneWireDevice):
    """
        64 kB Memory iButton
    """

    def __init__(self, serial, verbose=0):
        OneWireDevice.__init__(self, b'\x0c', serial, verbose)

        self.sram = [[b'\xff'] * 256] * 256
        self.scratch = [b'\x00'] * 256


u = FacedancerUSBApp(verbose=6)
b = [ DS1996(b'\x47\x54\x46\x4f\x21\x21', verbose=6) ]
d = USBMicroLANDevice(u, b, verbose=6)

d.connect()

try:
    d.run()
# SIGINT raises KeyboardInterrupt
except KeyboardInterrupt:
    d.disconnect()

