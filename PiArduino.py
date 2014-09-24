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
            self.ser = serial.Serial('/dev/ttyACM0', 9600) #ttyACM1
            self.isConnected = True
            logging.info('Arduino Connected')
        finally:
            self.mutex.release()

    def close(self):
        self.mutex.acquire()
        try:
            sel.ser.close()
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
            self.ser.write(command)
            logging.debug('Arduino Sent: '+str(command))
        finally:
            self.mutex.release()