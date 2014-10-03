import socket

wifiClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wifiClient.connect(("192.168.14.144", 8080))
wifiClient.send('{"message":"A"}')



# wifiClient.send('{"event":"EXPLORE"}')
# wifiClient.send('{"event":"ACTION","action":"GO","quantity":1}')
# wifiClient.send('{"event":"ACTION","action":"ROTATE","quantity":1}')