import socket

class Client:
    def __init__(self, config):
        self._host = config.host
        self._port = config.port

    def init(self):
        pass

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((self._host, self._port))

        s.close()
