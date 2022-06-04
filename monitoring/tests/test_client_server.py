import threading
import time

from ..common.contract.comm import decode_msg
from ..common.contract.limits import MAX_NUM_SENSORS
from ..common.contract.limits import EQUIPMENT_IDS
from ..common.contract.limits import SENSOR_IDS

class TestClientServer:
    def stop_server(self, client):
        client.kill_server()

    def check_resp(self, resp, expected):
        assert decode_msg(resp) == expected, f"Expected '{expected}' got '{resp}'"

    def wait_server_wakeup(self):
        time.sleep(0.1)

    def test_add_sensor_one(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensor(1, 1)
        self.check_resp(resp, f"sensor 1 added")

        self.stop_server(client)
        server_runner.join()

    def test_add_sensor_already_exists(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensor(1, 1)
        resp = client.add_sensor(1, 1)
        self.check_resp(resp, f"sensor 1 already exists in 1")

        self.stop_server(client)
        server_runner.join()

    def test_add_sensor_limit(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        num_sensors_added = 0
        for equipment_id in EQUIPMENT_IDS:
            for sensor_id in SENSOR_IDS:
                resp = client.add_sensor(sensor_id, equipment_id)
                self.check_resp(resp, f"sensor {sensor_id} added")
                num_sensors_added += 1
                if num_sensors_added >= MAX_NUM_SENSORS:
                    break
            if num_sensors_added >= MAX_NUM_SENSORS:
                break
        resp = client.add_sensor(SENSOR_IDS[0], EQUIPMENT_IDS[0])
        self.check_resp(resp, "limit exceeded")

        self.stop_server(client)
        server_runner.join()
