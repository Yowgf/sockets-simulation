class InvalidMessageError(Exception):
    def __init__(self, msg):
        super().__init__(f"Invalid message '{msg}'")

class InvalidSensorError(Exception):
    def __init__(self, sensor_id):
        super().__init__(f"Invalid sensor '{sensor_id}'")

class InvalidEquipmentError(Exception):
    def __init__(self, equipment_id):
        super().__init__(f"Invalid equipment '{equipment_id}'")
