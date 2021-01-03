from multiprocessing import Process
from threading import Thread
import time
import os
import socket
import random


class MyProcess(Process):
    def __init__(self):
        super(Process, self).__init__()
        self.sender_socket = socket.socket()
        self.sender_socket.connect(('127.0.0.1', 65432))
        self.rnd = random.Random()

    def run(self) -> None:
        while True:
            # print("hello from thread" + self.getName() + os.linesep)
            sending_string = "hello from thread" + self.name + os.linesep
            # print(sending_string)
            # self.sender_socket.connect(('127.0.0.1', 65432))
            self.sender_socket.send(sending_string.encode('utf-8'))
            # self.sender_socket.close()
            time.sleep(1 + self.rnd.randrange(0, 100) / 100)
            # if self.name != '1':
            # time.sleep(1 + self.rnd.randrange(0, 100) / 100)
            # else:
            # time.sleep(0.001)


class SocketListener(Thread):
    def __init__(self, conn: socket.socket, addr: tuple):
        self.conn = conn
        self.addr = addr
        super().__init__()

    def run(self) -> None:
        while True:
            data = self.conn.recv(1025)
            if data != b'':
                print(data.decode('utf-8'))


if __name__ == "__main__":
    # init socket
    listener_socket = socket.socket()
    listener_socket.bind(('127.0.0.1', 65432))
    listener_socket.listen(5)

    my_process_1 = MyProcess()
    my_process_1.name = "1"
    my_process_2 = MyProcess()
    my_process_2.name = "2"
    my_process_1.start()
    my_process_2.start()

    print("here listener starting...")
    # Socket listener
    while True:
        conn, addr = listener_socket.accept()
        SocketListener(conn, addr).start()


