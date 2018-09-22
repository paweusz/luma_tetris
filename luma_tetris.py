#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, termios, tty, os, time, datetime, random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

class Block:

    def __init__(self, dev):
        self.xy = (0,0)
        self.dev = dev

    def move(self, xy):
        self.xy = (self.xy[0] + xy[0], self.xy[1] + xy[1])

    def transform(self, xy):
        return (15 - xy[1], xy[0])

    def draw(self):
        with canvas(self.dev) as draw:
            draw.point(self.transform(self.xy), fill="white")    

class Rect(Block): 

    def draw(self):
        with canvas(self.dev) as draw:
            draw.rectangle(
                self.transform(self.xy) + self.transform((self.xy[0] + 1, self.xy[1] + 1)),
                outline="white", fill="white")    

class El(Block): 

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0], self.xy[1] + 2)) + self.transform((self.xy[0] + 1, self.xy[1] + 2)),
                fill="white")    

class Line(Block): 

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0], self.xy[1] + 3)),
                fill="white")    

class Zet(Block):

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0] + 1, self.xy[1]))
                 + self.transform((self.xy[0] + 1, self.xy[1] + 1 )) + self.transform((self.xy[0] + 2, self.xy[1] + 1)),
                fill="white")    

class Es(Block):

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform((self.xy[0], self.xy[1] + 1)) + self.transform((self.xy[0] + 1, self.xy[1] + 1))
                 + self.transform((self.xy[0] + 1, self.xy[1])) + self.transform((self.xy[0] + 2, self.xy[1])),
                fill="white")

class Jot(Block):
    
    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform((self.xy[0] + 1, self.xy[1])) + self.transform((self.xy[0] + 1, self.xy[1] + 2))
                 + self.transform((self.xy[0], self.xy[1] + 2)),
                fill="white")

class Te(Block):
    
    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0] + 2, self.xy[1])), fill="white")
            draw.line(
                self.transform((self.xy[0] + 1, self.xy[1])) + self.transform((self.xy[0] + 1, self.xy[1] + 2)), fill="white")

def test_boundries(dev):
    b = Block(dev)

    b.move((0,0))
    b.draw()
    time.sleep(1)

    b.move((7,0))
    b.draw()
    time.sleep(1)

    b.move((0,15))
    b.draw()
    time.sleep(1)
    
    b.move((-7,0))
    b.draw()
    time.sleep(1)

def test_shape(dev):
    r = Te(dev)
    r.draw()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main_loop(dev):
    block = Te(dev)
    block.draw()

    while True:
        ch = getch()

        if (ch == 's'):
            block.move((0,1))
            block.draw()

        if (ch == '8'):
            block.move((0,-1))
            block.draw()

        if (ch == 'd'):
            block.move((1,0))
            block.draw()

        if (ch == 'a'):
            block.move((-1,0))
            block.draw()

        if (ch == 'q'):
            break

def create_device():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,
                     cascaded=2,
                     block_orientation=90,
                     rotate=2)
    return device

if __name__ == "__main__":
    dev = create_device()

    #test_boundries(dev)
    #test_shape(dev)

    main_loop(dev)

    dev.cleanup()
