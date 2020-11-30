import sys

import qdarkstyle
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QtWidgets.QTableWidget()
        #self.table.setColumnCount(3)
        self.table.setColumnCount(1)
        self.setCentralWidget(self.table)
        #data1 = ['row1', 'row2', 'row3', 'row4']
        #data2 = ['1', '2.0', '3.00000001', '3.9999999']

        self.table.setRowCount(4)
        for index in range(4):
            item = QtWidgets.QHBoxLayout()
            item.addWidget(QtWidgets.QLabel(text="item {}".format(index)))
            item.addWidget(QtWidgets.QProgressBar())
            item.addWidget(QtWidgets.QPushButton(text="{}".format(index)))
            #i = self.table.model().index(index, 0)
            #self.table.setIndexWidget(i, item)
            self.table.setItemDelegateForRow(index, TableHLayout("1"))
            #self.table.setItem(index, 0, item)
            #self.table.setCellWidget(index, 0, item)

        # Create the list
        mylist = QListWidget()

        # Add to list a new item (item is simply an entry in your list)
        item = QListWidgetItem(mylist)
        mylist.addItem(item)

        # Instanciate a custom widget
        row = MyCustomWidget()
        item.setSizeHint(row.minimumSizeHint())

        # Associate the custom widget to the list entry
        mylist.setItemWidget(item, row)


        # for index in range(4):
        #     item1 = QtWidgets.QTableWidgetItem(data1[index])
        #     self.table.setItem(index, 0, item1)
        #     item2 = QtWidgets.QTableWidgetItem(data2[index])
        #     self.table.setItem(index, 1, item2)
        #     self.btn_sell = QtWidgets.QPushButton('Edit')
        #     self.btn_sell.clicked.connect(self.handleButtonClicked)
        #     self.table.setCellWidget(index, 2, self.btn_sell)

    def handleButtonClicked(self):
        button = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())


class TableHLayout(QtWidgets.QWidget):
    def __init__(self, name, parent=None):
        super(TableHLayout, self).__init__(parent)

        self.row = QHBoxLayout()

        self.row.addWidget(QLabel(name))
        self.row.addWidget(QPushButton("view"))
        self.row.addWidget(QPushButton("select"))

        self.setLayout(self.row)

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
