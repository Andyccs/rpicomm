import unittest
import logging
import PiArduino
import thread
import time

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

class TestPiArduino(unittest.TestCase):

	arduino = None

	@classmethod
	def setUpClass(cls):
		cls.arduino = PiArduino.PiArduino()
		cls.arduino.connect()
		time.sleep(2)

	def test_precondition(self):
		self.assertTrue(self.arduino!=None)
		self.assertTrue(self.arduino.isConnected)

	def test_integration(self):
		#this test assume that the arduino will 
		#always send back "hello\r\n" when an integer 
		#is sent to the arduino

		# TODO this test need to be revise
		# self.arduino.send('3')
		# time.sleep(1)
		# temp = self.arduino.receive()
		# self.assertEqual("hello\r\n",temp)
		pass

	@classmethod
	def tearDownClass(cls):
		if(cls.arduino.isConnected):
			cls.arduino.close()

if __name__ == "__main__":
	unittest.main()