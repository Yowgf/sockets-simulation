import socket

from common.log import log

logger = log.logger()

RECV_LIMIT = 1024

def decode_request(sock):
    msg = sock.recv(RECV_LIMIT)
    logger.info(f"Decoded request: {msg}")
    return msg

def send_response(sock, msg):
    sock.send(msg.encode('ascii'))

class Server:
    def __init__(self, config):
        self._ipver = config.ipver
        self._port = config.port

    def init(self):
        pass

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", self._port))
        s.listen(1)

        while True:
            client_socket, client_addr = s.accept()

            logger.info(f"Received connection from address {client_addr}")

            msg1 = decode_request(client_socket)
            send_response(client_socket, "sensor 1 added")
            msg2 = decode_request(client_socket)
            send_response(client_socket, "sensor 1 already exists in 1")

        s.close()
