from .errors import InvalidMessage

class AddRequest:
    def __init__(self, sensor_id, equipment_id):
        self.sensor_id = sensor_id
        self.equipment_id = equipment_id

    # add sensor {sensor_id} in {equipment_id}
    def parse(req):
        split_by_space = req.split(" ")
        sensor_id = split_by_space[2]
        equipment_id = split_by_space[4]
        return AddRequest(sensor_id, equipment_id)

class RemoveRequest:
    def __init__(self, sensor_id, equipment_id):
        self.sensor_id = sensor_id
        self.equipment_id = equipment_id

    # remove sensor {sensor_id} in {equipment_id}
    def parse(req):
        split_by_space = req.split(" ")
        sensor_id = split_by_space[2]
        equipment_id = split_by_space[4]
        return RemoveRequest(sensor_id, equipment_id)

class ListRequest:
    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    # list sensors in {equipment_id}
    def parse(req):
        split_by_space = req.split(" ")
        equipment_id = split_by_space[3]
        return ListRequest(equipment_id)

class ReadRequest:
    def __init__(self, sensors_list, equipment_id):
        self.sensors_list = sensors_list
        self.equipment_id = equipment_id

    # read {sensor_id1} {sensor_id2} ... in {equipment_id}
    def parse(req):
        split_by_space = req.split(" ")
        sensors_list = split_by_space[1:-2]
        equipment_id = split_by_space[-1]
        return ReadRequest(sensors_list, equipment_id)

class KillRequest:
    def __init__(self):
        pass

    def parse(req):
        return KillRequest()
