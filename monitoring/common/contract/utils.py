def sensors_list_to_string(sensors_list):
    sensors_list_str = ""
    for sensor_id in sensors_list:
        sensors_list_str += f"{sensor_id} "
    sensors_list_str = sensors_list_str.rstrip()
    return sensors_list_str
