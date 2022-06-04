import socket

from ...common.contract.limits import MAX_MSG_SIZE

class Client:
    def __init__(self, config):
        self._host = config.host
        self._port = config.port

        self._sock = None

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # TODO: Make sure was successfully estabilished
        self._sock.connect((self._host, self._port))

        # Casos para operacao 'instalar sensor'
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 added'
        # Se sensor ja estiver sido adicionado, espere uma resposta diferente
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 already exists in 1'

        self._sock.close()

    def add_sensor(self, sensor_id, equipment_id):
        self._sock.send(bytes(f"add sensor {sensor_id} in {equipment_id}"))
        return self._sock.recv(MAX_MSG_SIZE)
