import random

class Sensor:
    min_sensor_val = 0
    max_sensor_val = 10

    def __init__(self, id, val):
        if not Sensor.is_valid_value(val):
            raise ValueError(f"Invalid sensor value {val}")

        self.id = id
        self.val = val

    def new_randval(id):
        val = random.random() * Sensor.max_sensor_val
        return Sensor(id, val)

    def is_valid_value(val):
        return Sensor.min_sensor_val <= val and val <= Sensor.max_sensor_val
