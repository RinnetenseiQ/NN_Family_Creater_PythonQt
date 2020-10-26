import json
import socket
import sys
import time
from collections import deque
from threading import Thread

import qdarkstyle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication, QSettings

from Algorithms.GeneticProgram import GeneticProgramProcess
from Forms.Parents.start_page_gui_parent import Ui_StartPageWindow
from Forms.c2d_gui import MainWindow
from Forms.plot_ui import PlotWindow
from Forms.task_manager_gui import TasksWindow


class StartPageWindow(QtWidgets.QMainWindow, Ui_StartPageWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()

        self.setupUi(self)
        # self.loadSettings()
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
        self.comboBox.addItem("Convolutional 2D NN")

        self.comboBox_2.addItem("Genetic optimize")
        self.comboBox_2.addItem("Immune optimize")
        self.comboBox_2.addItem("Custom")

        self.pushButton.clicked.connect(self.open_Btn_Click)
        self.pushButton_2.clicked.connect(self.create_Btn_Click)
        self.pushButton_3.clicked.connect(self.task_Btn_Click)

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
    def __init__(self, chr_q: deque):
        super().__init__()
        self.chromosome_params_queue = chr_q

    def run(self):
        # while len(self.chromosome_params_queue) > 0:
        while True:
            if len(self.chromosome_params_queue) != 0:
                chromosome_params = self.chromosome_params_queue.popleft()
                prog = GeneticProgramProcess(chromosome_params)
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
