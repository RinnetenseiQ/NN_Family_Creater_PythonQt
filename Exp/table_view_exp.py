import sys

import qdarkstyle
from PyQt5 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)
        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QtWidgets.QTableWidgetItem(data1[index])
            self.table.setItem(index,0,item1)
            item2 = QtWidgets.QTableWidgetItem(data2[index])
            self.table.setItem(index,1,item2)
            self.btn_sell = QtWidgets.QPushButton('Edit')
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.table.setCellWidget(index,2,self.btn_sell)

    def handleButtonClicked(self):
        button = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())

if __name__ == "__main__":
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
    startWindow = MainWindow()
    startWindow.show()
    # Запуск
    sys.exit(app.exec_())