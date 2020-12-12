import sys

import cv2
import qdarkstyle
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap

from Forms.Parents.predict_c2d_gui_parent import Ui_PredictC2DWindow
from master.Webcam_captures.Video_capture import Video_capture


class PredictC2DWindow(QtWidgets.QMainWindow, Ui_PredictC2DWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.capture = Video_capture()
        self.thread = QtCore.QThread()
        self.capture.moveToThread(self.thread)
        self.capture.signal.connect(self.getImages)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.capture.run)
        # запустим поток
        self.thread.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.capture
        self.thread.quit()

    def open_c2d_model(self, path: str):
        pass

    @QtCore.pyqtSlot(object)
    def getImages(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qImg))
        pass



if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    QCoreApplication.setOrganizationName("QSoft")
    # QCoreApplication.setOrganizationDomain("Settings")
    QCoreApplication.setApplicationName("NN Family Creater")

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
    capture_window = PredictC2DWindow()
    capture_window.show()
    # Запуск
    sys.exit(app.exec_())