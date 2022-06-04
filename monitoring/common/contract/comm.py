from .limits import MAX_MSG_SIZE
from .request import (AddRequest,
                      RemoveRequest,
                      ListRequest,
                      ReadRequest,
                      KillRequest)
from .errors import InvalidMessageError

def encode_msg(msg_str):
    if len(msg_str) == 0:
        msg_str = "\n"
    elif msg_str[-1] != "\n":
        msg_str += "\n"
    msg = msg_str.encode('ascii')
    return msg

def decode_msg(msg_bytes):
    msg = msg_bytes.decode('ascii')
    if len(msg) == 0 or msg[-1] != "\n":
        raise InvalidMessageError(msg)
    return msg[:-1]

def encode_request(msg_str):
    return encode_msg(msg_str)

def decode_request(msg_bytes):
    msg = decode_msg(msg_bytes)
    if msg.startswith('add '):
        return AddRequest.parse(msg)
    elif msg.startswith('remove '):
        return RemoveRequest.parse(msg)
    elif msg.startswith('list '):
        return ListRequest.parse(msg)
    elif msg.startswith('read '):
        return ReadRequest.parse(msg)
    elif msg.startswith('kill'):
        return KillRequest.parse(msg)
    else:
        raise InvalidMessageError(msg)

def send_str(sock, msg_str):
    encoded_msg = encode_msg(msg_str)
    sock.send(encoded_msg)

def recv_request(sock):
    msg_bytes = sock.recv(MAX_MSG_SIZE)
    decoded_msg = decode_request(msg_bytes)
    return decoded_msg
