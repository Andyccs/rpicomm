from bluetooth import *
import logging

class PiBlueTooth:

	def connect(self):
		UUID = "a1513d56-2b38-421d-bee3-4286f12f9866"
		self.client_sock = BluetoothSocket ( RFCOMM )
		btAdd = "08:60:6E:A5:88:E4"
		print("finding service..")
		service_match = find_service(uuid=UUID, address=btAdd)
		while len(service_match) == 0:
			service_match = find_service(uuid=UUID, address=btAdd)
		first_match = service_match[0]
		port = first_match["port"]
		host = first_match["host"]
		self.client_sock.connect((host,port))
		self.isconnected = True



	def close(self):
		self.client_sock.close()
		self.server_sock.close()
		self.isConnected = False
		logging.info('Bluetooth disconnected')

	def send(self,data):
		if self.client_sock == None:
			return None

		try:	
			#self.client_sock.setblocking(1)
			self.client_sock.send(str(data),socket.MSG_WAITALL)
			logging.info('Bluetooth sent data')
		except IOError:
			logging.error('Bluetooth exception')
			raise IOError()

	def receive(self):
		if self.client_sock == None:
			return None

		try:	
			#self.client_sock.setblocking(0)
			data = self.client_sock.recv(1024,socket.MSG_DONTWAIT)
			if len(data)!=0:
				logging.info('Bluetooth received data')
				return data
		except IOError:
			logging.error('Bluetooth exception')
			raise IOError()
