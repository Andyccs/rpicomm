import PiArduino

arduino = PiArduino.PiArduino()
arduino.connect()
time.sleep(2)
arduino.send('A')
temp = arduino.receive()

print temp