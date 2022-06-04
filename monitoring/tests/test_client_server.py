import threading
import time

from ..common.contract.comm import decode_msg
from ..common.contract.limits import MAX_NUM_SENSORS
from ..common.contract.limits import EQUIPMENT_IDS
from ..common.contract.limits import SENSOR_IDS
from ..common.contract.utils import sensors_list_to_string

class TestClientServer:
    def stop_server(self, client):
        client.kill_server()

    def check_resp(self, resp, expected):
        decoded_resp = decode_msg(resp)
        assert decoded_resp == expected, (f"Expected '{expected}' "+
                                          f"got '{decoded_resp}'")

    def wait_server_wakeup(self):
        time.sleep(0.01)

    def test_add_sensors_one(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor 01 added")

        self.stop_server(client)
        server_runner.join()

    def test_add_sensors_already_exists(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        resp = client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor 01 already exists in 01")

        self.stop_server(client)
        server_runner.join()

    def test_add_sensors_multiple(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensors(SENSOR_IDS, EQUIPMENT_IDS[0])
        expect_added_sensors = sensors_list_to_string(SENSOR_IDS)
        self.check_resp(resp, f"sensor {expect_added_sensors} added")

        self.stop_server(client)
        server_runner.join()

    def test_add_sensors_limit(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        num_sensors_added = 0
        for equipment_id in EQUIPMENT_IDS:
            for sensor_id in SENSOR_IDS:
                resp = client.add_sensors([sensor_id], equipment_id)
                self.check_resp(resp, f"sensor {sensor_id} added")
                num_sensors_added += 1
                if num_sensors_added >= MAX_NUM_SENSORS:
                    break
            if num_sensors_added >= MAX_NUM_SENSORS:
                break
        resp = client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        self.check_resp(resp, "limit exceeded")

        self.stop_server(client)
        server_runner.join()

    def test_remove_sensor_does_not_exist(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.remove_sensor(SENSOR_IDS[0], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor {SENSOR_IDS[0]} does not exist in "+
                        f"{EQUIPMENT_IDS[0]}")

        self.stop_server(client)
        server_runner.join()

    def test_remove_sensor_exists(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        resp = client.remove_sensor(SENSOR_IDS[0], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor {SENSOR_IDS[0]} removed")

        self.stop_server(client)
        server_runner.join()

    def test_list_sensors_none(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.list_sensors(EQUIPMENT_IDS[0])
        self.check_resp(resp, "none")

        self.stop_server(client)
        server_runner.join()

    def test_list_sensors_one(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor 01 added")
        resp = client.list_sensors(EQUIPMENT_IDS[0])
        self.check_resp(resp, "01")

        self.stop_server(client)
        server_runner.join()

    def test_list_sensors_some(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensors(SENSOR_IDS, EQUIPMENT_IDS[0])
        expect_added_str = sensors_list_to_string(SENSOR_IDS)
        self.check_resp(resp, f"sensor {expect_added_str} added")
        resp = client.list_sensors(EQUIPMENT_IDS[0])
        self.check_resp(resp, "01 02 03 04")

        self.stop_server(client)
        server_runner.join()

    def test_read_no_sensors(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.read_sensors(SENSOR_IDS[:2], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"sensor(s) {SENSOR_IDS[0]} {SENSOR_IDS[1]} "+
                        f"not installed")

        self.stop_server(client)
        server_runner.join()

    def test_read_one_sensor(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        client.add_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        resp = client.read_sensors(SENSOR_IDS[:1], EQUIPMENT_IDS[0])
        self.check_resp(resp, f"{SENSOR_IDS[0]}")

        self.stop_server(client)
        server_runner.join()

    def test_read_full_equipment(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        client.add_sensors(SENSOR_IDS, EQUIPMENT_IDS[0])
        resp = client.read_sensors(SENSOR_IDS, EQUIPMENT_IDS[0])
        expected_resp = sensors_list_to_string(SENSOR_IDS)
        self.check_resp(resp, expected_resp)

        self.stop_server(client)
        server_runner.join()

    def test_read_some_installed_some_uninstalled(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        client.add_sensors(SENSOR_IDS[:2], EQUIPMENT_IDS[0])
        resp = client.read_sensors(SENSOR_IDS, EQUIPMENT_IDS[0])
        uninstalled_sensors = sensors_list_to_string(SENSOR_IDS[2:])
        self.check_resp(resp, f"sensor(s) {uninstalled_sensors} not installed")

        self.stop_server(client)
        server_runner.join()
