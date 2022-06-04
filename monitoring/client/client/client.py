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

    def init(self):
        pass

    def run(self):
        logger.info("Starting client on {self._host}:{self._port}")

        # Casos para operacao 'instalar sensor'
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 added'
        # Se sensor ja estiver sido adicionado, espere uma resposta diferente
        msg = self.add_sensor(1, 1); assert msg == b'sensor 1 already exists in 1'

    def add_sensor(self, sensor_id, equipment_id):
        return self._send_recv(f"add sensor {sensor_id} in {equipment_id}")

    def remove_sensor(self, sensor_id, equipment_id):
        return self._send_recv(f"remove sensor {sensor_id} in {equipment_id}")

    def list_sensors(self, equipment_id):
        return self._send_recv(f"list sensors in {equipment_id}")

    def read_sensors(self, sensors_list, equipment_id):
        sensors_list_str = ""
        for sensor_id in sensors_list:
            sensors_list_str += f"{sensor_id} "
        if sensors_list_str != "":
            # Remove trailing space
            sensors_list_str = sensors_list_str.rstrip()
        return self._send_recv(f"read {sensors_list_str} in {equipment_id}")

    def kill_server(self):
        self._send("kill")

    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(True)
        # TODO: Make sure was successfully estabilished
        self._sock.connect((self._host, self._port))

    def _close(self):
        self._sock.close()

    def _send(self, msg):
        self._connect()
        send_str(self._sock, msg)
        self._close()

    def _send_recv(self, msg):
        self._connect()
        send_str(self._sock, msg)
        resp = self._sock.recv(MAX_MSG_SIZE)
        self._close()
        return resp
