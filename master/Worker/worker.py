# from multiprocessing import Process
from multiprocessing import Process
from threading import Thread
import json
from socket import socket
from charm_socket import Charm_Socket
from random import SystemRandom
import uuid
from protocol import calculate


class Worker(Process):

    def __init__(self):
        super().__init__()
        self.running = False
        self.uid = str(uuid.uuid4())

    def run(self) -> None:
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        self.communicator = Communicator(adr=self.config["address"], port=self.config["port"], uid=self.uid)
        self.communicator.start()
        # while True:
        #     ...


class Communicator(Thread):

    def __init__(self, adr, port, uid):
        super().__init__()
        self.uid = uid
        self.port = port
        self.adr = adr

    def run(self) -> None:
        self.sock = Charm_Socket(listener=self.handler, args=(), address=self.adr, port=self.port, name=self.uid, buff_size=4096)
        print(6)
        # self.sock = Charm_Socket(listener=handler, args=(), address="localhost", port=9088, name=self.uid)

        # print(self.sock)

    def handler(self, action, data, name):
        print(7)
        if action == "calculate":
            calculate(data)


if __name__ == "__main__":
    worker = Worker()
    worker.start()
