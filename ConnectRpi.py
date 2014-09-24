import socket

wifiClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wifiClient.connect(("localhost", 8080))
wifiClient.send('{"event":"EXPLORE"}')	
wifiClient.send('{"event":"ACTION","action":"GO","quantity":1}')
wifiClient.send('{"event":"ACTION","action":"ROTATE","quantity":1}')