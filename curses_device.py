# -*- coding: UTF-8 -*-

from curses import wrapper
import curses

class CursesDevice(object):
	
	def run(self, method):
		self.method = method
		wrapper(self._do_run)

	def _do_run(self, abc):
		self.stdscr = curses.initscr()
		curses.curs_set(0)
		self.method()

	def clean(self):
		self.stdscr.clear()

	def point(self, xy):
		self.stdscr.addch(16 - xy[0], xy[1] + 1, curses.ACS_CKBOARD)

	def render(self):
		for x in range(8):
			self.stdscr.addstr(0, x + 1, str(x))
			self.stdscr.addstr(17, x + 1, str(x))
		for y in range(16):
			self.stdscr.addstr(y + 1, 0, str(y % 10))
			self.stdscr.addstr(y + 1, 9, str(y % 10))

		self.stdscr.refresh()

