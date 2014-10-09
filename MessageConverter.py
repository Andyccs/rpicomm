import MessageModel as model

class PCToArduino:
	@staticmethod
	def convert(incomingMessage):
		outgoingMessage = ""
		if incomingMessage['action']=='GO' :
			if incomingMessage['quantity']<=0 :
				outgoingMessage = '0'
			else:
				outgoingMessage = '1'
		elif incomingMessage['action']=='ROTATE' :
			if incomingMessage['quantity'] > 0 : 
				outgoingMessage = 'R'
			elif incomingMessage['quantity'] < 0 :
				outgoingMessage = 'L'
			else:
				outgoingMessage = '0'
		else:
			logging.debug('incoming message contains unknown action, sending move 0')
			outgoingMessage = '0'
		m = model.OutGoing(model.OutGoing.ARDUINO, outgoingMessage)
		return m

class ArduinoToPC:
	@staticmethod
	def convert(serialInput):
		information = serialInput.split(',');
		status = information[0]
		if(status=='1'):
			status = 'TASK_FINISH'
		information.pop(0)
		sensors = ','.join(information)

		jsonString = '{"event":"'+status+'","sensors":['+sensors+']}'

		return jsonString