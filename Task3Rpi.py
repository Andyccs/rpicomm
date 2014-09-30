import PiArduino
import time

arduino = PiArduino.PiArduino()
arduino.connect()
time.sleep(2)
arduino.send('B')
temp = arduino.receive()
while temp=='':
	print 'Receive Nothing'
	time.sleep(0.5)
	temp = arduino.receive()

print temp
