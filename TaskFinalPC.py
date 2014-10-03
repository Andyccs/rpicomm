import socket
import jsonpickle

wifiClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wifiClient.connect(("192.168.14.144", 8080))

while True:
	receive_string = wifiClient.recv(1024)
	if(receive_string==''):
		receive_string = wifiClient.recv(1024)

	print receive_string