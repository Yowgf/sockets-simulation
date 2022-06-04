from .errors import InvalidSensorError
from .errors import InvalidEquipmentError
from .limits import SENSOR_IDS
from .limits import EQUIPMENT_IDS

def validate_sensor_id(sensor_id):
    if sensor_id not in SENSOR_IDS:
        raise InvalidSensorError(sensor_id)

def validate_sensor_ids(sensor_ids):
    for sensor_id in sensor_ids:
        validate_sensor_id(sensor_id)

def validate_equipment_id(equipment_id):
    if equipment_id not in EQUIPMENT_IDS:
        raise InvalidEquipmentError(equipment_id)
