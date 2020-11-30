import sys

import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton


class MyCustomWidget(QWidget):
    def __init__(self, name, parent=None):
        super(MyCustomWidget, self).__init__(parent)

        self.row = QHBoxLayout()

        self.row.addWidget(QLabel(name))
        self.row.addWidget(QPushButton("view"))
        self.row.addWidget(QPushButton("select"))

        self.setLayout(self.row)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the list

        mylist = QListWidget()
        self.setCentralWidget(mylist)
        # Add to list a new item (item is simply an entry in your list)
        item = QListWidgetItem(mylist)
        mylist.addItem(item)

        # Instanciate a custom widget
        row = MyCustomWidget("1")
        item.setSizeHint(row.minimumSizeHint())

        # Associate the custom widget to the list entry
        mylist.setItemWidget(item, row)


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
