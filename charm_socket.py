import socket
from threading import Thread


def func(buff):
    print(buff.decode('utf-8'))


class Charm_Socket:

    def __init__(self, listener, args: tuple, address: str, port: int, is_server=False, buff_size=1024):
        self.buff_size = buff_size
        self.args = args
        self.listener = listener
        self.port = port
        self.address = address
        self.is_server = is_server
        self.connections = []
        self.sock = socket.socket(socket.AF_INET)
        if is_server:
            self.sock.bind((self.address, self.port))
            self.sock.listen()
            thread = Thread(target=self.accepted)
            thread.start()
        else:
            self.sock.connect((self.address, self.port))
            self.connections.append(self.sock)
            thread = Listener(self.sock, self.buff_size)
            thread.listen = self.listener
            thread.start()

    def accepted(self):
        while True:
            conn, addr = self.sock.accept()
            self.connections.append(conn)
            thread = Listener(conn, self.buff_size)
            thread.listen = self.listener
            thread.start()

    def send(self, message: str):
        if self.is_server:
            for conn in self.connections:
                conn.send(message.encode('utf-8'))
        else:
            self.connections[-1].send(message.encode('utf-8'))
        pass


class Listener(Thread):

    def __init__(self, sock: socket.socket, buff_size: int):
        super().__init__()
        self.buff_size = buff_size
        self.buffer = None
        self.sock = sock

    def run(self) -> None:
        while True:
            self.buffer = self.sock.recv(self.buff_size)
            if self.buffer != "":
                self.listen(self.buffer)

    def listen(self, buffer):
        pass


if __name__ == "__main__":
    charm_socket_server = Charm_Socket(listener=func, args=(), address="localhost",
                                       port=6121, is_server=True)
    charm_socket_client = Charm_Socket(listener=func, args=(), address="localhost",
                                       port=6121)
    charm_socket_client.send("test")
    charm_socket_client2 = Charm_Socket(listener=func, args=(), address="localhost",
                                       port=6121)
    charm_socket_client3 = Charm_Socket(listener=func, args=(), address="localhost",
                                       port=6121)
    charm_socket_client2.send("test2")
    charm_socket_server.send("test3")
    pass
