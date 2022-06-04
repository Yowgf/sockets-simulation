import socket

from ...common.log import log
from ...common.contract.comm import send_str
from ...common.contract.limits import MAX_MSG_SIZE

logger = log.logger()

class Client:
    def __init__(self, config):
        self._host = config.host
        self._port = config.port

        self._sock = None

    def __del__(self):
        if self._sock != None:
            self._sock.close()

    def init(self):
        pass

    def run(self):
        logger.info("Starting client on {self._host}:{self._port}")

        # Casos para operacao 'instalar sensor'
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 added'
        # Se sensor ja estiver sido adicionado, espere uma resposta diferente
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 already exists in 1'

    def add_sensor(self, sensor_id, equipment_id):
        self._connect()
        send_str(self._sock, f"add sensor {sensor_id} in {equipment_id}")
        resp = self._sock.recv(MAX_MSG_SIZE)
        self._close()
        return resp

    def kill_server(self):
        self._connect()
        send_str(self._sock, "kill")
        self._close()

    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(True)
        # TODO: Make sure was successfully estabilished
        self._sock.connect((self._host, self._port))

    def _close(self):
        self._sock.close()
