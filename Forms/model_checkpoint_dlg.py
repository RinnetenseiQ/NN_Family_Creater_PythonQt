from PyQt5 import QtWidgets
from Forms.Parents.model_checkpoint_gui_parent import Ui_ModelCheckpointWindow


class ModelCheckpointDlg(QtWidgets.QDialog, Ui_ModelCheckpointWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initWidgets()

    def initWidgets(self):
        pass
