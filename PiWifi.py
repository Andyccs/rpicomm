import socket
import sys
import logging

class PiWifi:

	def __init__(self, host, port):
		# do some checking for the inputs
		assert host != None, "Host is None"
		assert type(port) is int, "port is not an integer: %r" % id

		# initialization
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.isConnected = False

		self.conn = None
		self.address = None

	def connect(self):
		if self.isConnected == True:
			return

		try:
			self.socket.bind((self.host, self.port))
			logging.log(5, 'Socket Bind complete')
		except socket.error as msg:
			logging.error('Bind failed, Error Code: ' + str(msg[0]) + ', Message: ' + msg[1])
			raise socket.error()

		self.socket.listen(10)
		logging.debug('Socket Now Listening')

		self.socket.setblocking(True)
		(self.conn, self.addr) = self.socket.accept()
		logging.info('Connected with:' + self.addr[0] + ':' + str(self.addr[1]) )

		self.isConnected = True

	def close(self):
		if self.isConnected == False:
			return

		self.conn.close()
		self.socket.close()
		isConnected = False
		logging.info('Disconnected')

	def connected(self):
		return self.isConnected

	def send(self, data):
		if self.isConnected==False:
			logging.warning('No wifi connection, abort sending data')
			return None

		data = str(data)
		self.conn.send(data.encode('utf-8'))
		logging.debug('Sending data: '+data)

	def receive(self):
		if self.isConnected==False:
			logging.warning('No connection, abort receiving data')
			return None

		result = ""
		data = self.conn.recv(1)
		result += data
		while(data!='}'):
			data = self.conn.recv(1)
			result += data

		logging.log(5, 'Receiving data: '+result)
		return result.decode('utf-8')
