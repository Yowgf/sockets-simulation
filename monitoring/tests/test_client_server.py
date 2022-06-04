from multiprocessing import Process
import pytest

from ..client.client.client import Client
from ..server.server.server import Server

from .mocks import ClientConfig, ServerConfig

class TestClientServer:
    PORT = 51555

    @pytest.fixture
    def client(self):
        client_config = ClientConfig('localhost', self.PORT)
        client = Client(client_config)
        client.init()
        return client

    @pytest.fixture
    def server(self):
        server_config = ServerConfig('iv4', self.PORT)
        server = Server(server_config)
        server.init()
        return server

    def stop_server(client):
        client.kill_server()

    def check_resp(self, resp, expected):
        assert resp.decode('ascii') == expected

    def test_add_sensor(self, client, server):
        server_runner = Process(target=server.run)
        server_runner.start()

        resp = client.add_sensor(1, 1)
        self.check_resp(resp, f"sensor {sensor_id} added")

        stop_server()
        server_runner.join()
