import PiBluetooth
import logging
import jsonpickle

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

bt = PiBluetooth.PiBluetooth()
bt.connect()

while True:
	receive_string = bt.receive()
	receiveDict = jsonpickle.decode(receive_string)
	print receiveDict['message']
