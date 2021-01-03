import socket
import time
from threading import Thread
from typing import Any
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from master.Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams

import json
import pandas as pd


class Project_controller:
    C2D_IMG_CLF_GEN = 1221000

    def __init__(self, mode: int, is_open: bool = False,
                 project_name: str = "project",
                 project_path: str = "C:/keras/Projects"):
        """
        :param is_open: to load before created project or no
        :param mode: code of project type
        1st digit - is code of task
            1 - classification, 2 - clasterisation, 3 - regression
        2nd digit - is a code for project input data type
            0 - audio, 1 - text, 2 - image, 3 - video, 4 - table, 5 - timesteps
        3rd digit - is a code for type of project
            0 - custom, 1 - applied, 2 - optimising
        4th digit - type of optimising algorithm
            0 - without, 1 - genetic, 2 - immune
        5-6th digit - type of aplied models project
            00 - without, 01 - ResNet50V2 .........
        7th digit - is additional
            -if not optimising && image, 0 - simple convolutional, 1 - perceptron, .......

        For example 1221000 is a code of project which use c2d_gui window:
        task:                   (1)classification
        input type:             (2)image
        project type:           (2)optimising
        optimising algorithm:   (1)genetic
        applied:                (0)
                                (0)without
        additional:             (0)simple convolutional


        """

        self.is_open = is_open
        self.mode = mode
        self.communicator = Communicator()
        self.is_run = False  # флаг, показывающий находится данный проект в данный момент в расчете
        self.is_shown = False  # флаг, определяющий, отображается ли проект в task_manager_ui
        self.is_in_queue = False  # флаг, показывающий, находится ли проект в очереди на расчет
        # если is_shown = False, то остальные два тоже False

        self.socket_port = 0
        self.progress_percent = 0
        self.params = self.get_project_params()

        self.Accuracies = pd.DataFrame()
        self.params_count = pd.DataFrame()
        self.Assessments = pd.DataFrame()

        self.chromosome_configs = []

        self.current_chr = {}

        self.optimising_search_output: str = ""
        self.network_output: str = ""
        self.erroneus_output: str = ""

        self.settings = QSettings()
        self.dataset_path = self.settings.value("datasetPath", "C:/", type=str)
        self.project_path = project_path
        self.project_name = project_name

        ####### Slots-Signals #######
        # # создадим поток
        # self.thread = QtCore.QThread()
        # # создадим объект для выполнения кода в другом потоке
        # self.ui_handler = UIHandler()
        # # перенесём объект в другой поток
        # self.ui_handler.moveToThread(self.thread)
        # # после чего подключим все сигналы и слоты
        # self.ui_handler.signal.connect(self.data_received)
        # self.ui_handler.plot_signal.connect(self.data_received)
        # self.ui_handler.draw_signal.connect(plot_ui.refresh_figure)
        # # self.ui_handler.signal.
        # # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        # self.thread.started.connect(self.ui_handler.run)
        # # запустим поток
        # self.thread.start()
        #############################

    # @QtCore.pyqtSlot(object)
    def data_received(self, data: dict):
        if data.get("action") == "chr_plotting":
            self.current_chr = json.loads(data.get("data"))
        if data.get("target") == "geneticOutput_TE":
            if data.get("action") == "appendText":
                self.optimising_search_output += data.get("data")
                # self.optimizin_output_TE.append(data.get("data"))
            # elif data.get("action") == "clear":
            #     self.optimizin_output_TE.clear()
        elif data.get("target") == "chrOutput_TE":
            if data.get("action") == "appendText":
                self.network_output += data.get("data")
        pass

    @QtCore.pyqtSlot(object)
    def refresh_output(self, data: dict):
        if data.get("target") == "geneticOutput_TE":
            if data.get("action") == "appendText":
                self.optimising_search_output += data
                # self.optimizin_output_TE.append(data.get("data"))
            # elif data.get("action") == "clear":
            #     self.optimizin_output_TE.clear()
        elif data.get("target") == "chrOutput_TE":
            if data.get("action") == "appendText":
                self.network_output += data
                # self.chr_output_TE.append(data.get("data"))
            # elif data.get("action") == "clear":
            #     self.chr_output_TE.clear()

    def get_socket(self):
        self.net_sock = socket.socket()
        self.net_sock.bind(('localhost', 0))
        self.net_sock.listen(3)
        self.gen_sock = socket.socket()
        self.gen_sock.bind(('localhost', 0))
        self.gen_sock.listen(3)
        with open("../report.txt", "a") as f:
            f.write("bind:\n")
            f.write("net_sock = " + str(self.net_sock.getsockname()[1]) + "\n")
            f.write("gen_sock = " + str(self.gen_sock.getsockname()[1]) + "\n")
            f.write("========================\n")

        return self.net_sock, self.net_sock.getsockname()[1], self.gen_sock, self.gen_sock.getsockname()[1]

    # @QtCore.pyqtSlot(object)

    def listen(self, sock1, sock2):
        self.thread1 = QtCore.QThread()
        self.thread2 = QtCore.QThread()
        self.ui_handler1 = UIHandler(sock1)
        self.ui_handler2 = UIHandler(sock2)
        self.ui_handler1.moveToThread(self.thread1)
        self.ui_handler2.moveToThread(self.thread2)
        self.ui_handler1.signal.connect(self.data_received)
        self.ui_handler2.signal.connect(self.data_received)
        self.ui_handler1.plot_signal.connect(self.data_received)
        self.ui_handler2.plot_signal.connect(self.data_received)
        self.thread1.started.connect(self.ui_handler1.run)
        self.thread2.started.connect(self.ui_handler2.run)
        self.thread1.start()
        self.thread2.start()
        pass

    def listen2(self, sock):

        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.ui_handler = UIHandler(sock)
        # перенесём объект в другой поток
        self.ui_handler.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.ui_handler.signal.connect(self.data_received)
        self.ui_handler.plot_signal.connect(self.data_received)
        # self.ui_handler.draw_signal.connect(plot_ui.refresh_figure)
        # self.ui_handler.signal.
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.ui_handler.run)
        # запустим поток
        self.thread.start()
        # if action == "listen!":
        #     # создадим поток
        #     self.thread = QtCore.QThread()
        #     # создадим объект для выполнения кода в другом потоке
        #     self.ui_handler = UIHandler()
        #     # перенесём объект в другой поток
        #     self.ui_handler.moveToThread(self.thread)
        #     # после чего подключим все сигналы и слоты
        #     self.ui_handler.signal.connect(self.data_received)
        #     self.ui_handler.plot_signal.connect(self.data_received)
        #     # self.ui_handler.draw_signal.connect(plot_ui.refresh_figure)
        #     # self.ui_handler.signal.
        #     # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        #     self.thread.started.connect(self.ui_handler.run)
        #     # запустим поток
        #     self.thread.start()
        # elif action == "switch_off":
        #     # перестать слушать
        #     pass

    def listen3(self, sock1, sock2):
        self.listener1 = Listener(sock1, self)
        self.listener2 = Listener(sock2, self)
        # self.listener1.signal.connect(self.data_received)
        # self.listener2.signal.connect(self.data_received)
        # self.listener1.run()
        # self.listener2.run()
        self.listener1.start()
        self.listener2.start()

        pass

    def pause_Btn_Click(self):
        pass

    def get_project_params(self):
        if self.is_open:
            pass
        else:
            params = None
            if self.mode == Project_controller.C2D_IMG_CLF_GEN:  # 1221000
                params = C2D_ChromosomeParams()
                # self.callbacks_handler
            return params

    def update_name(self, name):
        self.name = name

    def update_progress(self, progress):
        self.progress_percent = progress

    def to_json(self):
        pass

    def from_json(self):
        pass


