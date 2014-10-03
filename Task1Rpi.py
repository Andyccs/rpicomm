"""
Manual Testing to allow PC to connect to RPi
"""
import PiWifi
import thread
import socket
import logging
import jsonpickle

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)


wifi = PiWifi.PiWifi("192.168.14.144",8080)
wifi.connect()

assert wifi.connected()

while True:
	receive_string = wifi.receive()
	receiveDict = jsonpickle.decode(receive_string)
	print receiveDict['message']