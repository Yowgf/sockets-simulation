MAX_MSG_SIZE = 500 # bytes

EQUIPMENT_IDS = ['01', '02', '03', '04']
SENSOR_IDS = ['01', '02', '03', '04']

MAX_NUM_SENSORS = 15

def get_sensorid_from_int(sensorid_int):
    return f"{sensorid_int:02d}"
