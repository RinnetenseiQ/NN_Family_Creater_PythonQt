import sys

import qdarkstyle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import os
os.path

from Forms.Parents.exp_gui_parent import Ui_MainWindow



class Exp_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.pushButton.setIcon()
        #icon = QIcon("..Forms/resourses/archive_folder_80px.png")
        # self.pushButton.setText("1")
        # self.pushButton.setIcon(QIcon("resourses\\archive_folder_80px.png"))
        # self.pushButton_2.setIcon(QIcon("archive_folder_80px.png"))
        # self.pushButton_3.setIcon(QIcon("C:\\Users\\Rinnetensei\\PycharmProjects\\NN_Family_Creater\\Forms\\resourses\\archive_folder_80px.png"))
        # self.pushButton.setIcon(QIcon("../Forms/resourses/archive_btn.png"))
        # self.pushButton.setIconSize(QtCore.QSize(24, 24))
        # self.pushButton.setStyleSheet("background-image : url(archive_folder_80px.png);")
        # self.pushButton.setIconSize(QtCore.QSize(24, 24))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    # app.setSt
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    startWindow = Exp_Window()
    startWindow.show()
    # Запуск
    sys.exit(app.exec_())
