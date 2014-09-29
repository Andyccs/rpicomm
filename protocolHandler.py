import simplejson

class protocolHandler:

    moveForward = 0
    moveLeft = 1
    moveRight = 2
    moveBack = 3

    movementAction = None
    sensorInfo = None
	quantity = None

    def __init__(self):
        quantity = 0
        movementAction = None
        sensorInfo = [0,0,0,0]

    def decodeCommand(self, command):
        commandList = simplejson.loads(command)
        self.movementAction = commandList['action']
        self.quantity = commandList['quantity']

    def getMovementAction(self):
        return self.commandSource

    def getQuantity(self):
        return int(self.quantity)
