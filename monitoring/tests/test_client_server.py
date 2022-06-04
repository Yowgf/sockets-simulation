import threading
import time

from ..common.contract.comm import decode_msg

class TestClientServer:
    def stop_server(self, client):
        client.kill_server()

    def check_resp(self, resp, expected):
        assert decode_msg(resp) == expected

    def wait_server_wakeup(self):
        time.sleep(0.5)

    def test_add_sensor(self, client, server):
        server_runner = threading.Thread(target=server.run)
        server_runner.start()
        self.wait_server_wakeup()

        resp = client.add_sensor(1, 1)
        self.check_resp(resp, f"sensor 1 added")

        self.stop_server(client)
        server_runner.join()
