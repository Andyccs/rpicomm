import PiBluetooth
import logging
import jsonpickle
import time

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

bt = PiBluetooth.PiBluetooth()
bt.connect()

while True:
	receive_string = bt.receive()
	while receive_string=='':
		time.sleep(0.5)
		receive_string = bt.receive()
	receiveDict = jsonpickle.decode(receive_string)
	print receiveDict['message']
