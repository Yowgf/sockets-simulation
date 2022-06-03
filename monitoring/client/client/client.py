import socket

class Client:
    def __init__(self, config):
        self._host = config.host
        self._port = config.port

    def init(self):
        pass

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: Make sure was successfully estabilished
        s.connect((self._host, self._port))

        # Casos para operacao 'instalar sensor'
        s.send(b"add sensor 1 in 1")
        msg = s.recv(1024); assert msg == b'sensor 1 added'
        # Se sensor ja estiver sido adicionado, espere uma resposta diferente
        s.send(b"add sensor 1 in 1")
        msg = s.recv(1024); assert msg == b'sensor 1 already exists in 1'

        s.close()
