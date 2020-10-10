from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as qtCanvas
from PyQt5.QtWidgets import QSizePolicy


class MyMplCanvas(qtCanvas):
    def __init__(self, figure):
        self.figure = figure
        qtCanvas.__init__(self, self.figure)
        qtCanvas.setSizePolicy(self,
                               QSizePolicy.Expanding,
                               QSizePolicy.Expanding)
        qtCanvas.updateGeometry(self)
