import serial
import logging


class PiArduino:
    def __init__(self):
        self.ser = None
        self.isConnected = False

    def connect(self):
        #timeout=0 for non-blocking read
        #since no writetimeout is specified, write is blocking
        self.ser = serial.Serial('/dev/ttyACM0', 57600,timeout=None) #ttyACM1
        self.isConnected = True
        logging.info('Arduino Connected')

    def close(self):
        self.ser.close()
        self.isConnected = False
        logging.info('Arduino Disconnected')

    def connected(self):
        return self.isConnected

    def receive(self):
        sensor = self.ser.readline().rstrip()

        logging.debug('Arduino Received: '+str(sensor))
        return sensor

    def send(self,command):
        for c in command:
            self.ser.write(c)
        logging.debug('Arduino Sent: '+str(command))
