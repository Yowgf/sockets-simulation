import socket

from common.log import log
from common.contract.comm import send_str
from common.contract.comm import decode_msg
from common.contract.limits import MAX_MSG_SIZE
from common.contract.utils import sensors_list_to_string
from common.utils.utils import parse_address_type
from common.utils.utils import new_socket

logger = log.logger()

class Client:
    def __init__(self, config):
        self._host = config.host
        self._port = config.port

        self._sock = None

    def init(self):
        pass

    def run(self):
        entry = ""
        stop_keyword = "quit"
        while True:
            entry = input()
            if entry == stop_keyword:
                logger.info("Received stop keyword {stop_keyword}. Halting.")
                break
            if entry == 'kill':
                self._send(entry)
            else:
                resp = self._send_recv(entry)
                print(decode_msg(resp))

    def add_sensors(self, sensor_ids, equipment_id):
        sensors_list_str = sensors_list_to_string(sensor_ids)
        return self._send_recv(f"add sensor {sensors_list_str} in "+
                               f"{equipment_id}")

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
        logger.info(f"Connecting client to {self._host}:{self._port}")
        address_type = parse_address_type(self._host)
        self._sock = new_socket(address_type)
        self._sock.connect((self._host, self._port))

    def _close(self):
        logger.info(f"Closing connection to {self._host}:{self._port}")
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
