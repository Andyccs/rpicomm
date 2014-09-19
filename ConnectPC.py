import PiWifi
import thread
import socket
import logging

#Edited by Andy

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)


wifi = PiWifi.PiWifi("192.168.1.1",8888)
wifi.connect()

assert wifi.connected()

while True:
	receive_string = wifi.receive()
	print receive_string