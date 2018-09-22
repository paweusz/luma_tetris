#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, termios, tty, os, time, datetime, random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

class Block(object):

    def __init__(self, dev):
        self.xy = (0,0)
        self.rotation = 0
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

class LBlock(Block): 

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0], self.xy[1] + 2)) + self.transform((self.xy[0] + 1, self.xy[1] + 2)),
                fill="white")    

class IBlock(Block): 

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0], self.xy[1] + 3)),
                fill="white")    

class ZBlock(Block):

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform(self.xy) + self.transform((self.xy[0] + 1, self.xy[1]))
                 + self.transform((self.xy[0] + 1, self.xy[1] + 1 )) + self.transform((self.xy[0] + 2, self.xy[1] + 1)),
                fill="white")    

class SBlock(Block):

    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform((self.xy[0], self.xy[1] + 1)) + self.transform((self.xy[0] + 1, self.xy[1] + 1))
                 + self.transform((self.xy[0] + 1, self.xy[1])) + self.transform((self.xy[0] + 2, self.xy[1])),
                fill="white")

class JBlock(Block):
    
    def draw(self):
        with canvas(self.dev) as draw:
            draw.line(
                self.transform((self.xy[0] + 1, self.xy[1])) + self.transform((self.xy[0] + 1, self.xy[1] + 2))
                 + self.transform((self.xy[0], self.xy[1] + 2)),
                fill="white")

class TBlock(Block):

    def __init__(self, dev):
        super(TBlock, self).__init__(dev)
        self._points = [[(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (1, 1), (2, 1), (1, 2)]]

    def draw(self):
        with canvas(self.dev) as draw:
            for i in range(4):
                draw.point(self.transform(
                    (self.xy[0] + self._points[self.rotation][i][0],
                     self.xy[1] + self._points[self.rotation][i][1])),
                           fill="white")

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
    block = TBlock(dev)
    block.draw()

    while True:
        ch = getch()

        if (ch == ' '):
            block.rotation = block.rotation - 1
            if (block.rotation == -1):
                block.rotation = 3
            block.draw()

        if (ch == 's'):
            block.move((0,1))
            block.draw()

        if (ch == 'w'):
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
