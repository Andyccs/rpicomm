import logging
import PiWifi
import PiArduino
import jsonpickle
import socket
import serial
import MessageModel as model
from MessageConverter import PCToArduino, ArduinoToPC

FORMAT = '%(asctime)-15s %(message)s'
LEVEL = logging.DEBUG
#LEVEL = 5
logging.basicConfig(level=LEVEL,format=FORMAT)

wifi = PiWifi.PiWifi("192.168.14.144",8080)
arduino = PiArduino.PiArduino()

while(True):
	try:
		arduino.connect()
		wifi.connect()

		while(True):
			receive_string = wifi.receive()
			receiveDict = jsonpickle.decode(receive_string)
			logging.debug('wifi message: '+str(receiveDict))

			event = receiveDict['event']
			event = event.upper()
			
			# this event came from PC
			# need to send appropriate string to arduino
			# 0: Move forward 0 unit
			# 1: Move forward 1 unit
			# L: Turn left
			# R: Turn right
			if event == 'ACTION':
				logging.debug('sended wifi message to arduino');
				arduino.send(PCToArduino.convert(receiveDict))
				receive_string = arduino.receive()

				logging.debug("Arduino receive: "+receive_string)
				logging.debug('sended arduino message to wifi');

				if(receiveDict['action'] !='INIT' and receiveDict['action']!= 'DIRECT'):
					jsonString = ArduinoToPC.convert(receive_string)
					wifi.send(jsonString)
				else:
					wifi.send('{"event":"MSG","content":"'+receive_string+'"}')

			# these events are came from ANDROID to PC, then to Rpi
			# just forward original message to PC
			elif event == 'EXPLORE' or event == 'START':
				logging.debug('sended wifi message to wifi');
				wifi.send(receive_string)

	except socket.error as msg:
		logging.error('connecting to wifi failed, retrying')
	except serial.SerialException:
		logging.error('connecting to arduino failed, retrying')
	except ValueError as msg:
		logging.error(msg)
	except BaseException as msg:
		logging.error(msg)	
	except Exception as msg:
		logging.error(msg)