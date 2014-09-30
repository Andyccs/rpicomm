from bluetooth import *
import serial

class piBlueTooth:
    uuid = "a1513d56-2b38-421d-bee3-4286f12f9866"
	addr = 4
	
    server_sock = None
    port = None
    client_sock = None
    client_info = None
	
	#boolean flag for connection
	connect_flag = False
	
    def __init__(self):
	
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.setblocking(False)
        self.server_sock.bind(("",addr))
        self.server_sock.listen(10)
		
        self.port = self.server_sock.getsockname()[1]
		
        advertise_service( self.server_sock, "SampleServer",
                           service_id = self.uuid,
                           service_classes = [ self.uuid,
                           SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ]
                        )
       
	def connect(self):
		
		print "Waiting for connection on RFCOMM channel %d" % self.port
        self.client_sock, self.client_info = self.server_sock.accept()
		connect_flag = True
        print "Accepted connection from ", self.client_info
		
	
    def receive(self):
        if self.client_sock == None:
                return
        try:
				#get any available data is what recv(1024) for
                data = self.client_sock.recv(1024)
                if len(data) <> 0:
                        print "Received From Bluetooth [%s]" % data
                        return data
        except IOError:
                print "BlueTooth Receiving Exception"
                pass

    def send(self, data):
        if self.client_sock == None:
                return
        try:
                self.client_sock.send(str(data))
        except IOError:
                print "BlueTooth Sending Exception"
                pass
				
				
    def close(self):
        self.client_sock.close()
        self.server_sock.close()
		connect_flag = False
