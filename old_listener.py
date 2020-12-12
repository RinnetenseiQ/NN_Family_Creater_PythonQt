import json
import socket

from PyQt5 import QtCore


class UIHandler(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)
    plot_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('localhost', 12246))
        self.sock.listen(1)
        super().__init__()

    def run(self):
        conn, addr = self.sock.accept()
        while True:
            data = conn.recv(20480).decode('UTF-8')
            if not data:
                continue
            datalist = data.split('&')
            if datalist[-1] == "": datalist.pop()
            for data in datalist:
                # data = eval(data)
                data = json.loads(data)
                if data.get("action") == "reconnect":
                    conn, addr = self.sock.accept()
                    pass
                elif data.get("target") == "plot_ui":
                    self.plot_signal.emit(data)
                else:
                    self.signal.emit(data)
            QtCore.QThread.msleep(1000)