class Communicator(QtCore.QObject):
    pinok = QtCore.pyqtSignal(object)
    ui_pinok = QtCore.pyqtSignal(object)


class ListenerParser(Thread):
    def __init__(self, conn, project_controller):
        self.project_controller = project_controller
        self.conn = conn
        super().__init__()

    def run(self) -> None:
        self.buff = []
        while True:
            data = self.conn.recv(20480).decode('UTF-8')
            #if self.break_point: breakpoint()
            if not data:
                time.sleep(0.5)
                continue
            self.buff.clear()
            #if self.break_point: breakpoint()
            data = data.split("&")
            if data[-1] == "": data.pop(-1)
            if len(data) != 0: self.buff += data
            if len(self.buff) == 0:
                time.sleep(0.5)
                continue

            for data in self.buff:
                # data = eval(data)
                try:
                    data = json.loads(data)
                except json.decoder.JSONDecodeError:
                    data
                except TypeError:
                    data
                self.update_pc(data)
                # if data.get("target") == "accept":
                #   conn, addr = self.sock.accept()
                    # self.sock.listen()
            # conn, addr = self.sock.accept()

    def update_pc(self, data):

        copy_str = str(self.project_controller.optimising_search_output)
        str_list = copy_str.split("\n")
        if len(str_list) >= 82:
            self.break_point = True
        if data.get("target") == "accuracy":
            self.project_controller.Accuracies = self.project_controller.Accuracies.append(data.get("data"), ignore_index=True, sort=False)
            self.project_controller.communicator.ui_pinok.emit(self.project_controller)
        if data.get("target") == "assesment":
            self.project_controller.Assessments = self.project_controller.Assessments.append(data.get("data"), ignore_index=True, sort=False)
            self.project_controller.communicator.ui_pinok.emit(self.project_controller)
        if data.get("target") == "params":
            self.project_controller.params_count = self.project_controller.params_count.append(data.get("data"), ignore_index=True, sort=False)
            self.project_controller.communicator.ui_pinok.emit(self.project_controller)
        if data.get("target") == "chr_config":  # 2
            self.project_controller.chromosome_configs.append(data.get("data"))
            self.project_controller.optimising_search_output += data.get("data")
            if len(self.project_controller.optimising_search_output) == len(copy_str):
                breakpoint()
            if self.project_controller.optimising_search_output is copy_str:
                breakpoint()
        if data.get("target") == "interim_est":  # 3
            s = "Params: {}   Accuracy: {}".format(data.get("data")[0], data.get("data")[1])
            self.project_controller.optimising_search_output += "\n" + s + "\n\n"
            if len(self.project_controller.optimising_search_output) == len(copy_str):
                breakpoint()
        if data.get("target") == "gen_epoch":  # 1
            s = "################# Epoch {} ###################".format(str(data.get("data")))
            self.project_controller.optimising_search_output += s + "\n\n"
            if len(self.project_controller.optimising_search_output) == len(copy_str):
                breakpoint()
        if data.get("target") == "assesment_str":  # 4
            self.project_controller.optimising_search_output += data.get("data") + "\n"
            if len(self.project_controller.optimising_search_output) == len(copy_str):
                breakpoint()
        if data.get("target") == "net_output":
            self.project_controller.network_output += data.get("data") + "\n"
        #     pass



        #     pass

        self.project_controller.communicator.pinok.emit(self.project_controller)


