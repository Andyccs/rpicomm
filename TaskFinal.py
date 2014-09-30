# A character sent from N7 will be transferred to Arduino which increment 
# it by 1, and then route to the PC through Wifi for display.

import Queue
import logging
import threading
import PiWifi
import PiArduino
import PiBluetooth
import socket
import serial
import bluetooth
import MessageModel as model
import time


FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL,format=FORMAT)

wifi = PiWifi.PiWifi("192.168.14.144",8080)
arduino = PiArduino.PiArduino()
bluetooth = PiBluetooth.PiBluetooth()

# elements in this queue are dictionary
# each dictionary must have an "event" key/value pair
incomingMessageQueue = Queue.Queue()

########################################################33
class wifiThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				wifi.connect()
			except socket.error as msg:
				logging.error('connecting to wifi failed, retrying')

class arduinoThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				arduino.connect()
				while(True):
					logging.log(5,'receiving from arduino')
					receive_string = arduino.receive()
					while(receive_string == ''):
						logging.log(5,'give up receiving from arduino')
						time.sleep(0.5)
						receive_string = arduino.receive()
					logging.log(5,'receiving from arduino end')

					logging.log(5,"Arduino thread receive: "+receive_string)
					
					# here, I will receive only one character
					message = {"to":"pc","message":receive_string}

					#put with blocking=True
					incomingMessageQueue.put(message, True)

			except serial.SerialException:
				logging.error('connecting to arduino failed, retrying')

class bluetoothThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				bluetooth.connect()
				while(True):
					logging.log(5,'receiving from bluetooth')
					receive_string = bluetooth.receive()
					while(receive_string == ''):
						logging.log(5,'give up receiving from bluetooth')
						time.sleep(0.5)
						receive_string = bluetooth.receive()
					logging.log(5,'receiving from bluetooth end')

					# here, I will receive only one character
					messageDict = {"to":"arduino","message":receive_string}

					#put with blocking=True
					incomingMessageQueue.put(messageDict, True)
			except bluetooth.BluetoothError:
				logging.error('connecting to bluetooth failed, retrying')
			except ValueError as msg:
				logging.error(msg)

class incomingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				incomingMessage = incomingMessageQueue.get(True)
				logging.debug('consuming incoming message: '+str(incomingMessage))

				event = incomingMessage['to']
				
				if to == 'arduino':
					arduino.send(event['message'])
				elif event == 'pc':
					wifi.send(event['message'])

				incomingMessageQueue.task_done()
			except BaseException as msg:
				logging.error(msg)	

###################################################

wifiThread = wifiThread()
arduinoThread = arduinoThread()
bluetoothThread = bluetoothThread()
incomingMessageConsumerThread = incomingMessageConsumerThread()

wifiThread.start()
arduinoThread.start()
bluetoothThread.start()
incomingMessageConsumerThread.start()