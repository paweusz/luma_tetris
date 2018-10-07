#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, termios, tty, os, time, datetime, random

from curses_device import CursesDevice
from blocks import *
from scene import Scene

from threading import Timer

class Game:

    def __init__(self, dev):
        self.blocks = [OBlock, LBlock, IBlock, ZBlock, SBlock, JBlock, TBlock]

        self.scene = Scene(dev, (8,16))
        self.block = self.random_block()
        self.scene.set_current_block(self.block)
        
    def tick(self):
        if (not self.move_block((0,1))):
            self.scene.hydrate_block(self.block)
            self.scene.process_lines()
            self.block = self.random_block()
            self.scene.set_current_block(self.block)

        self.scene.render()

        self.timer = Timer(1, self.tick)
        self.timer.start()

    def move_block(self, xy):
        self.block.move(xy)
        if (self.scene.collides(self.block)):
            self.block.move((-xy[0], -xy[1]))
            return False
        return True

    def random_block(self):
        block_idx = random.randint(0,len(self.blocks)-1)
        return self.blocks[block_idx]()

    def main_loop(self):
    	self.tick()
    
        while True:
            ch = self.getch()

            if (ch == ' '):
                self.block.rotation = self.block.rotation - 1
                if (self.block.rotation == -1):
                    self.block.rotation = 3

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

if __name__ == "__main__":
    dev = CursesDevice()

    game = Game(dev)
    dev.run(game.main_loop)


