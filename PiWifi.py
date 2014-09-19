import socket
import sys
import logging
import threading

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

		self.mutex = threading.Lock()


	def connect(self):
		self.mutex.acquire()
		try:
			if self.isConnected == True:
				return

			try:
				self.socket.bind((self.host, self.port))
				logging.debug('Socket Bind complete')
			except socket.error as msg:
				logging.error('Bind failed, Error Code: ' + str(msg[0]) + ', Message: ' + msg[1])
				raise socket.error()

			self.socket.listen(10)
			logging.debug('Socket Now Listening')

			(self.conn, self.addr) = self.socket.accept()
			logging.info('Connected with:' + self.addr[0] + ':' + str(self.addr[1]) )

			self.isConnected = True
		finally:
			self.mutex.release()

	def close(self):
		self.mutex.acquire()

		try:
			if self.isConnected == False:
				return
				
			self.conn.close()
			self.socket.close()
			isConnected = False
			logging.info('Disconnected')
		finally:
			self.mutex.release()

	def connected(self):
		self.mutex.acquire()
		try:
			return self.isConnected
		finally:
			self.mutex.release()

	def send(self, data):
		self.mutex.acquire()
		try:
			if self.isConnected==False:
				logging.warning('No connection, abort sending data')
				return None

			data = str(data)
			self.conn.send(data.encode('utf-8'))
			logging.debug('Sending data: '+data)
		finally:
			self.mutex.release()

	def receive(self):
		self.mutex.acquire()
		try:
			if self.isConnected==False:
				logging.warning('No connection, abort receiving data')
				return None

			data = self.conn.recv(1024)
			logging.debug('Receiving data: '+data)
			return data.decode('utf-8')
		finally:
			self.mutex.release()
