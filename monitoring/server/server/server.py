import socket

from ...common.log import log
from ...common.contract.errors import InvalidMessage
from ...common.contract.limits import MAX_NUM_SENSORS
from ...common.contract.comm import send_str, recv_request
from ...common.contract.request import (AddRequest,
                                        RemoveRequest,
                                        ListRequest,
                                        ReadRequest,
                                        KillRequest)

logger = log.logger()

# TODO cases:
#
# - add invalid sensor (only allow 1-4)
# - add invalid equipment (only allow 1-4)
#
# General TODOs:
#
# - Implement the parse function of each type of request
# - Reject request if malformed
################################################################################

class TerminateServer(Exception):
    def __init__(self, reason):
        super().__init__("Terminating server due to reason: " + reason)

class Server:
    def __init__(self, config):
        self._ipver = config.ipver
        self._port = config.port

        # Map <equipment id> -> <list of sensors>
        self._sensors = {}

        self._sock = None

    def init(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(True)

    def run(self):
        self._sock.bind(("", self._port))
        self._sock.listen(1)

        try:
            while True:
                client_socket, client_addr = self._sock.accept()
                logger.info(f"Received connection from address {client_addr}")

                try:
                    req = recv_request(client_socket)
                    resp = self._process_request(req)
                    send_str(client_socket, resp)
                except InvalidMessage as e:
                    log.info(f"Received invalid message from client: {e}")

        except TerminateServer as terminate_exc:
            logger.info(str(terminate_exc))

        self._sock.close()

    def _process_request(self, req):
        if isinstance(req, AddRequest):
            return self._add_sensor(req)
        elif isinstance(req, RemoveRequest):
            return self._remove_sensor(req)
        elif isinstance(req, ListRequest):
            return self._list_sensors(req)
        elif isinstance(req, ReadRequest):
            return self._read_sensors(req)
        elif isinstance(req, KillRequest):
            raise TerminateServer("Received kill request")
        else:
            raise InvalidMessage(f"Invalid request type {type(req)} for request {req}")

    def _add_sensor(self, req):
        sensor_id = req.sensor_id
        equipment_id = req.equipment_id
        if self._get_num_sensors() >= MAX_NUM_SENSORS:
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
        sensor_id = req.sensor_id
        equipment_id = req.equipment_id
        if (equipment_id not in self._sensors or
            sensor_id not in self._sensors[equipment_id]
        ):
            return f"sensor {sensor_id} does not exist in {equipment_id}"
        else:
            self._sensors[equipment_id].remove(sensor_id)
            return f"sensor {sensor_id} removed"

    def _list_sensors(self, req):
        equipment_id = req.equipment_id
        if (equipment_id not in self._sensors or
            len(self._sensors[equipment_id]) == 0
        ):
            return "none"
        else:
            resp = str(self._sensors[equipment_id][0])
            for sensor_id in self._sensors[equipment_id][1:]:
                resp += f" {sensor_id}"
            return resp

    def _read_sensors(self, req):
        sensors_list = req.sensors_list
        equipment_id = req.equipment_id
        success_msg = ""
        failure_msg = ""
        for sensor_id in sorted(sensors_list):
            if (equipment_id not in self._sensors or 
                sensor_id not in self._sensors[equipment_id]
            ):
                failure_msg += f" {sensor_id}"
            else:
                success_msg += f"{sensor_id} "
        if failure_msg != "":
            return "sensor(s)" + failure_msg + " not installed"
        else:
            # Remove trailing space
            return success_msg.rstrip()

    def _get_num_sensors(self):
        num_sensors = 0
        for equipment_id in self._sensors:
            num_sensors += len(self._sensors[equipment_id])
        return num_sensors
