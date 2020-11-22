import json
import socket
import sys
import time
from collections import deque
from threading import Thread

import qdarkstyle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QFileDialog

from Algorithms.GeneticProgram import GeneticProgramProcess
from Forms.Parents.start_page_gui_parent import Ui_StartPageWindow
from Forms.c2d_gui import MainWindow
from Forms.plot_ui import PlotWindow
from Forms.predict_c2d_gui import PredictC2DWindow
from Forms.task_manager_gui import TasksWindow


class StartPageWindow(QtWidgets.QMainWindow, Ui_StartPageWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()

        self.setupUi(self)
        self.settings = QSettings()
        self.loadSettings()
        self.initWidgets()

        self.paramsQueue = deque([])
        self.plots_window = PlotWindow()
        self.tasks_window = TasksWindow(self.plots_window, self.paramsQueue)

        queue_program_thread = QueueProgramThread(self.paramsQueue)
        queue_program_thread.start()

        ############### Commutators ################
        ####### Slots-Signals #######
        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.ui_handler = UIHandler()
        # перенесём объект в другой поток
        self.ui_handler.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.ui_handler.signal.connect(self.tasks_window.refresh_output)
        self.ui_handler.plot_signal.connect(self.plots_window.refreshFigure)
        # self.ui_handler.signal.
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.ui_handler.run)
        # запустим поток
        self.thread.start()
        #############################

        self.show()

    def initWidgets(self):
        tab_list = ["Optimizing",
                    "Application",
                    "Custom",
                    "Predict"]
        for i in range(len(tab_list)):
            self.tabWidget.setTabText(i, tab_list[i])
        self.tabWidget.setCurrentIndex(0)

        self.comboBox.addItems(["Convolutional 2D NN"])
        self.comboBox_2.addItems(["Genetic optimize", "Immune optimize", "Custom"])
        self.app_model_CB.addItems(["ResNet50V2", "VGG19"])
        self.predict_problem_CB.addItems(["classification", "regression", "clasterization"])
        self.predict_datatype_CB.addItems(["2D (image)", "3D (video)", "1D (timesteps)", "text", "DataFrame"])

        self.pushButton.clicked.connect(self.open_Btn_Click)
        self.pushButton_2.clicked.connect(self.create_Btn_Click)
        self.pushButton_3.clicked.connect(self.task_Btn_Click)
        self.dataset_path_TB.clicked.connect(self.app_dataset_path_Btn_clicked)
        self.saveTo_TB.clicked.connect(self.app_saveTo_Bnt_Clicked)
        self.app_create_Btn.clicked.connect(self.app_create_Btn_Clicked)
        self.predict_letsgo_Btn.clicked.connect(self.predict_lets_go_Btn_Clicked)

    def loadSettings(self):
        self.app_dataset_path_LE.setText(self.settings.value("app_datasetPath", "C:/", type=str))
        self.saveTo_path_LE.setText(self.settings.value("custom_model_path", "C:/", type=str))

    def create_Btn_Click(self):
        if self.comboBox.currentIndex() == 0:
            if self.comboBox.currentIndex() == 0:
                self.c2d_window = MainWindow(self.paramsQueue, self.tasks_window)
                self.c2d_window.show()
                # self.hide()

        pass

    def open_Btn_Click(self):
        pass

    def task_Btn_Click(self):
        self.tasks_window.show()
        pass

    def app_dataset_path_Btn_clicked(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Dataset folder",
                                                   self.settings.value("app_datasetPath", "C:/", type=str))
        if dirlist == "":
            self.app_dataset_path_LE.setText(self.settings.value("app_datasetPath", "C:/", type=str))
        else:
            self.app_dataset_path_LE.setText(dirlist)
            self.settings.setValue("app_datasetPath", dirlist)
            self.settings.sync()

    def app_saveTo_Bnt_Clicked(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get folder to save model",
                                                   self.settings.value("custom_model_path", "C:/", type=str))
        if dirlist == "":
            self.saveTo_path_LE.setText(self.settings.value("custom_model_path", "C:/", type=str))
        else:
            self.saveTo_path_LE.setText(dirlist)
            self.settings.setValue("custom_model_path", dirlist)
            self.settings.sync()

    def app_create_Btn_Clicked(self):
        if self.app_model_CB.currentText() == 0:
            params = {"model": "ResNet50V2",
                      "datapath": self.app_dataset_path_LE.text(),
                      "save_to": self.saveTo_path_LE.text(),
                      "project_name": self.app_project_name_LE.text()}
            self.paramsQueue.append(params)

            pass

    def predict_lets_go_Btn_Clicked(self):
        self.predict_window = None
        # predict_mode = (self.predict_problem_CB.currentText() == 0) and (self.predict_datatype_CB.currentText() == 0)
        if (self.predict_problem_CB.currentIndex() == 0) and (self.predict_datatype_CB.currentIndex() == 0):
            self.predict_window = PredictC2DWindow()
        self.predict_window.show()

        pass


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


class QueueProgramThread(Thread):
    def __init__(self, params_queue: deque):
        super().__init__()
        self.params_queue = params_queue

    def run(self):
        # while len(self.chromosome_params_queue) > 0:
        #
        while True:
            if len(self.params_queue) != 0:
                prog = None
                params = self.params_queue.popleft()
                if params.__class__.__name__ == "C2D_ChromosomeParams":
                    prog = GeneticProgramProcess(params)
                elif type(params) == dict:
                    pass
                elif params == "custom":  # переделать под custom
                    pass

                prog.run()
                # процесс стопит поток или нет? Yes
            else:
                time.sleep(1)


if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    QCoreApplication.setOrganizationName("QSoft")
    # QCoreApplication.setOrganizationDomain("Settings")
    QCoreApplication.setApplicationName("NN Family Creater")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    # app.setSt
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    startWindow = StartPageWindow()
    # Запуск
    sys.exit(app.exec_())
