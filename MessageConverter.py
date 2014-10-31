import MessageModel as model

class PCToArduino:
	@staticmethod
	def convert(incomingMessage):
		outgoingMessage = ""
		if incomingMessage['action']=='GO' :
			if incomingMessage['quantity']<=0 :
				outgoingMessage = '0'
			elif incomingMessage['quantity']==1:
				outgoingMessage = '1'
			elif incomingMessage['quantity']==2:
				outgoingMessage = '2'
			elif incomingMessage['quantity']==3:
				outgoingMessage = '3'
			elif incomingMessage['quantity']==4:
				outgoingMessage = '4'	
			elif incomingMessage['quantity']==5:
				outgoingMessage = '5'
			elif incomingMessage['quantity']==6:
				outgoingMessage = '6'
			elif incomingMessage['quantity']==7:
				outgoingMessage = '7'
			elif incomingMessage['quantity']==8:
				outgoingMessage = '8'	
			elif incomingMessage['quantity']==9:
				outgoingMessage = '9'

		elif incomingMessage['action']=='ROTATE' :
			if incomingMessage['quantity'] > 0 : 
				outgoingMessage = 'R'
			elif incomingMessage['quantity'] < 0 :
				outgoingMessage = 'L'
			else:
				outgoingMessage = '0'
		elif incomingMessage['action']=='KELLY':
			outgoingMessage = 'C'
		else:
			logging.debug('incoming message contains unknown action, sending move 0')
			outgoingMessage = '0'
		return outgoingMessage

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
