#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import time
import random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.render import canvas

class block:

    def __init__(self, dev):
        self.xy = (0,0)
        self.dev = dev

    def move(self, xy):
        self.xy = (self.xy[0] + xy[0], self.xy[1] + xy[1])

    def draw(self):
        with canvas(self.dev) as draw:
            draw.point(self.xy, fill="white")    
    
def create_device():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,
                     cascaded=2,
                     block_orientation=90,
                     rotate=2)
    return device

if __name__ == "__main__":
    dev = create_device()

    b = block(dev)
    b.move((7,7))
    b.draw()

    time.sleep(1)
    dev.cleanup()
