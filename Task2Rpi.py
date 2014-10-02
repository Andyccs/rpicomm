import PiWifi
import logging

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)

bt = PiBluetooth.PiBluetooth()
bt.connect()

while True:
        receive_string = bt.receive()
        print receive_string
