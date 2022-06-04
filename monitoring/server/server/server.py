import socket

from ...common.log import log
from ...common.contract.limits import MAX_MSG_SIZE
from .request import AddRequest, RemoveRequest, ListRequest, ReadRequest

logger = log.logger()

class Server:
    def __init__(self, config):
        self._ipver = config.ipver
        self._port = config.port

        # Map <equipment id> -> <list of sensors>
        self._sensors = {}
        self._max_num_sensors = 15

        self._sock = None

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def run(self, should_stop=lambda:False):
        s.bind(("", self._port))
        s.listen(1)

        while not should_stop():
            client_socket, client_addr = s.accept()

            logger.info(f"Received connection from address {client_addr}")

            req = self._receive()
            resp = self._process_request(request)
            self._respond(resp)

        s.close()

    def _receive(self):
        msg_bytes = self._sock.recv(MAX_MSG_SIZE)
        msg = msg.decode('ascii')
        if msg.startswith('add'):
            return AddRequest.parse(msg)
        elif msg.startswith('remove'):
            return RemoveRequest.parse(msg)
        elif msg.startswith('list'):
            return ListRequest.parse(msg)
        elif msg.startswith('read'):
            return ReadRequest.parse(msg)
        else:
            raise ValueError(f"Invalid message {msg}")

    def _respond(self, resp):
        self._sock.send(resp.encode('ascii'))

    def _process_request(self, req):
        if isinstance(req, AddRequest):
            return self._add_sensor(req)
        elif isinstance(req, RemoveRequest):
            return self._remove_sensor(req)
        elif isinstance(req, ListRequest):
            return self._list_sensors(req)
        elif isinstance(req, ReadRequest):
            return self._read_sensor(req)

    def _add_sensor(self, req):
        sensor_id = req.sensor_id
        equipment_id = req.equipment_id
        if self._get_num_sensors() >= self._max_num_sensors:
            return f"limit exceeded"
        elif equipment_id not in self._sensors:
            self._sensors[equipment_id] = [sensor_id]
            return f"sensor {sensor_id} added"
        elif sensor_id in self._sensors[equipment_id]:
            return f"sensor {sensor_id} already exists in {equipment_id}"
        else:
            self._sensors[equipment_id].append(sensor_id)
            return f"sensor {sensor_id} added"

    def _remove_sensor(self, req):
        pass

    def _list_sensors(self, req):
        pass

    def _read_sensor(self, req):
        pass

    def _get_num_sensors(self):
        num_sensors = 0
        for equipment_id in self._sensors:
            num_sensors += len(self._sensors[equipment_id])
        return num_sensors
