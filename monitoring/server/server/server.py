from copy import copy
import socket

from .errors import TerminateServer
from .sensor import Sensor
from ...common.log import log
from ...common.contract.errors import (InvalidMessageError,
                                       InvalidSensorError,
                                       InvalidEquipmentError)
from ...common.contract.limits import MAX_NUM_SENSORS
from ...common.contract.comm import send_str, recv_request
from ...common.contract.request import (AddRequest,
                                        RemoveRequest,
                                        ListRequest,
                                        ReadRequest,
                                        KillRequest)
from ...common.contract.utils import sensors_list_to_string
from ...common.utils.utils import new_socket

logger = log.logger()

# TODO cases:
# 
# - Fix the 'read' API
################################################################################

class Server:
    def __init__(self, config):
        self._ipver = config.ipver
        self._port = config.port

        # Map <equipment id> -> <list of sensors>
        self._sensors = {}

    def init(self):
        self._sock = new_socket(self._ipver)

    def run(self):
        # bind "" == bind INADDR_ANY
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
                except InvalidMessageError as e:
                    logger.info(f"Received invalid message error: {e}")
                except InvalidSensorError as e:
                    logger.info(f"Received invalid sensor error: {e}")
                    send_str(client_socket, "invalid sensor")
                except InvalidEquipmentError as e:
                    logger.info(f"Received invalid equipment error: {e}")
                    send_str(client_socket, "invalid equipment")

        except TerminateServer as terminate_exc:
            logger.info(str(terminate_exc))
        finally:
            self._sock.close()

    def _process_request(self, req):
        if isinstance(req, AddRequest):
            return self._add_sensors(req)
        elif isinstance(req, RemoveRequest):
            return self._remove_sensor(req)
        elif isinstance(req, ListRequest):
            return self._list_sensors(req)
        elif isinstance(req, ReadRequest):
            return self._read_sensors(req)
        elif isinstance(req, KillRequest):
            raise TerminateServer("Received kill request")
        else:
            raise InvalidMessageError(f"Invalid request type {type(req)} for request {req}")

    def _add_sensors(self, req):
        sensor_ids = req.sensor_ids
        equipment_id = req.equipment_id
        cur_num_sensors = self._get_num_sensors()

        added = []
        to_add = copy(sensor_ids)
        while len(to_add) > 0:
            if cur_num_sensors + len(added) >= MAX_NUM_SENSORS:
                return "limit exceeded"

            sensor_id = to_add.pop()
            if self._is_sensor_placed(equipment_id, sensor_id):
                return f"sensor {sensor_id} already exists in {equipment_id}"

            self._insert_sensor(equipment_id, sensor_id)
            added.append(sensor_id)

        added_str = sensors_list_to_string(sensor_ids)
        return f"sensor {added_str} added"

    def _remove_sensor(self, req):
        sensor_id = req.sensor_id
        equipment_id = req.equipment_id
        if not self._is_sensor_placed(equipment_id, sensor_id):
            return f"sensor {sensor_id} does not exist in {equipment_id}"
        else:
            self.__remove_sensor(equipment_id, sensor_id)
            return f"sensor {sensor_id} removed"

    def _list_sensors(self, req):
        equipment_id = req.equipment_id
        if (equipment_id not in self._sensors or
            len(self._sensors[equipment_id]) == 0
        ):
            return "none"
        else:
            sorted_sensor_ids = sorted([sensor.id for sensor in
                                        self._sensors[equipment_id]])
            resp = str(sorted_sensor_ids[0])
            for sensor_id in sorted_sensor_ids[1:]:
                resp += f" {sensor_id}"
            return resp

    def _read_sensors(self, req):
        sensor_ids = req.sensors_list
        equipment_id = req.equipment_id
        success_msg = ""
        failure_msg = ""
        sensors = None
        for sensor_id in sensor_ids:
            if not self._is_sensor_placed(equipment_id, sensor_id):
                failure_msg += f" {sensor_id}"
            else:
                if sensors == None:
                    sensors = self._sensors[equipment_id]
                for sensor in sensors:
                    if sensor.id == sensor_id:
                        break
                success_msg += f"{sensor.val:.2f} "
        if failure_msg != "":
            return "sensor(s)" + failure_msg + " not installed"
        else:
            return success_msg.rstrip()

    def _is_sensor_placed(self, equipment_id, sensor_id):
        if not equipment_id in self._sensors:
            return False
        sensor_ids = [sensor.id for sensor in self._sensors[equipment_id]]
        return sensor_id in sensor_ids

    def _insert_sensor(self, equipment_id, sensor_id):
        if equipment_id not in self._sensors:
            self._sensors[equipment_id] = []
        self._sensors[equipment_id].append(Sensor.new_randval(sensor_id))

    def __remove_sensor(self, equipment_id, sensor_id):
        if equipment_id not in self._sensors:
            raise ValueError(f"Attempt to remove sensor for equipment "+
                             f"{equipment_id} which does not exist")
        sensor_idx = ([sensor.id for sensor in self._sensors[equipment_id]].
                      index(sensor_id))
        self._sensors[equipment_id].pop(sensor_idx)

    def _get_num_sensors(self):
        num_sensors = 0
        for equipment_id in self._sensors:
            num_sensors += len(self._sensors[equipment_id])
        return num_sensors
