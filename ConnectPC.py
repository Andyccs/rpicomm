"""
Manual Testing to allow PC to connect to RPi
"""
import PiWifi
import thread
import socket
import logging

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL,format=FORMAT)


wifi = PiWifi.PiWifi("0.0.0.0",8000)
wifi.connect()

assert wifi.connected()

while True:
	receive_string = wifi.receive()
	print receive_string