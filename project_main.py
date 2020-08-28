from PySide2 import QtWidgets
import sys
#from (ui filename) import (class)
from Forms.project_gui import Ui_MainWindow


class Calculator(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		
		self.setupUi(self)
		self.show()
		self.first_value = None
		self.second_value = None
		self.result = None
		self.example = ""
		self.equal = ""


if __name__ == '__main__':
    # Новый экземпляр QApplication
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    #app.setStyle('windowsvista')
    #app.setStyle('Windows')
    #print(QStyleFactory.keys())
    # Сздание инстанса класса
    calc = Calculator()
    # Запуск
    sys.exit(app.exec_())