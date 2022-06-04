class InvalidMessage(Exception):
    def __init__(self, msg):
        super().__init__("Invalid message " + str(msg))
