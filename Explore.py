import Queue
import logging
import threading
import PiWifi
import PiArduino
import PiBluetooth
import jsonpickle
import socket
import serial
import bluetooth
import MessageModel as model
import time
from MessageConverter import PCToArduino, ArduinoToPC


FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL,format=FORMAT)

# elements in this queue are dictionary
# each dictionary must have an "event" key/value pair
incomingMessageQueue = Queue.Queue()
outgoingMessageQueue = Queue.Queue()

wifi = PiWifi.PiWifi("192.168.14.144",8080)
arduino = PiArduino.PiArduino()
bluetooth = PiBluetooth.PiBluetooth()

########################################################33
class wifiThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				wifi.connect()
				while(True):
					logging.log(5,'receiving from wifi')
					

					receive_string = wifi.receive()
					while(receive_string == ''):
						logging.log(5,'give up receiving from wifi')
						time.sleep(0.5)
						receive_string = wifi.receive()
					logging.log(5,'receiving from wifi end')

					receiveDict = jsonpickle.decode(receive_string)

					#put with blocking=True
					incomingMessageQueue.put(receiveDict, True)
			except socket.error as msg:
				logging.error('connecting to wifi failed, retrying')
			except ValueError as msg:
				logging.error(msg)

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
					jsonString = ArduinoToPC.convert(receive_string)
					logging.log(5,"Arduino thread converted to json: "+jsonString)

					#put with blocking=True
					incomingMessageQueue.put(jsonString, True)

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

					receiveDict = jsonpickle.decode(receive_string)

					#put with blocking=True
					incomingMessageQueue.put(receiveDict, True)
			except bluetooth.BluetoothError:
				logging.error('connecting to bluetooth failed, retrying')
			except bluetooth.IOError:
				logging.error('IOError occurred')
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

				event = incomingMessage['event']
				event = event.upper()
				
				# this event came from PC
				# need to send appropriate string to arduino
				# 0: Move forward 0 unit
				# 1: Move forward 1 unit
				# L: Turn left
				# R: Turn right
				if event == 'ACTION':
					outgoingMessageQueue.put(PCToArduino.convert(incomingMessage))

				# this event came from Arduino
				# need to send appropriate string to PC
				elif event == 'TASK_FINISH':
					self.__forwardMessage(incomingMessage, model.OutGoing.PC)

				# these events are came from ANDROID
				# just forward them to PC
				elif event == 'EXPLORE' or event == 'START':
					self.__forwardMessage(incomingMessage, model.OutGoing.PC)

				# this event came from ANDROID
				# need to send latest map info to PC
				elif event == 'GET_MAP':
					self.__forwardMessage(incomingMessage, model.OutGoing.PC)

				# this event came from PC
				# need to forward to ANDROID
				elif event == 'MAP':
					self.__forwardMessage(incomingMessage, model.OutGoing.ANDROID)

				incomingMessageQueue.task_done()
			except BaseException as msg:
				logging.error(msg)	

	def __forwardMessage(self, incomingMessage, to):
		outgoingMessage = jsonpickle.encode(incomingMessage, unpicklable=False)
		m = model.OutGoing(to, outgoingMessage)
		outgoingMessageQueue.put(m)

class outgoingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				outgoingMessage = outgoingMessageQueue.get(True)
				logging.debug('consuming outgoing message: '+str(outgoingMessage))

				if outgoingMessage.to == model.OutGoing.PC :
					logging.log(5,'sending to pc through wifi')
					wifi.send(outgoingMessage.message)
					logging.log(5,'after sending to pc through wifi')
				elif outgoingMessage.to == model.OutGoing.ANDROID :
					logging.log(5,'sending to android through bluetooth')
					bluetooth.send(outgoingMessage.message)
					logging.log(5,'after sending to android through bluetooth')
				elif outgoingMessage.to == model.OutGoing.ARDUINO :
					logging.log(5,'sending to arduino through serial')
					arduino.send(outgoingMessage.message)
					logging.log(5,'after sending to arduino through serial')
					pass

				outgoingMessageQueue.task_done()
			except BaseException as msg:
				logging.error(msg)	



###################################################

wifiThread = wifiThread()
arduinoThread = arduinoThread()
bluetoothThread = bluetoothThread()

incomingMessageConsumerThread = incomingMessageConsumerThread()
outgoingMessageConsumerThread = outgoingMessageConsumerThread()

wifiThread.start()
arduinoThread.start()
bluetoothThread.start()

incomingMessageConsumerThread.start()
outgoingMessageConsumerThread.start()
