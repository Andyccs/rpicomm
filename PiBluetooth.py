from bluetooth import *
import logging

class PiBlueTooth:
	UUID = "00001101-0000-1000-8000-00805F9B34FB"
	ADDR = None
    
    def __init__(self, address):
    	PiBlueTooth.ADDR = address

    	self.server_sock = BluetoothSocket(RFCOMM)
    	self.server_sock.bind(("",ADDR))
    	self.server_sock.listen(10)

    	self.port = self.server_sock.getsockname()[1]

    	advertise_service( self.server_sock, "SampleServer",
                           service_id = PiBlueTooth.UUID,
                           service_classes = [ PiBlueTooth.UUID, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ]
                        )

    	self.client_sock = None
    	self.client_info = None
    	self.isConnected = False

	def connect(self):
		self.client_sock, self.client_info = self.server_sock.accept()
		self.isConnected = True
		logging.info('Bluetooth accepted connection from '+ self.client_info)

	def close(self):
		self.client_sock.close()
		self.server_sock.close()
		self.isConnected = False
		logging.info('Bluetooth disconnected')

	def send(self,data):
		if self.client_sock == None:
			return None

		try:
			self.client_sock.send(str(data))
			logging.info('Bluetooth sent data')
		except IOError:
			logging.error('Bluetooth exception')
			raise IOError()

	def receive(self):
		if self.client_sock == None:
			return None

		try:
			data = self.client_sock.recv(1024)
			if len(data)!=0:
				logging.info('Bluetooth received data')
				return data
		except IOError:
			logging.error('Bluetooth exception')
			raise IOError()
