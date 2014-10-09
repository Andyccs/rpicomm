import serial
import logging
import threading


class PiArduino:
    def __init__(self):
        self.ser = None
        self.isConnected = False

        self.mutex = threading.Lock()

    def connect(self):
        self.mutex.acquire()
        try:
            #timeout=0 for non-blocking read
            #since no writetimeout is specified, write is blocking
            self.ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1) #ttyACM1
            self.isConnected = True
            logging.info('Arduino Connected')
        finally:
            self.mutex.release()

    def close(self):
        self.mutex.acquire()
        try:
            # problem here
            self.ser.close()
            self.isConnected = False
            logging.info('Arduino Disconnected')
        finally:
            self.mutex.release()

    def connected(self):
        self.mutex.acquire()
        try:
            return self.isConnected
        finally:
            self.mutex.release()

    def receive(self):
        self.mutex.acquire()
        try:
            sensor = self.ser.readline().rstrip()

            logging.debug('Arduino Received: '+str(sensor))
            return sensor
        finally:
            self.mutex.release()

    def send(self,command):
        self.mutex.acquire()
        try:

            # problem here
            # SerialException('write failed: %s % (v, )')
            # serial.serialutil.SerialExeption: write failed: [Errno 5] Input/output error
            self.ser.write(command)
            logging.debug('Arduino Sent: '+str(command))
        finally:
            self.mutex.release()