import Queue
import logging
import threading
import PiWifi
import jsonpickle
import socket
import OutGoingMessageModel as model
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


########################################################33
class wifiThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			try:
				wifi.connect()
				while(True):
					receive_string = wifi.receive()
					receiveDict = jsonpickle.decode(receive_string)
					incomingMessageQueue.put(receiveDict, True)
			except socket.error as msg:
				logging.error('connecting to wifi failed, retrying')
			except ValueError as msg:
				logging.error(msg)

class incomingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			incomingMessage = incomingMessageQueue.get(True)
			logging.debug('consuming incoming message: '+str(incomingMessage))

			event = incomingMessage['event']
			if event == 'ACTION':
				pass
			elif event == 'TASK_FINISH':
				pass
			elif event == 'EXPLORE':
				outgoingMessage = jsonpickle.encode(incomingMessage, unpicklable=False)
				m = model.MessageModel(model.MessageModel.PC, outgoingMessage)
				outgoingMessageQueue.put(m)
				pass
			elif event == 'START':
				pass
			elif event == 'GET_MAP':
				pass

			incomingMessageQueue.task_done()

class outgoingMessageConsumerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while(True):
			outgoingMessage = outgoingMessageQueue.get(True)
			logging.debug('consuming outgoing message: '+str(outgoingMessage))

			if outgoingMessage.to == model.MessageModel.PC :
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