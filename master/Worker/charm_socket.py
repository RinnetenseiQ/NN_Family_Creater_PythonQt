import socket
import os
from threading import Thread
import json


# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput


def handle_server(action, data, name):
    if name == "client":
        print("data from client: {} | {}".format(action, data))
    if name == "client2":
        print("data from client2: {} | {}".format(action, data))
    if name == "client3":
        print("data from client3: {} | {}".format(action, data))


def handle_client(action, data, name):
    print("action: {}, data: {}".format(action, data))


def handle_client2(action, data, name):
    print("Hello from server to client2")

    # if action == '':
    #     print("data from {}: {}".format(name, data))


class Charm_Socket:

    def __init__(self, listener, args: tuple, address: str, port: int, name: str, is_server=False, buff_size=1024):
        self.buff_size = buff_size
        self.args = args
        self.listener = listener
        self.port = port
        self.address = address
        self.is_server = is_server
        self.connections = {}
        self.name = [name]
        self.sock = socket.socket(socket.AF_INET)
        if is_server:
            self.names = []
            self.sock.bind((self.address, self.port))
            self.sock.listen()
            thread = Thread(target=self.accepted)
            thread.start()
        else:
            self.sock.connect((self.address, self.port))
            self.connections[self.sock] = ""
            self.send("connect", self.name[-1])
            thread = Listener(self.name, self.sock, self.connections, self.buff_size, self)
            thread.listen = self.listener
            thread.start()

    def accepted(self):
        while True:
            conn, addr = self.sock.accept()
            self.connections[conn] = ""
            thread = Listener(self.name, conn, self.connections, self.buff_size, self)
            thread.listen = self.listener
            thread.start()

    def send(self, action, data, name=None):
        data = {"action": action, "data": data}
        data = json.dumps(data)
        data += os.linesep

        if self.is_server:
            conn = None
            for key, value in self.connections.items():
                if name == value:
                    conn = key
            conn.send(bytes(data, encoding="utf-8"))

            # for conn in self.connections:
            #     conn.send(bytes(data, encoding="utf-8"))
        else:
            list(self.connections.keys())[-1].send(bytes(data, encoding="utf-8"))

    # def send2(self, message: str):
    #     message += os.linesep
    #     if self.is_server:
    #         for conn in self.connections:
    #             conn.send(message.encode('utf-8'))
    #     else:
    #         self.connections[-1].send(message.encode('utf-8'))
    #     pass


class Listener(Thread):

    def __init__(self, name: list, sock: socket.socket, connections: dict, buff_size: int, charm_socket):
        super().__init__()
        self.charm_socket = charm_socket
        self.connections = connections
        self.name = name
        self.client_name = ''
        self.buff_size = buff_size
        self.buffer = []
        self.sock = sock

    def run(self) -> None:
        while True:
            raw_buff = self.sock.recv(self.buff_size).decode('utf-8')
            raw_buff = raw_buff.split(os.linesep)
            for string in raw_buff:
                if string != "":
                    self.buffer.append(string)
            # self.name = "pnx"
            if len(self.buffer) > 0:
                for string in self.buffer:
                    dictionary = json.loads(string)
                    if dictionary["action"] == "connect":
                        self.client_name = dictionary["data"]
                        self.connections[self.sock] = self.client_name
                    else:
                        #self.listen(dictionary["action"], dictionary["data"], self.client_name, self.charm_socket)
                        self.listen(dictionary["action"], dictionary["data"], self.client_name)

            self.buffer.clear()

    def listen(self, action, data, name):
    #def listen(self, action, data, name, charm_socket):
        print("name")
        pass


def test():
    charm_socket_server = Charm_Socket(listener=handle_server, args=(), address="localhost",
                                       port=6121, name='server', is_server=True)
    charm_socket_client = Charm_Socket(listener=handle_client, args=(), address="localhost",
                                       name='client', port=6121)
    charm_socket_client.send("", "test")
    charm_socket_client2 = Charm_Socket(listener=handle_client2, args=(), address="localhost",
                                        name='client2', port=6121)
    charm_socket_client2.send("", "test2")
    charm_socket_client3 = Charm_Socket(listener=handle_client, args=(), address="localhost",
                                        name='client3', port=6121)
    charm_socket_client3.send("", "test3")
    charm_socket_server.send("", "server test", "client2")


if __name__ == "__main__":
    # with PyCallGraph(GraphvizOutput(output_file="../charm_sock.png")):
    #     test()
    # pass
    test()
