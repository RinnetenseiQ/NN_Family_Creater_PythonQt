import socket
import json
from Exp.charm_socket import Charm_Socket


def handle_server(action, data, name, charm_socket):
    if action == "resend":
        data = json.loads(data)
        #charm_socket.send(data["action"], data["data"], data["name"])
        charm_socket.send(**data)


class Communication_Server:
    def __init__(self):
        charm_socket = Charm_Socket(listener=handle_server, args=(), address="localhost",
                                       port=6121, name='server', is_server=True)


