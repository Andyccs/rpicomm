class MessageModel():
	ARDUINO = "arduino"
	ANDROID = "android"
	PC = "PC"

	def __init__(self,to,message):

		if(to!=self.ARDUINO and to!=self.ANDROID and to!=self.PC):
			assert False

		self.to = to
		self.message = message

	def __str__(self):
		return "to: "+self.to+", message: "+self.message