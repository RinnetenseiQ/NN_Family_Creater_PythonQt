from PyQt5 import QtWidgets, QtCore

from Forms.Parents.early_stopping_gui_parent import Ui_EarlyStoppingWindow


class EarlyStoppingDlg(QtWidgets.QDialog, Ui_EarlyStoppingWindow):
    signal = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.OK_Btn.clicked.connect(self.OK_Btn_Clicked)
        self.initWidgets()

    def initWidgets(self):
        self.setWindowTitle("Early Stopping Callback Properties")
        self.monitor_CB.addItems(["loss", "acc", "val_loss", "val_acc"])  # {loss,acc,val_loss,val_acc}
        self.mode_CB.addItems(["min", "max", "auto"])

        # set qsettings here
        pass

    def OK_Btn_Clicked(self):
        data = {"monitor": self.monitor_CB.currentText(),
                "min_delta": self.delta_dSB.value(),
                "patience": self.patience_SB.value(),
                "mode": self.mode_CB.currentText(),  # {min, max, auto}
                "restore_best_weights": self.weights_ChB.isChecked(),
                "verbose": 1 if self.verbose_ChB.isChecked() else 0}
        self.signal.emit(data)
        self.reject()
        # self.done(0)
