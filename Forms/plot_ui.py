import json

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from Forms.Parents.plot_gui_parent import Ui_MainWindow

from MPL_Canvas import MyMplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as Toolbar
import matplotlib.pyplot as plt
import pandas as pd


def setOneAxesProperties(ax, title, x_label, y_label):
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    pass


class PlotWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.tempMetrics = pd.DataFrame()
        self.tempAccuracy = pd.DataFrame()
        self.tempParams = pd.DataFrame()
        self.tempAssessments = pd.DataFrame()

        self.initFigure()
        self.canvas.draw()

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
            #self.ax4.plot([data_for_plotting.get("epoch_deJure"), 0], [data_for_plotting.get("epoch_deJure"), 5])
            setOneAxesProperties(self.ax4, "Training Loss and Accuracy (CNN)", "Epoch #", "Loss/Accuracy")
            self.ax4.legend(bbox_to_anchor=(1.05, 1))
            pass
        elif data.get("action") == "search_plotting":
            pass
        elif data.get("action") == "clear":
            for ax in self.figure.axes:
                ax.clear()
            self.setAllAxesProperties()
            pass
        elif data.get("action") == "assessment":
            v = data.get("data")
            vs = pd.DataFrame([v])
            self.tempAssessments = self.tempAssessments.append(vs, ignore_index=True, sort=True)
            self.ax1.clear()
            for i in self.tempAssessments.columns:
                if i != "epoch":
                    self.ax1.plot(self.tempAssessments["epoch"].values, self.tempAssessments[i].values, label=i)
                    self.ax1.scatter(self.tempAssessments["epoch"].values, self.tempAssessments[i].values)
                    # https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.scatter.html

            # self.ax1.legend(bbox_to_anchor=(1.05, 1))
            setOneAxesProperties(self.ax1, "Assessments - Epoch", "Epoch #", "Assessments")
            self.canvas.draw()

            pass
        elif data.get("action") == "accuracy":
            add = data.get("data")
            adds = pd.DataFrame([add])
            # print(add.values)
            # print(self.tempAccuracy)
            self.tempAccuracy = self.tempAccuracy.append(add, ignore_index=True, sort=True)
            # self.tempAccuracy = self.tempAccuracy.append(adds, ignore_index=True, sort=False)
            # print(self.tempAccuracy)

            self.ax2.clear()
            for i in self.tempAccuracy.columns:
                if i != "epoch":
                    self.ax2.plot(self.tempAccuracy["epoch"].values, self.tempAccuracy[i].values, label=i)
                    self.ax2.scatter(self.tempAccuracy["epoch"].values, self.tempAccuracy[i].values)

            setOneAxesProperties(self.ax2, "Accuracy - Epoch", "Epoch #", "Accuracy")
            # self.ax2.legend(bbox_to_anchor=(1.05, 1))
            self.canvas.draw()
            pass
        elif data.get("action") == "params":
            add = data.get("data")
            adds = pd.DataFrame([add])
            # self.tempParams = self.tempParams.append(adds)
            # self.tempParams = self.tempParams.append(adds, ignore_index=True, sort=False)
            self.tempParams = self.tempParams.append(adds, ignore_index=True, sort=True)

            self.ax3.clear()
            for i in self.tempAccuracy.columns:
                if i != "epoch":
                    self.ax3.plot(self.tempAccuracy[i].values, self.tempParams[i].values, label=i)
                    self.ax3.scatter(self.tempAccuracy[i].values, self.tempParams[i].values)

            setOneAxesProperties(self.ax3, "Accuracy - Params", "Accuracy", "Params")
            # self.ax3.legend(bbox_to_anchor=(1.05, 1))

            #### Testing
            self.ax5.clear()
            for i in self.tempParams.columns:
                if i != "epoch":
                    self.ax5.plot(self.tempParams["epoch"].values, self.tempParams[i].values, label=i)
                    self.ax5.scatter(self.tempParams["epoch"].values, self.tempParams[i].values)
            setOneAxesProperties(self.ax5, "Params - Epoch", "Epoch", "Params")
            self.canvas.draw()

        elif data.get("action") == "init":
            popSize = data.get("data")
            columns = ["epoch"]
            for i in range(popSize):
                column_name = "Chromosome(" + str(i + 1) + ")"
                columns.append(column_name)
            self.tempAssessments = pd.DataFrame(columns=columns)

        self.canvas.draw()

    def setAllAxesProperties(self):
        setOneAxesProperties(self.ax1, "Assessments - Epoch", "Epoch #", "Assessments")
        setOneAxesProperties(self.ax2, "Accuracy - Epoch", "Epoch #", "Accuracy")
        setOneAxesProperties(self.ax3, "Accuracy - Params", "Accuracy", "Params")
        setOneAxesProperties(self.ax4, "Training Loss and Accuracy (CNN)", "Epoch #", "Loss/Accuracy")
        setOneAxesProperties(self.ax5, "Title", "X", "Y")
        setOneAxesProperties(self.ax6, "Title", "X", "Y")

        # plt.constrained_layout()
        # plt.tight_layout()
        pass

    def initFigure(self):
        # self.figure = plt.figure(constrained_layout=True)
        setPlotStyle(0)

        self.figure = plt.figure()
        # plt.rcParams['figure.constrained_layout.use'] = True

        # https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.figure.html
        egrid = (2, 3)
        self.ax1 = plt.subplot2grid(egrid, (0, 0))
        self.ax2 = plt.subplot2grid(egrid, (0, 1))
        self.ax3 = plt.subplot2grid(egrid, (0, 2))
        self.ax4 = plt.subplot2grid(egrid, (1, 0))
        self.ax5 = plt.subplot2grid(egrid, (1, 1))
        self.ax6 = plt.subplot2grid(egrid, (1, 2))
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.subplot2grid.html

        self.setAllAxesProperties()
        self.lineUpping = QtWidgets.QVBoxLayout(self.widget)
        self.canvas = MyMplCanvas(self.figure)
        self.lineUpping.addWidget(self.canvas)
        self.toolbar = Toolbar(self.canvas, self)
        self.lineUpping.addWidget(self.toolbar)
        pass


def setPlotStyle(style: int):
    # plt.style.use('Solarize_Light2')
    # plt.style.use('_classic_test_patch')
    # plt.style.use('bmh')
    # plt.style.use('classic')
    # plt.style.use('dark_background')
    # plt.style.use('fast')
    # plt.style.use('fivethirtyeight')
    # plt.style.use('ggplot')
    # plt.style.use('grayscale')
    plt.style.use('seaborn')
    # plt.style.use('seaborn-bright')
    # plt.style.use('seaborn-colorblind')
    # plt.style.use('seaborn-dark')
    # plt.style.use('seaborn-dark-palette')
    # plt.style.use('seaborn - darkgrid')
    # plt.style.use('seaborn - deep')
    # plt.style.use('seaborn - muted')
    # plt.style.use('seaborn - notebook')
    # plt.style.use('seaborn - paper', )
    # plt.style.use('seaborn - pastel')
    # plt.style.use('seaborn - poster')
    # plt.style.use('seaborn - talk')
    # plt.style.use('seaborn - ticks')
    # plt.style.use('seaborn - white')
    # plt.style.use('seaborn-white')
    # plt.style.use('seaborn-whitegrid')
    # plt.style.use('tableau - colorblind1')
    pass
