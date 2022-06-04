import socket

IPV4_ADDRESS_TYPE = 'v4'
IPV6_ADDRESS_TYPE = 'v6'

def parse_address_type(hostname):
    if ':' in hostname:
        return IPV6_ADDRESS_TYPE
    else:
        return IPV4_ADDRESS_TYPE

def new_socket(address_type):
    if address_type == IPV4_ADDRESS_TYPE:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif address_type == IPV6_ADDRESS_TYPE:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        raise ValueError(f"Unable to start server with invalid IP version "+
                         f"'{address_type}'")
    sock.setblocking(True)
    return sock
