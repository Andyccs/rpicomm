import unittest
import logging
import PiBluetooth
import thread
import time
from bluetooth import *

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

class TestPiBluetooth(unittest.TestCase):

	bt1 = None
	bt2 = None

	@classmethod
	def setUpClass(cls):
		cls.bt1 = PiBluetooth.PiBluetooth(4)