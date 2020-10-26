# from PySide2 import QtWidgets
import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QSettings

import qdarkstyle
import sys
import json

from PyQt5.QtWidgets import QFileDialog, qApp
from PyQt5 import QtGui

from Forms.property_dlg import PropertyWindow
from NetworkRandomParams import NetworkRandomParams
from ChromosomeParams import ChromosomeParams
from Structures.Convolutional.C2dRandomParams import C2dRandomParams
from Structures.Dense.D2dRandomParams import D2dRandomParams
from Support import Support
from collections import deque
from threading import Thread

import socket
import time

from MPL_Canvas import MyMplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as Toolbar
import matplotlib.pyplot as plt
from Forms.plot_ui import PlotWindow

from Algorithms.GeneticProgram import GeneticProgramProcess

# from (ui filename) import (class)
# from Forms.project_gui import Ui_MainWindow
# from PyQt5.uic.Compiler.qtproxies import QtCore

from Forms.Parents.c2d_gui_parent import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, paramsQueue: deque, tasks_window):
        super().__init__()
        self.tasks_window = tasks_window
        self.paramsQueue = paramsQueue
        self.settings = QSettings()

        # self.queue_program_thread: QueueProgramThread = None
        self.setupUi(self)
        self.loadSettings()
        self.first_value = None
        self.second_value = None
        self.result = None
        self.example = ""
        self.equal = ""

        # self.paramsQueue = deque([])
        # queue_program_thread = QueueProgramThread(self.paramsQueue, self)
        # queue_program_thread.start()

        ############## Widgets Init #################
        self.lf_CCE_ChB.setChecked(True)


        # self.errorOutput_TE.geometry().moveTo(self.geneticOutput_TE.)
        # self.errorOutput_TE.move(self.geneticOutput_TE.mapToGlobal(QtCore.QPoint(0, 0)))
        #############################################

        ############## Widgets Listeners ############
        ###### Buttons ######
        self.search_Btn.clicked.connect(self.search_Btn_Click)
        self.train_Btn.clicked.connect(self.train_Btn_Click)
        self.DatasetPath_TB.clicked.connect(self.datasetPath_TB_Click)
        self.ModelsPath_TB.clicked.connect(self.modelsPath_TB_Click)
        self.LabelPath_TB.clicked.connect(self.labelPath_TB_Click)
        self.PlotPath_TB.clicked.connect(self.plotPath_TB_Click)
        self.modelCheckpoint_TB.clicked.connect(self.modelCheckpoint_TB_Click)
        self.tensorBoard_TB.clicked.connect(self.tensorBoard_TB_Click)
        self.earlyStopping_TB.clicked.connect(self.earlyStopping_TB_Click)
        self.scheduler_TB.clicked.connect(self.scheduler_TB_Click)
        self.terminateNaN_TB.clicked.connect(self.terminateNaN_TB_Click)
        self.ReduceLR_TB.clicked.connect(self.reduceLR_TB_Click)
        self.remoteMonitor_TB.clicked.connect(self.remoteMonitor_TB_Click)
        self.lambda_TB.clicked.connect(self.lambda_TB_Click)
        self.CSVLogger_TB.clicked.connect(self.CSVLogger_TB_Click)
        self.ProgbarLogger_TB.clicked.connect(self.progbarLogger_TB_Click)

        self.actionProperties.triggered.connect(self.show_properties_Click)

        # ############### Commutators ################
        # ####### Slots-Signals #######
        # # создадим поток
        # self.thread = QtCore.QThread()
        # # создадим объект для выполнения кода в другом потоке
        # self.ui_handler = UIHandler()
        # # перенесём объект в другой поток
        # self.ui_handler.moveToThread(self.thread)
        # # после чего подключим все сигналы и слоты
        # self.ui_handler.signal.connect(self.refresh_UI)
        # self.plot_ui = PlotWindow()
        # self.ui_handler.plot_signal.connect(self.plot_ui.refreshFigure)
        # # self.ui_handler.signal.
        # # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        # self.thread.started.connect(self.ui_handler.run)
        # # запустим поток
        # self.thread.start()
        # #############################
        ########### Naive ###########
        # self.sock_listener = SocketListener(self)
        # self.sock_listener.start()
        #############################

        ############################################

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # тут нужно спросить подтверждение и убить всех детей
        # qApp.quit()
        self.close()

    def loadSettings(self):
        self.DatasetPath_LE.setText(self.settings.value("datasetPath", "C:/", type=str))
        self.ModelPath_LE.setText(self.settings.value("modelsPath", "C:/", type=str))
        self.Labels_LE.setText(self.settings.value("labelPath", "C:/", type=str))
        self.PlotsPath_LE.setText(self.settings.value("plotPath", "C:/", type=str))

    ################## Listener`s methods ###############
    ####### Buttons ########
    def search_Btn_Click(self):
        self.paramsQueue.append(self.collectGUIParams())

    def train_Btn_Click(self):
        self.tasks_window.show()
        pass

    def datasetPath_TB_Click(self):
        # при нажатии на отмену валится
        dirlist = QFileDialog.getExistingDirectory(self, "Get Dataset folder",
                                                   self.settings.value("datasetPath", "C:/", type=str))
        if dirlist == "":
            self.DatasetPath_LE.setText(self.settings.value("datasetPath", "C:/", type=str))
        else:
            self.DatasetPath_LE.setText(dirlist)
            self.settings.setValue("datasetPath", dirlist)
            self.settings.sync()

    def modelsPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Models folder",
                                                   self.settings.value("modelsPath", "C:/", type=str))
        if dirlist == "":
            self.ModelPath_LE.setText(self.settings.value("modelsPath", "C:/", type=str))
        else:
            self.ModelPath_LE.setText(dirlist)
            self.settings.setValue("modelsPath", dirlist)
            self.settings.sync()

    def labelPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Labels folder",
                                                   self.settings.value("labelPath", "C:/", type=str))
        if dirlist == "":
            self.Labels_LE.setText(self.settings.value("labelPath", "C:/", type=str))
        else:
            self.Labels_LE.setText(dirlist)
            self.settings.setValue("labelPath", dirlist)
            self.settings.sync()

    def plotPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Plots folder",
                                                   self.settings.value("plotPath", "C:/", type=str))
        if dirlist == "":
            self.PlotsPath_LE.setText(self.settings.value("plotPath", "C:/", type=str))
        else:
            self.PlotsPath_LE.setText(dirlist)
            self.settings.setValue("plotPath", dirlist)
            self.settings.sync()

    def modelCheckpoint_TB_Click(self):
        pass

    def tensorBoard_TB_Click(self):
        pass

    def earlyStopping_TB_Click(self):
        pass

    def scheduler_TB_Click(self):
        pass

    def terminateNaN_TB_Click(self):
        pass

    def reduceLR_TB_Click(self):
        pass

    def remoteMonitor_TB_Click(self):
        pass

    def lambda_TB_Click(self):
        pass

    def CSVLogger_TB_Click(self):
        pass

    def progbarLogger_TB_Click(self):
        pass

    def show_properties_Click(self):
        self.propertyWindow = PropertyWindow()
        self.propertyWindow.exec()
        pass

        ###### Slots ##########

    # @QtCore.pyqtSlot(object)
    # def refresh_UI(self, data: dict):
    #     if data.get("target") == "geneticOutput_TE":
    #         if data.get("action") == "appendText":
    #             self.geneticOutput_TE.append(data.get("data"))
    #         elif data.get("action") == "clear":
    #             self.geneticOutput_TE.clear()
    #     elif data.get("target") == "chrOutput_TE":
    #         if data.get("action") == "appendText":
    #             self.chrOutput_TE.append(data.get("data"))
    #         elif data.get("action") == "clear":
    #             self.chrOutput_TE.clear()
    #     elif data.get("target") == "chr_plotting":
    #         pass
    #     elif data.get("target") == "search_plotting":
    #         pass
    #     elif data.get("target") == "search_PB":
    #         if data.get("action") == "setValue":
    #             self.progressBar.setValue(data.get("data"))

    #######################

    ################# Logic #############################
    def collectGUIParams(self):
        # Convolutional
        cActivations = []
        if self.cReLU_ChB.isChecked(): cActivations.append("relu")
        if self.cSoftMax_ChB.isChecked(): cActivations.append("softmax")
        if self.cLReLU_ChB.isChecked(): cActivations.append("Leaky ReLU")
        if self.cSoftSign_ChB.isChecked(): cActivations.append("softsign")
        if self.cSigmoid_ChB.isChecked(): cActivations.append("sigmoid")
        if self.cELU_ChB.isChecked(): cActivations.append("elu")
        if self.cSELU_ChB.isChecked(): cActivations.append("selu")
        if self.cSoftPlus_ChB.isChecked(): cActivations.append("softplus")
        if self.cTanh_ChB.isChecked(): cActivations.append("tang")
        if self.cPReLU_ChB.isChecked(): cActivations.append("PReLu")
        if self.cTReLU_ChB.isChecked(): cActivations.append("TReLU")

        dActivations = []
        if self.dReLU_ChB.isChecked(): dActivations.append("relu")
        if self.dSoftMax_ChB.isChecked(): dActivations.append("softmax")
        if self.dLReLU_ChB.isChecked(): dActivations.append("Leaky ReLU")
        if self.dSoftSign_ChB.isChecked(): dActivations.append("softsign")
        if self.dSigmoid_ChB.isChecked(): dActivations.append("sigmoid")
        if self.dELU_ChB.isChecked(): dActivations.append("elu")
        if self.dSELU_ChB.isChecked(): dActivations.append("selu")
        if self.dSoftPlus_ChB.isChecked(): dActivations.append("softplus")
        if self.dTanh_ChB.isChecked(): dActivations.append("tang")
        if self.dPReLU_ChB.isChecked(): dActivations.append("PReLu")
        if self.dTReLU_ChB.isChecked(): dActivations.append("TReLU")

        optimizers = []
        if self.optAdadelta_ChB.isChecked(): optimizers.append("adadelta")
        if self.optAdagrad_ChB.isChecked(): optimizers.append("adagrad")
        if self.optAdam_ChB.isChecked(): optimizers.append("adam")
        if self.optAdamax_ChB.isChecked(): optimizers.append("adamax")
        if self.optNadam_ChB.isChecked(): optimizers.append("nadam")
        if self.optRMSprop_ChB.isChecked(): optimizers.append("rmsprop")
        if self.optSGD_ChB.isChecked(): optimizers.append("sgd")

        loss_func = []
        if self.lf_BCE_ChB.isChecked(): loss_func.append("binary crossentropy")
        if self.lf_CCE_ChB.isChecked(): loss_func.append("categorical crossentropy")
        if self.lf_cHingle_ChB.isChecked(): loss_func.append("categorical hingle")
        if self.lf_CosProx_ChB.isChecked(): loss_func.append("Cosine proximity")
        if self.lf_Hingle_ChB.isChecked(): loss_func.append("hinge")
        if self.lf_KDL_ChB.isChecked(): loss_func.append("kdl")
        if self.lf_Logcosh.isChecked(): loss_func.append("logcosh")
        if self.lf_MAE_ChB.isChecked(): loss_func.append("mae")
        if self.lf_MAPE_ChB.isChecked(): loss_func.append("mape")
        if self.lf_MSE_ChB.isChecked(): loss_func.append("mse")
        if self.lf_MSLE_ChB.isChecked(): loss_func.append("msle")
        if self.lf_Poisson_ChB.isChecked(): loss_func.append("poisson")
        if self.lf_sCCE_ChB.isChecked(): loss_func.append("sparse categorical crossentropy")
        if self.lf_sqHingle_ChB.isChecked(): loss_func.append("squared hinge")

        callbacks = []
        if self.modelCheckpoint_ChB.isChecked(): callbacks.append(0)
        if self.tensorBoard_ChB.isChecked(): callbacks.append(1)
        if self.earlyStopping_ChB.isChecked(): callbacks.append(2)
        if self.scheduler_ChB.isChecked(): callbacks.append(3)
        if self.terminateNaN_ChB.isChecked(): callbacks.append(4)
        if self.ReduceLR_ChB.isChecked(): callbacks.append(5)
        if self.remoteMonitor_ChB.isChecked(): callbacks.append(6)
        if self.lambda_ChB.isChecked(): callbacks.append(7)
        if self.CSVLogger_ChB.isChecked(): callbacks.append(8)
        if self.ProgbarLogger_ChB.isChecked(): callbacks.append(9)

        nrp = NetworkRandomParams(self.constLR_ChB.isChecked(),
                                  [self.minLR_dSB.value(), self.maxLR_dSB.value()],
                                  self.DatasetPath_LE.text(), self.ModelPath_LE.text(), self.Labels_LE.text(),
                                  self.PlotsPath_LE.text(), self.netName_LE.text(), optimizers, loss_func,
                                  self.networkEpoch_SB.value(), self.batchSize_SB.value())
        c2d_rp = C2dRandomParams(self.maxConv_SB.value(),
                                 [self.min_filersPowIndex_SB.value(), self.max_filersPowIndex_SB.value()],
                                 len(cActivations), cActivations,
                                 [self.xKernel_SB.value(), self.yKernel_SB.value()],
                                 self.cDropout_ChB.isChecked(), self.cMaxDropout_SB.value())
        d2d_rp = D2dRandomParams(self.maxDense_SB.value(),
                                 [self.min_neuronsPowIndex_SB.value(), self.max_neuronsPowIndex_SB.value()],
                                 Support.getOutputNumb(self.DatasetPath_LE.text()), len(dActivations),
                                 dActivations, self.dDropout_ChB.isChecked(), self.dMaxDropout_SB.value())
        gp = ChromosomeParams(nrp, c2d_rp, d2d_rp, self.evolEpoch_SB.value(),
                              [self.copy_SB.value(), self.cross_SP.value(), self.mutate_SB.value()],
                              self.popSize_SB.value(), self.estimatingWay_CB.currentIndex(), 2,
                              self.mutateRate_SB.value(), 1, 1)
        return gp

    #####################################################


