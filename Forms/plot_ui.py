import json

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from Forms.plot_gui_parent import Ui_MainWindow

from MPL_Canvas import MyMplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as Toolbar
import matplotlib.pyplot as plt
import pandas as pd


class PlotWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.tempMetrics = pd.DataFrame()
        self.tempAccuracy = pd.DataFrame()
        self.tempParams = pd.DataFrame()
        self.tempAssessments = pd.DataFrame()

        ########## Testing ##########
        x = np.arange(0, 5, 0.1)
        y = np.sin(x)
        self.figure = plt.figure()

        egrid = (2, 3)
        ########## 1 Ax ##########
        self.ax1 = plt.subplot2grid(egrid, (0, 0))
        self.ax1.set_title("Assessments - Epoch")
        self.ax1.set_xlabel("Epoch #")
        self.ax1.set_ylabel("Assessments")
        ###########################

        ########## 1 Ax ##########
        self.ax2 = plt.subplot2grid(egrid, (0, 1))
        ###########################

        ########## 1 Ax ##########
        self.ax3 = plt.subplot2grid(egrid, (0, 2))
        ###########################

        ########## 1 Ax ##########
        self.ax4 = plt.subplot2grid(egrid, (1, 0))
        self.ax4.set_title("Training Loss and Accuracy (CNN)")
        self.ax4.set_xlabel("Epoch #")
        self.ax4.set_ylabel("Loss/Accuracy")
        ###########################

        ########## 1 Ax ##########
        self.ax5 = plt.subplot2grid(egrid, (1, 1))
        ###########################

        ########## 1 Ax ##########
        self.ax6 = plt.subplot2grid(egrid, (1, 2))
        ###########################

        self.ax6.plot(x, y)
        self.ax6.plot(y, x)
        self.ax6 = plt.plot(x / 2, y / 2)
        self.ax6 = plt.plot(y / 2, x / 2)
        plt.tight_layout()

        self.lineUpping = QtWidgets.QVBoxLayout(self.widget)
        self.canvas = MyMplCanvas(self.figure)
        self.lineUpping.addWidget(self.canvas)
        self.toolbar = Toolbar(self.canvas, self)
        self.lineUpping.addWidget(self.toolbar)
        #############################

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()

    @QtCore.pyqtSlot(object)
    def refreshFigure(self, data: dict):
        if data.get("action") == "chr_plotting":
            self.ax4.clear()
            data_for_plotting = json.loads(data.get("data"))
            N = np.arange(0, data_for_plotting.get("epoch_deFacto"))
            loss = data_for_plotting.get("loss")
            val_loss = data_for_plotting.get("val_loss")
            acc = data_for_plotting.get("acc")
            val_acc = data_for_plotting.get("val_acc")

            self.ax4.plot(N, loss, label="train_loss")
            self.ax4.plot(N, val_loss, label="val_loss")
            self.ax4.plot(N, acc, label="train_acc")
            self.ax4.plot(N, val_acc, label="val_acc")
            self.ax4.set_title("Training Loss and Accuracy (CNN)")
            self.ax4.set_xlabel("Epoch #")
            self.ax4.set_ylabel("Loss/Accuracy")
            self.ax4.legend(bbox_to_anchor=(1.05, 1))

            pass
        elif data.get("action") == "search_plotting":
            pass
        elif data.get("action") == "clear":
            for ax in self.figure.axes:
                pass
            pass
        elif data.get("action") == "assessment":
            v = data.get("data")
            # vs = pd.DataFrame.from_dict([v])
            vs = pd.DataFrame([v])
            self.tempAssessments = self.tempAssessments.append(vs, ignore_index=True, sort=True)
            self.ax1.clear()
            # self.ax1 = self.tempMetrics.plot(self.tempAssessments["epoch"], self.tempAssessments["Chromosome(0)"])
            # self.ax1.plot(self.tempAssessments["epoch"], self.tempAssessments["Chromosome(0)"])
            for i in self.tempAssessments.columns:
                if i != "epoch":
                    self.ax1.plot(self.tempAssessments["epoch"].values, self.tempAssessments[i].values, label=i)

            self.ax1.set_title("Assessments - Epoch")
            self.ax1.set_xlabel("Epoch #")
            self.ax1.set_ylabel("Assessments")
            self.ax1.legend(bbox_to_anchor=(1.05, 1))
            self.canvas.draw()

            pass
        elif data.get("action") == "accuracy":
            add = data.get("data")
            add = pd.DataFrame([add])
            self.tempAccuracy = self.tempAccuracy.append(add, ignore_index=True, sort=True)

            self.ax2.clear()
            for i in self.tempAccuracy.columns:
                if i != "epoch":
                    self.ax2.plot(self.tempAccuracy["epoch"].values, self.tempAccuracy[i].values, label=i)

            self.ax2.set_title("Accuracy - Epoch")
            self.ax2.set_xlabel("Epoch #")
            self.ax2.set_ylabel("Accuracy")
            self.ax2.legend(bbox_to_anchor=(1.05, 1))
            self.canvas.draw()
            pass
        elif data.get("action") == "params":
            add = data.get("data")
            add = pd.DataFrame([add])
            self.tempParams = self.tempParams.append(add, ignore_index=True, sort=True)

            self.ax3.clear()
            for i in self.tempAccuracy.columns:
                if i != "epoch":
                    self.ax3.plot(self.tempParams["epoch"].values, self.tempParams[i].values, label=i)

            self.ax3.set_title("Accuracy - Epoch")
            self.ax3.set_xlabel("Epoch #")
            self.ax3.set_ylabel("Accuracy")
            self.ax3.legend(bbox_to_anchor=(1.05, 1))
            self.canvas.draw()

        elif data.get("action") == "init":
            popSize = data.get("data")
            columns = ["epoch"]
            for i in range(popSize):
                column_name = "Chromosome(" + str(i + 1) + ")"
                columns.append(column_name)
            self.tempAssessments = pd.DataFrame(columns=columns)

        self.canvas.draw()
