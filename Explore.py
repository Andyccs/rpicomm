import Queue
import logging
import threading
import PiWifi
import jsonpickle
import socket
import OutGoingMessageModel as model
import time
from MessageConverter import PCToArduino, ArduinoToPC
# import PiArduino
# import PiBluetooth

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL,format=FORMAT)

# elements in this queue are dictionary
# each dictionary must have an "event" key/value pair
incomingMessageQueue = Queue.Queue()
outgoingMessageQueue = Queue.Queue()

wifi = PiWifi.PiWifi("localhost",8080)
# arduino = PiArduino.PiArduino()

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
						receive_string = wifi.receive()
					logging.log(5,'receiving from arduino end')

					jsonString = ArduinoToPC.convert(receive_string)

					#put with blocking=True
					incomingMessageQueue.put(jsonString, True)

			except Serial.SerialException:
				logging.error('connecting to arduino failed, retrying')

class incomingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			incomingMessage = incomingMessageQueue.get(True)
			logging.debug('consuming incoming message: '+str(incomingMessage))

			event = incomingMessage['event']
			
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
				self.__forwardMessage(incomingMessage, model.MessageModel.PC)

			# these events are came from ANDROID
			# just forward them to PC
			elif event == 'EXPLORE' or event == 'START':
				self.__forwardMessage(incomingMessage, model.MessageModel.PC)

			# this event came from ANDROID
			# need to send latest map info to PC
			elif event == 'GET_MAP':
				self.__forwardMessage(incomingMessage, model.MessageModel.PC)

			# this event came from PC
			# need to forward to ANDROID
			elif event == 'MAP':
				self.__forwardMessage(incomingMessage, model.MessageModel.ANDROID)

			incomingMessageQueue.task_done()
	def __forwardMessage(self, incomingMessage, to):
		outgoingMessage = jsonpickle.encode(incomingMessage, unpicklable=False)
		m = model.MessageModel(to, outgoingMessage)
		outgoingMessageQueue.put(m)

class outgoingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			outgoingMessage = outgoingMessageQueue.get(True)
			logging.debug('consuming outgoing message: '+str(outgoingMessage))

			if outgoingMessage.to == model.MessageModel.PC :
				logging.log(5,'sending to pc through wifi')
				wifi.send(outgoingMessage.message)
				logging.log(5,'after sending')
				pass
			elif outgoingMessage.to == model.MessageModel.ANDROID :
				pass
			elif outgoingMessage.to == model.MessageModel.ARDUINO :
				pass

			outgoingMessageQueue.task_done()


###################################################

wifiThread = wifiThread()
incomingMessageConsumerThread = incomingMessageConsumerThread()
outgoingMessageConsumerThread = outgoingMessageConsumerThread()

wifiThread.start()
incomingMessageConsumerThread.start()
outgoingMessageConsumerThread.start()