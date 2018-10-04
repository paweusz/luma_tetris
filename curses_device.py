# -*- coding: UTF-8 -*-

from curses import wrapper
import curses

class CursesDevice(object):
	
	def run(self, method):
		self.method = method
		wrapper(self._do_run)

	def _do_run(self, abc):
		self.stdscr = curses.initscr()
		self.method()

	def clean(self):
		self.stdscr.clear()

	def point(self, xy):
		self.stdscr.addstr(16 - xy[0], xy[1] + 1, 'X')

	def render(self):
		for x in range(0,8):
			self.stdscr.addstr(0, x + 1, str(x))
		for y in range(0,16):
			self.stdscr.addstr(y + 1, 0, str(y % 10))
		self.stdscr.refresh()
	


