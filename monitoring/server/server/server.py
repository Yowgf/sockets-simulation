import socket

class Server:
    def __init__(self, config):
        self._ipver = config.ipver
        self._port = config.port

    def init(self):
        pass

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", self._port))
        s.listen(backlog=1)

        while True:
            client_socket, client_addr = s.accept()

        s.close()
