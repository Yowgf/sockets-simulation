import pytest

from ..client.client.client import Client
from ..server.server.server import Server
from .mocks import ClientConfig, ServerConfig

PORT = 60008

@pytest.fixture
def client():
    client_config = ClientConfig('127.0.0.1', PORT)
    client = Client(client_config)
    client.init()
    return client

@pytest.fixture
def server():
    server_config = ServerConfig('v4', PORT)
    server = Server(server_config)
    server.init()
    return server

@pytest.fixture
def client_ipv6():
    client_config = ClientConfig('::1', PORT)
    client = Client(client_config)
    client.init()
    return client

@pytest.fixture
def server_ipv6():
    server_config = ServerConfig('v6', PORT)
    server = Server(server_config)
    server.init()
    return server
