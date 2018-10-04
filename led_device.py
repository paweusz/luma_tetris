from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

class LedDevice(object):

	def __init__(self):
		serial = spi(port=0, device=0, gpio=noop())
		self.device = max7219(serial,
		                 cascaded=2,
		                 block_orientation=90,
		                 rotate=2)

	def point(self, xy):
		self.device.point(xy, fill="white")


