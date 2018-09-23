#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, termios, tty, os, time, datetime, random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from threading import Timer

class Block(object):

    def __init__(self):
        self.xy = (0,0)
        self.rotation = 0

    def move(self, xy):
        self.xy = (self.xy[0] + xy[0], self.xy[1] + xy[1])

    def transform(self, xy):
        return (15 - xy[1], xy[0])

    def get_xy(self, point_idx):
        return (self._points[self.rotation][point_idx][1] + self.xy[0],
                self._points[self.rotation][point_idx][0] + self.xy[1])

    def render(self, draw):
        for i in range(4):
            draw.point(self.transform(
                (self.xy[0] + self._points[self.rotation][i][1],
                 self.xy[1] + self._points[self.rotation][i][0])),
                       fill="white")

class OBlock(Block): 

    def __init__(self):
        super(OBlock, self).__init__()
        self._points = [[(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]]

class LBlock(Block): 

    def __init__(self):
        super(LBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 0)]]

class IBlock(Block): 

    def __init__(self):
        super(IBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)]]

class ZBlock(Block):

    def __init__(self):
        super(ZBlock, self).__init__()
        self._points = [[(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)]]
        
class SBlock(Block):

    def __init__(self):
        super(SBlock, self).__init__()
        self._points = [[(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]]

class JBlock(Block):
    
    def __init__(self):
        super(JBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 0)]]

class TBlock(Block):

    def __init__(self):
        super(TBlock, self).__init__()
        self._points = [[(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (1, 1), (2, 1), (1, 2)]]

class Scene:

    def __init__(self, dev):
        self.blocks = []
        self.dev = dev

    def add_block(self, block):
        self.blocks.append(block)

    def render(self):
        with canvas(self.dev) as draw:
            for block in self.blocks:
                block.render(draw)

    def does_collide(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)

            if (my_xy[0] == 8 or my_xy[0] == -1 or my_xy[1] == 16 or my_xy[1] == -1):
                return True
            
            for b in self.blocks:
                if (b != block):
                    for other_i in range(4):
                        other_xy = b.get_xy(other_i)
                        if (other_xy == my_xy):
                            return True
        return False

class Game:

    def __init__(self, dev):
        self.block_idx = 0
        self.blocks = [OBlock, LBlock, IBlock, ZBlock, SBlock, JBlock, TBlock]

        self.scene = Scene(dev)
        self.block = self.blocks[self.block_idx]()
        self.scene.add_block(self.block)
        
        self._tick()

    def _tick(self):
        if (not self.move_block((0,1))):
            self.block = self.blocks[self.block_idx]()
            self.scene.add_block(self.block)

        self.scene.render()

        self.timer = Timer(1, self._tick)
        self.timer.start()

    def move_block(self, xy):
        self.block.move(xy)
        if (self.scene.does_collide(self.block)):
            self.block.move((-xy[0], -xy[1]))
            return False
        return True

    def main_loop(self):
        while True:
            ch = self.getch()

            if (ch == ' '):
                self.block.rotation = self.block.rotation - 1
                if (self.block.rotation == -1):
                    self.block.rotation = 3

            if (ch == 'c'):
                self.block_idx = self.block_idx + 1
                if (self.block_idx == 7):
                    self.block_idx = 0

            if (ch == 's'):
                self.move_block((0,1))

            if (ch == 'w'):
                self.move_block((0,-1))

            if (ch == 'd'):
                self.move_block((1,0))

            if (ch == 'a'):
                self.move_block((-1,0))

            if (ch == 'q'):
                self.timer.cancel()
                break

            self.scene.render()

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

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