# class UIHandler(QtCore.QObject):
#     signal = QtCore.pyqtSignal(object)
#     plot_signal = QtCore.pyqtSignal(object)
#
#     def __init__(self):
#         self.sock = socket.socket()
#         self.sock.bind(('localhost', 12246))
#         self.sock.listen(1)
#         super().__init__()
#
#     def run(self):
#         conn, addr = self.sock.accept()
#         while True:
#             data = conn.recv(20480).decode('UTF-8')
#             if not data:
#                 continue
#             datalist = data.split('&')
#             if datalist[-1] == "": datalist.pop()
#             for data in datalist:
#                 #data = eval(data)
#                 data = json.loads(data)
#                 if data.get("action") == "reconnect":
#                     conn, addr = self.sock.accept()
#                     pass
#                 elif data.get("target") == "plot_ui":
#                     self.plot_signal.emit(data)
#                 else:
#                     self.signal.emit(data)
#             QtCore.QThread.msleep(1000)


class SocketListener(Thread):
    def __init__(self, mainwindow: MainWindow):
        self.sock = socket.socket()
        self.sock.bind(('localhost', 12246))
        self.sock.listen(1)
        self.mainwindow = mainwindow
        Thread.__init__(self)

    def run(self) -> None:
        conn, addr = self.sock.accept()
        while True:
            data = conn.recv(20480).decode('UTF-8')
            if not data:
                continue
            datalist = data.split('}')
            datalist.pop()
            for data in datalist:
                data = eval(data + "}")
                if data.get("codeword") == "geneticOutput_TE":
                    self.mainwindow.geneticOutput_TE.append(data.get("data"))
                    time.sleep(0.1)
                    self.mainwindow.geneticOutput_TE.verticalScrollBar().setValue(
                        self.mainwindow.geneticOutput_TE.verticalScrollBar().maximum())
                elif data.get("codeword") == "chrOutput_TE":
                    self.mainwindow.chrOutput_TE.append(data.get("data"))
                elif data.get("codeword") == "chr_plotting":
                    pass
                elif data.get("codeword") == "search_plotting":
                    pass
                elif data.get("codeword") == "search_PB":
                    self.mainwindow.progressBar.setValue(data.get("data"))


# class QueueProgramThread(Thread):
#     def __init__(self, chr_q: deque, main_window: MainWindow):
#         super().__init__()
#         self.chromosome_params_queue = chr_q
#         self.main_window = main_window
#
#     def run(self):
#         # while len(self.chromosome_params_queue) > 0:
#         while True:
#             if len(self.chromosome_params_queue) != 0:
#                 chromosome_params = self.chromosome_params_queue.popleft()
#                 prog = GeneticProgramProcess(chromosome_params)
#                 prog.run()
#                 # процесс стопит поток или нет? Yes
#             else: time.sleep(1)


if __name__ == '__main__':
    # Новый экземпляр QApplication
    QCoreApplication.setOrganizationName("QSoft")
    QCoreApplication.setApplicationName("NN Family Creater")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # print(QtWidgets.QStyleFactory.keys())
    # app.setStyle('Windows')
    # app.setStyle('windowsvista')
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    mainWindow = MainWindow(deque([]))
    mainWindow.show()
    # Запуск
    sys.exit(app.exec_())