class Listener(Thread):
    # signal = QtCore.pyqtSignal(object)

    def __init__(self, sock, project_controller):
        self.project_controller = project_controller
        self.sock = sock
        self.break_point = False
        super().__init__()

    def run(self):
        print("run connection listening...")
        #self.sock
        while True:
            conn, addr = self.sock.accept()
            ListenerParser(conn, self.project_controller).start()








class UIHandler(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)
    plot_signal = QtCore.pyqtSignal(object)
    draw_signal = QtCore.pyqtSignal(object)

    def __init__(self, sock):
        self.sock = sock
        super().__init__()

    def run(self):
        print("run")
        conn, addr = self.sock.accept()
        self.buff = []
        while True:
            data = conn.recv(20480).decode('UTF-8')
            if data != "": self.buff.append(data)
            if len(self.buff) == 0:
                continue
            # conn, addr = self.sock.accept()
            # if not (not data or data == ''):
            #     # if not data:
            #     continue
            # datalist = data.split('&')
            # if datalist[-1] == "": datalist.pop()
            for data in self.buff:
                # data = eval(data)
                data = json.loads(data)
                # if data.get("action") == "reconnect":
                #     conn, addr = self.sock.accept()
                #     pass
                # if data.get("target") == "acc":
                self.plot_signal.emit(data)
                # else:
                self.signal.emit(data)
                conn, addr = self.sock.accept()
            # conn, addr = self.sock.accept()
            QtCore.QThread.msleep(100)

    # def run(self):
    #     conn, addr = self.sock.accept()
    #     while True:
    #         data = conn.recv(20480).decode('UTF-8')
    #         if not data:
    #             continue
    #         datalist = data.split('&')
    #         if datalist[-1] == "": datalist.pop()
    #         for data in datalist:
    #             # data = eval(data)
    #             data = json.loads(data)
    #             if data.get("action") == "reconnect":
    #                 conn, addr = self.sock.accept()
    #                 pass
    #             elif data.get("target") == "plot_ui":
    #                 self.plot_signal.emit(data)
    #             else:
    #                 self.signal.emit(data)
    #         QtCore.QThread.msleep(1000)
