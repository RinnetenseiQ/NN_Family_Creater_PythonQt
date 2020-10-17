import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QSettings

from Forms.Parents.start_page_gui_parent import Ui_StartPageWindow
from Forms.c2d_gui import MainWindow


class StartPageWindow(QtWidgets.QMainWindow, Ui_StartPageWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()

        self.setupUi(self)
        # self.loadSettings()
        self.initWidgets()

        self.show()

    def initWidgets(self):
        self.comboBox.addItem("Convolutional 2D NN")

        self.comboBox_2.addItem("Genetic optimize")
        self.comboBox_2.addItem("Immune optimize")
        self.comboBox_2.addItem("Custom")

        self.pushButton_2.clicked.connect(self.create_Btn_Click)

    def create_Btn_Click(self):
        if self.comboBox.currentIndex() == 0:
            if self.comboBox.currentIndex() == 0:
                mainWindow = MainWindow()
                mainWindow.show()
                self.hide()

        pass


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
    startWindow = StartPageWindow()
    # Запуск
    sys.exit(app.exec_())
