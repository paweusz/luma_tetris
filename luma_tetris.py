#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, termios, tty, os, time, datetime, random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from threading import Timer

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
            for i in range(4):
                draw.point(self.transform(
                    (self.xy[0] + self._points[self.rotation][i][1],
                     self.xy[1] + self._points[self.rotation][i][0])),
                           fill="white")

class OBlock(Block): 

    def __init__(self, dev):
        super(OBlock, self).__init__(dev)
        self._points = [[(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]]

class LBlock(Block): 

    def __init__(self, dev):
        super(LBlock, self).__init__(dev)
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 0)]]

class IBlock(Block): 

    def __init__(self, dev):
        super(IBlock, self).__init__(dev)
        self._points = [[(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)]]

class ZBlock(Block):

    def __init__(self, dev):
        super(ZBlock, self).__init__(dev)
        self._points = [[(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)]]
        
class SBlock(Block):

    def __init__(self, dev):
        super(SBlock, self).__init__(dev)
        self._points = [[(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]]

class JBlock(Block):
    
    def __init__(self, dev):
        super(JBlock, self).__init__(dev)
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 0)]]

class TBlock(Block):

    def __init__(self, dev):
        super(TBlock, self).__init__(dev)
        self._points = [[(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (1, 1), (2, 1), (1, 2)]]

class Game:

    def __init__(self, dev):
        self.block_idx = 0
        self.blocks = [OBlock(dev), LBlock(dev), IBlock(dev), ZBlock(dev), SBlock(dev), JBlock(dev), TBlock(dev)]
        self.timer = Timer(1, self._tick)
        self._tick()

    def _tick(self):
        block = self.blocks[self.block_idx]
        block.move((0,1))
        block.draw()

        self.timer = Timer(1, self._tick)
        self.timer.start()

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def main_loop(self):
        while True:
            block = self.blocks[self.block_idx]
            block.draw()

            ch = self.getch()

            if (ch == ' '):
                block.rotation = block.rotation - 1
                if (block.rotation == -1):
                    block.rotation = 3

            if (ch == 'c'):
                self.block_idx = self.block_idx + 1
                if (self.block_idx == 7):
                    self.block_idx = 0

            if (ch == 's'):
                block.move((0,1))

            if (ch == 'w'):
                block.move((0,-1))

            if (ch == 'd'):
                block.move((1,0))

            if (ch == 'a'):
                block.move((-1,0))

            if (ch == 'q'):
                self.timer.cancel()
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

    game = Game(dev)
    game.main_loop()

    dev.cleanup()
