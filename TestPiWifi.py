import unittest
import logging
import PiWifi
import thread
import time
import socket

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

class TestPiWifi(unittest.TestCase):
	
	wifi = None
	wifiClient = None

	@classmethod
	def setUpClass(cls):
		cls.wifi = PiWifi.PiWifi("localhost",8080)
		thread.start_new_thread(cls.wifi.connect,())

		cls.wifiClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cls.wifiClient.connect(("localhost", 8080))

	def test_precondition(self):
		time.sleep(2)
		self.assertTrue(TestPiWifi.wifi.connected())
 
	def test_send_data(self):
		test_string = "{test send data}"
		TestPiWifi.wifi.send(test_string)
		time.sleep(2)

		receive_string = TestPiWifi.wifiClient.recv(1024)
		self.assertEqual("{test send data}",receive_string)

	def test_receive_data(self):
		test_string = "{test receive data}"
		TestPiWifi.wifiClient.send(test_string.encode('utf-8'))	

		time.sleep(2)
		receive_string = TestPiWifi.wifi.receive()
		self.assertEqual("{test receive data}", receive_string)


	@classmethod
	def tearDownClass(cls):
		if(cls.wifi.connected()):
			cls.wifi.close()

if __name__ == "__main__":
	unittest.main()
