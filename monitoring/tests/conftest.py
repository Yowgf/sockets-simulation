import pytest

from ..client.client.client import Client
from ..server.server.server import Server
from .mocks import ClientConfig, ServerConfig

PORT = 60006

@pytest.fixture
def client():
    client_config = ClientConfig('localhost', PORT)
    client = Client(client_config)
    client.init()
    return client

@pytest.fixture
def server(client):
    server_config = ServerConfig('iv4', PORT)
    server = Server(server_config)
    server.init()
    return server
