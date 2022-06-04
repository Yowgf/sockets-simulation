class AddRequest:
    def __init__(self, sensor_id, equipment_id):
        self.sensor_id = sensor_id
        self.equipment_id = equipment_id

class RemoveRequest:
    def __init__(self, sensor_id, equipment_id):
        self.sensor_id = sensor_id
        self.equipment_id = equipment_id

class ListRequest:
    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

class ReadRequest:
    def __init__(self, sensors_list, equipment_id):
        self.sensors_list = sensors_list
        self.equipment_id = equipment_id
