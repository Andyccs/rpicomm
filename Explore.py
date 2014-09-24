import Queue
import logging
import threading
import PiWifi
import jsonpickle

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL,format=FORMAT)

incomingMessageQueue = Queue.Queue()
outgoingMessageQueue = Queue.Queue()

wifi = PiWifi.PiWifi("localhost",8080)

class wifiThread (threading.Thread):
	while(True):
		try:
			wifi.connect()
			while(True):
				receive_string = wifi.receive()
				thawed = jsonpickle.decode(receive_string)
		except socket.error as msg:
			logging.error('Bind failed, Error Code: ' + str(msg[0]) + ', Message: ' + msg[1])
	


def main():
	pass