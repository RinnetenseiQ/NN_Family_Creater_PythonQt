import math
import platform
import sys
import numpy as np
import matplotlib.pyplot as plt

import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication

from Forms.Parents.property_gui_parent import Ui_Dialog
from MPL_Canvas import MyMplCanvas
import sip


class PropertyWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initWidgets()
        self.temp_properties = {"app_theme": 0, "app_style": 0, "plot_style": 0}

    def initWidgets(self):
        self.comboBox.addItem("Dark theme")
        self.comboBox.addItem("Light theme")
        os_name = platform.system()

        self.figure = plt.figure()
        self.lineUpping = QtWidgets.QVBoxLayout(self.widget)
        self.canvas = MyMplCanvas(self.figure)
        self.lineUpping.addWidget(self.canvas)

        x = np.array([1, 2, 3, 4, 5])
        y = np.sin(x)
        self.ax1 = plt.plot(x, y, label="xy")
        self.ax1 = plt.plot(y, x, label="yx")
        self.ax1 = plt.plot(y / 2, x / 2, label="yx/2")
        self.ax1 = plt.plot(x / 2, y / 2, label="xy/2")

        self.plt_themes = ['Solarize_Light2',
                           '_classic_test_patch',
                           'bmh',
                           'classic',
                           'dark_background',
                           'fast',
                           'fivethirtyeight',
                           'ggplot',
                           'grayscale',
                           'seaborn',
                           'seaborn-bright',
                           'seaborn-colorblind',
                           'seaborn-dark',
                           'seaborn-dark-palette',
                           'seaborn-darkgrid',
                           'seaborn-deep',
                           'seaborn-muted',
                           'seaborn-notebook',
                           'seaborn-paper',
                           'seaborn-pastel',
                           'seaborn-poster',
                           'seaborn-talk',
                           'seaborn-ticks',
                           'seaborn-white',
                           'seaborn-white',
                           'seaborn-whitegrid',
                           'tableau-colorblind1']

        self.comboBox_3.addItems(self.plt_themes)

        app_linux_styles = ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
        app_windows_styles = ['Windows', 'Fusion', 'windowsvista']
        if os_name == 'Windows':
            self.comboBox_2.addItems(app_windows_styles)
        elif app_linux_styles == 'Linux':
            self.comboBox_2.addItems(app_linux_styles)

        # QtWidgets.QApplication.instance()

        # self.
        self.comboBox.activated.connect(self.combobox_SelectedIndexChanged)
        self.comboBox_2.activated.connect(self.combobox_2_SelectedIndexChanged)
        self.comboBox_3.activated.connect(self.combobox_3_SelectedIndexChanged)


        pass

    def cancel_Btn_Click(self):
        pass

    def apply_Btn_Click(self):
        pass

    def ok_Btn_Click(self):
        pass

    def combobox_SelectedIndexChanged(self):
        self.temp_properties["app_theme"] = self.comboBox.currentIndex()
        app = QtWidgets.QApplication.instance()
        if self.comboBox.currentIndex() == 0:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
        elif self.comboBox.currentIndex() == 1:
            # QtWidgets.QApplication.setStyleSheet('')
            app.setStyleSheet('')

    def combobox_2_SelectedIndexChanged(self):
        self.temp_properties["app_style"] = self.comboBox_2.currentIndex()
        index = self.comboBox_2.currentIndex()
        setAppStyle(windows_theme=index, linux_theme=index)

    def combobox_3_SelectedIndexChanged(self):
        self.temp_properties["plot_style"] = self.comboBox_3.currentIndex()
        self.ax1.clear()

        setPlotStyle(self.plt_themes, self.comboBox_3.currentIndex())

        #plt.draw()

        sip.delete(self.canvas)
        plt.close()
        self.figure = plt.figure(constrained_layout=True)
        x = np.array([1, 2, 3, 4, 5])
        y = np.sin(x)
        self.ax1 = plt.plot(x, y, label="xy")
        self.ax1 = plt.plot(y, x, label="yx")
        self.ax1 = plt.plot(y / 2, x / 2, label="yx/2")
        self.ax1 = plt.plot(x / 2, y / 2, label="xy/2")


        self.canvas = MyMplCanvas(self.figure)
        #self.figure.show()
        self.lineUpping.addWidget(self.canvas)
        self.canvas.draw()
        #self.update()
        # self.hide()
        # self.show()

        pass


def setPlotStyle(themes, style: int):
    plt.style.use(themes[style])

    # plt.style.context(themes[style])


def setAppStyle(windows_theme: int = 0, linux_theme: int = 0):
    app_linux_styles = ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app_windows_styles = ['Windows', 'Fusion', 'windowsvista']
    app = QtWidgets.QApplication.instance()
    os_name = platform.system()
    if os_name == 'Windows':
        app.setStyle(app_windows_styles[windows_theme])
    elif os_name == 'Linux':
        app.setStyle(app_linux_styles[linux_theme])


if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    QCoreApplication.setOrganizationName("QSoft")
    # QCoreApplication.setOrganizationDomain("Settings")
    QCoreApplication.setApplicationName("NN Family Creater")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    window = PropertyWindow()
    # Запуск
    sys.exit(app.exec_())
