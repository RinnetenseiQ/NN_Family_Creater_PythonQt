import socket
from typing import Any

from PyQt5 import QtCore

from Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams
import json
import pandas as pd


class Project_controller:
    def __init__(self, mode: int, project_type: str = None,
                 is_open: bool = False,
                 optimising: str = None,
                 plot_ui=None):
        """
        :param project_type: can be "c2d",
        :param is_open: to load before created project or no
        :param optimising: can be "genetic", "immune", None
        :param plot_ui:
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

        self.optimising = optimising
        self.is_open = is_open
        self.project_type = project_type

        self.mode = mode

        self.is_run = False  # флаг, показывающий находится данный проект в данный момент в расчете
        self.is_shown = False  # флаг, определяющий, отображается ли проект в task_manager_ui
        self.is_in_queue = False  # флаг, показывающий, находится ли проект в очереди на расчет
        # если is_shown = False, то остальные два тоже False

        # params init
        self.computation_params = None
        if is_open:
            # load project params from file
            pass
        else:
            pass



        self.Accuracies = pd.DataFrame()
        self.Params = pd.DataFrame()
        self.Assessments = pd.DataFrame()

        self.current_chr = {}

        self.optimising_search_output: str = ""
        self.network_output: str = ""
        self.erroneus_output: str = ""

        ####### Slots-Signals #######
        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.ui_handler = UIHandler()
        # перенесём объект в другой поток
        self.ui_handler.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.ui_handler.signal.connect(self.data_received)
        self.ui_handler.plot_signal.connect(self.data_received)
        self.ui_handler.draw_signal.connect(plot_ui.refresh_figure)
        # self.ui_handler.signal.
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.ui_handler.run)
        # запустим поток
        self.thread.start()
        #############################

    #@QtCore.pyqtSlot(object)
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

    def pause_Btn_Click(self):
        pass

    def get_project_params(self):
        params = None
        if self.mode == 1221000:
            params = C2D_ChromosomeParams()
        return params

    def to_json(self):
        pass

    def from_json(self):
        pass


class UIHandler(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)
    plot_signal = QtCore.pyqtSignal(object)
    draw_signal = QtCore.pyqtSignal(object)

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
