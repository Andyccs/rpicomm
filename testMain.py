from piBlueTooth import piBlueTooth
from protocolHandler import protocolHandler
import threading
import Queue

class BTThread(threading.thread):
	mainThread = None
	#0 = false
	connected = 0
	piBlueTooth = None
	#queue.queue is a Constructor for a FIFO queue
	dataDropped = Queue.queue()
	action = None
	quantity = None
	
	def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
	
	def assignMainThread(self, mainThread):
                self.mainthread = mainThread

    def btConnected(self):
				#return true
                return self.connected == 1

    def send(self, data):
                if self.connected == 1:
                self.piBlueTooth.send(str(data))
	
	def run(self):
                print '[BlueTooth Thread Start]'

                #Code to run bluetooth thread, method that establish connection and accept and sent inputs
                while 1:
                        self.piBlueTooth = piBlueTooth()
                        self.connected = 1

                        try:
                                while 1:
                                        bluetoothRecv = self.piBlueTooth.receive().strip()
                                        print str(bluetoothRecv)
                                        if bluetoothRecv == "EXPLORE": #Exploration
                                                self.mainthread.commandStartExp()
                                        elif bluetoothRecv == "START": #Shortest Path
                                                self.mainthread.commandStartSP()
                                        elif bluetoothRecv == "GET_MAP": #Get Map Info
                                                self.mainthread.commandGM()
                                        else:
                                                self.mainthread.addToQueue('B:'+ bluetoothRecv)
                        except Exception:
                                print "BlueTooth Receive Exception"
                                self.piBlueTooth.close()
                                self.connected = 0
                                continue	
		
class mainThread(threading.Thread):

        negAck = False
		totalBuff = 1
        #comment first because there is only BT else totalBuff = 3
        androidControl = True
        mainQueue = None
        lock = None

        #def __init__(self, threadID, name, wifiThread, btThread, aurThread):
		def __init__(self, threadID, name, btThread):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.mainQueue = Queue.Queue()
                self.protocolHandler = protocolHandler()
                self.btThread = btThread
                self.lock = threading.BoundedSemaphore(self.totalBuff)
        
		def addToQueue(self, command):
                print '[Command To Queue]: ' + command
                self.mainQueue.put(command)

        def clearQueue(self):
                while self.mainQueue.empty() == False:
                        self.mainQueue.get()
				#returns a new bounded semaphore object
				#bounded semaphore checks to make sure its current value doesn’t exceed its initial value
                self.lock = threading.BoundedSemaphore(self.totalBuff)
        
	def pcFlush(self):
                if not self.androidControl:
                        self.clearQueue()

        def commandStartSP(self):
                print 'Shortest Path Start'
                self.androidControl = False
                self.clearQueue()
				
        def commandStartExp(self):
                print 'Exploration Start'
                self.androidControl = False
                self.clearQueue()
				
        def processCommand(self):
                if not self.mainQueue.empty():
                        command = self.mainQueue.get()
						
                        self.protocolHandler.decodeCommand(command)

                        movementAction = self.protocolHandler.getMovementAction()
                        quantity = self.protocolHandler.getCommandInfo()

                        #if commandFrom == 'W' and not self.androidControl:
                         #       self.lock.acquire()
                          #      self.aurThread.send(str(commandToSend))
                           #     print '[Sent Wifi Data To Arduino]: ' + str(commandToSend)

                        #if commandFrom == 'B' and self.androidControl:
                         #       self.lock.acquire()
                          #      self.aurThread.send(str(commandToSend))
                           #     print '[Sent BT Data To Arduino]: ' + str(commandToSend)

								
        def run(self):
                #while true
                while 1:
                        self.processCommand()
                        try:
                                self.processCommand()
                        except Exception:
                                print "Unable to execute main thread"
								
					 #(id, name)
piBtThread = btThread(1, "BlueTooth Thread")
piMainThread = mainThread(0, "Main Thread", piBtThread)
piBtThread.assignMainThread(piMainThread)

piBtThread.start()
piMainThread.start()
