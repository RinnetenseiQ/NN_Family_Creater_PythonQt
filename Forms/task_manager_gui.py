import sys
from collections import deque

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QCoreApplication

from Forms.Parents.task_manager_gui_parent import Ui_QueueWindow
from Forms.plot_ui import PlotWindow


class TasksWindow(QtWidgets.QMainWindow, Ui_QueueWindow):
    def __init__(self, plot_ui: PlotWindow, paramsQueue: deque):
        super().__init__()
        self.paramsQueue = paramsQueue
        self.plot_ui = plot_ui
        self.settings = QSettings()

        self.setupUi(self)
        # self.loadSettings()
        self.initWidgets()

    def initWidgets(self):
        self.errorneous_output_TE.setVisible(False)
        self.errorneous_output_TE.move(self.optimizin_output_TE.mapToParent(QtCore.QPoint(0, 0)))
        self.errorneous_output_TE.resize(self.optimizin_output_TE.size())

        self.chr_output_TE.setVisible(False)
        self.chr_output_TE.move(self.optimizin_output_TE.mapToParent(QtCore.QPoint(0, 0)))
        self.chr_output_TE.resize(self.optimizin_output_TE.size())

        self.comboBox.addItem("Current optimization search output")
        self.comboBox.addItem("Erroneous output")
        self.comboBox.addItem("Current chromosome output")

        self.comboBox.activated.connect(self.combobox_SelectedIndex_changed)
        self.clear_Btn.clicked.connect(self.clear_Btn_Click)
        self.pause_Btn.clicked.connect(self.pause_Btn_Click)
        self.plots_Btn.clicked.connect(self.plots_Btn_Click)

        ####### Testing #######

        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()

    def clear_Btn_Click(self):
        pass

    def pause_Btn_Click(self):
        pass

    def plots_Btn_Click(self):
        self.plot_ui.show()
        #self.plot_ui.update()
        pass

    def combobox_SelectedIndex_changed(self):
        if self.comboBox.currentIndex() == 0:
            self.optimizin_output_TE.setVisible(True)
            self.errorneous_output_TE.setVisible(False)
            self.chr_output_TE.setVisible(False)
        elif self.comboBox.currentIndex() == 1:
            self.optimizin_output_TE.setVisible(False)
            self.errorneous_output_TE.setVisible(True)
            self.chr_output_TE.setVisible(False)
        elif self.comboBox.currentIndex() == 2:
            self.optimizin_output_TE.setVisible(False)
            self.errorneous_output_TE.setVisible(False)
            self.chr_output_TE.setVisible(True)
        pass

    @QtCore.pyqtSlot(object)
    def refresh_output(self, data: dict):
        if data.get("target") == "geneticOutput_TE":
            if data.get("action") == "appendText":
                self.optimizin_output_TE.append(data.get("data"))
            elif data.get("action") == "clear":
                self.optimizin_output_TE.clear()
        elif data.get("target") == "chrOutput_TE":
            if data.get("action") == "appendText":
                self.chr_output_TE.append(data.get("data"))
            elif data.get("action") == "clear":
                self.chr_output_TE.clear()


if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    QCoreApplication.setOrganizationName("QSoft")
    # QCoreApplication.setOrganizationDomain("Settings")
    QCoreApplication.setApplicationName("NN Family Creater")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    mainWindow = TasksWindow()
    # Запуск
    sys.exit(app.exec_())
