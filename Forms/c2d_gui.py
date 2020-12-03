# from PySide2 import QtWidgets
import sys
from collections import deque

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QFileDialog

from Callbacks.CallbacksHandler import CallbacksHandler
from Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams
from Forms.Parents.c2d_gui_parent import Ui_MainWindow
from Forms.early_stopping_dlg import EarlyStoppingDlg
from Forms.model_checkpoint_dlg import ModelCheckpointDlg
from Forms.property_dlg import PropertyWindow
from Structures.NetworkRandomParams import NetworkRandomParams
from Project_controller import Project_controller
from Structures.Convolutional.C2dRandomParams import C2dRandomParams
from Structures.Dense.D2dRandomParams import D2dRandomParams
import Support


# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput


# from (ui filename) import (class)
# from Forms.project_gui import Ui_MainWindow
# from PyQt5.uic.Compiler.qtproxies import QtCore


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, paramsQueue: deque, project_controller: Project_controller):
        super().__init__()
        self.project_controller = project_controller
        self.paramsQueue = paramsQueue
        self.settings = QSettings()
        self.callbacks_handler = CallbacksHandler()
        self.setupUi(self)
        self.loadSettings()
        self.first_value = None
        self.second_value = None
        self.result = None
        self.example = ""
        self.equal = ""

        ############## Widgets Init #################
        self.lf_CCE_ChB.setChecked(True)

        self.connect_all()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # тут нужно спросить подтверждение и убить всех детей
        # qApp.quit()
        self.close()

    def loadSettings(self):
        self.DatasetPath_LE.setText(self.settings.value("datasetPath", "C:/", type=str))
        self.ModelPath_LE.setText(self.settings.value("modelsPath", "C:/", type=str))
        self.Labels_LE.setText(self.settings.value("labelPath", "C:/", type=str))
        self.PlotsPath_LE.setText(self.settings.value("plotPath", "C:/", type=str))

        self.set_activations_state()
        self.set_optimizers()
        self.set_loss()
        self.set_callbacks()

        x_kernel, y_kernel = self.project_controller.params.c2d_rp.kernelSizeRange
        self.xKernel_SB.setValue(x_kernel)
        self.yKernel_SB.setValue(y_kernel)
        self.maxConv_SB.setValue(self.project_controller.params.c2d_rp.layersRange)
        min_filters, max_filters = self.project_controller.params.c2d_rp.fPowRange
        self.min_filersPowIndex_SB.setValue(min_filters)
        self.max_filersPowIndex_SB.setValue(max_filters)
        self.cDropout_ChB.setChecked(self.project_controller.params.c2d_rp.dropoutExist)
        self.cMaxDropout_SB.setValue(self.project_controller.params.c2d_rp.dropoutRange)

        self.maxDense_SB.setValue(self.project_controller.params.d2d_rp.layersNumbRange)
        min_neurons, max_neurons = self.project_controller.params.d2d_rp.firstNeuronsRange
        self.min_neuronsPowIndex_SB.setValue(min_neurons)
        self.max_neuronsPowIndex_SB.setValue(max_neurons)
        self.dDropout_ChB.setChecked(self.project_controller.params.d2d_rp.dropoutExist)
        self.dMaxDropout_SB.setValue(self.project_controller.params.d2d_rp.dropoutRange)

        self.netName_LE.setText(self.project_controller.name)
        self.evolEpoch_SB.setValue(self.project_controller.params.genEpoch)
        self.popSize_SB.setValue(self.project_controller.params.popSize)
        copy, cross, mutate = self.project_controller.params.selection
        self.copy_SB.setValue(copy)
        self.cross_SP.setValue(cross)
        self.mutate_SB.setValue(mutate)

        self.batchSize_SB.setValue(self.project_controller.params.nrp.batchSize)
        self.networkEpoch_SB.setValue(self.project_controller.params.nrp.trainEpoch)
        self.DatasetPath_LE.setText(self.project_controller.params.nrp.dataPath)
        # убрать поля путей для сохранения меток, моделей и графиков
        # добавить поле для изменения месторасположения проекта
        self.constLR_ChB.setChecked(True)
        self.minLR_dSB.setValue(self.project_controller.params.nrp.LR_Range[0])
        self.maxLR_dSB.setValue(self.project_controller.params.nrp.LR_Range[1])

    def connect_all(self):

        ############## Widgets Listeners ############
        ###### Buttons ######
        self.search_Btn.clicked.connect(self.search_Btn_Click)
        self.train_Btn.clicked.connect(self.train_Btn_Click)
        self.DatasetPath_TB.clicked.connect(self.datasetPath_TB_Click)
        self.ModelsPath_TB.clicked.connect(self.modelsPath_TB_Click)
        self.LabelPath_TB.clicked.connect(self.labelPath_TB_Click)
        self.PlotPath_TB.clicked.connect(self.plotPath_TB_Click)


        self.actionProperties.triggered.connect(self.show_properties_Click)
        self.modelCheckpoint_ChB.stateChanged.connect(self.modelCheckpoint_checked)
        self.earlyStopping_ChB.stateChanged.connect(self.earlyStopping_checked)

        #######Callbacks#######
        self.earlyStopping_ChB.stateChanged.connect(self.earlyStopping_checked)
        self.modelCheckpoint_ChB.stateChanged.connect(self.modelCheckpoint_checked)
        self.tensorBoard_ChB.stateChanged.connect(self.tensorboard_checked)
        self.scheduler_ChB.stateChanged.connect(self.LRScheduler_checked)
        self.terminateNaN_ChB.stateChanged.connect(self.terminateNaN_checked)
        self.lambda_ChB.stateChanged.connect(self.lambda_callback_checked)
        self.CSVLogger_ChB.stateChanged.connect(self.CSVLogger_checked)
        self.ProgbarLogger_ChB.stateChanged.connect(self.progbar_logger_checked)
        self.remoteMonitor_ChB.stateChanged.connect(self.remote_monitor_checked)
        self.ReduceLR_ChB.stateChanged.connect(self.reduceLR_onPlato_checked)

        self.modelCheckpoint_TB.clicked.connect(self.modelCheckpoint_TB_Click)
        self.tensorBoard_TB.clicked.connect(self.tensorBoard_TB_Click)
        self.earlyStopping_TB.clicked.connect(self.earlyStopping_TB_Click)
        self.scheduler_TB.clicked.connect(self.scheduler_TB_Click)
        self.terminateNaN_TB.clicked.connect(self.terminateNaN_TB_Click)
        self.ReduceLR_TB.clicked.connect(self.reduceLR_TB_Click)
        self.remoteMonitor_TB.clicked.connect(self.remoteMonitor_TB_Click)
        self.lambda_TB.clicked.connect(self.lambda_TB_Click)
        self.CSVLogger_TB.clicked.connect(self.CSVLogger_TB_Click)
        self.ProgbarLogger_TB.clicked.connect(self.progbarLogger_TB_Click)
        ########################

    ################## Listener`s methods ###############
    ####### Buttons ########
    def search_Btn_Click(self):
        #params = self.collectGUIParams()
        #self.project_controller.params = params

        self.paramsQueue.append(self.project_controller)

    def train_Btn_Click(self):
        pass

    def datasetPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Dataset folder",
                                                   self.settings.value("datasetPath", "C:/", type=str))
        if dirlist == "":
            self.DatasetPath_LE.setText(self.settings.value("datasetPath", "C:/", type=str))
        else:
            self.project_controller.params.nrp.dataPath = dirlist
            self.DatasetPath_LE.setText(dirlist)
            self.settings.setValue("datasetPath", dirlist)
            self.settings.sync()

    def modelsPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Models folder",
                                                   self.settings.value("modelsPath", "C:/", type=str))
        if dirlist == "":
            self.ModelPath_LE.setText(self.settings.value("modelsPath", "C:/", type=str))
        else:
            self.project_controller.params.nrp.modelPath = dirlist
            self.ModelPath_LE.setText(dirlist)
            self.settings.setValue("modelsPath", dirlist)
            self.settings.sync()

    def labelPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Labels folder",
                                                   self.settings.value("labelPath", "C:/", type=str))
        if dirlist == "":
            self.Labels_LE.setText(self.settings.value("labelPath", "C:/", type=str))
        else:
            self.project_controller.params.nrp.labelPath = dirlist
            self.Labels_LE.setText(dirlist)
            self.settings.setValue("labelPath", dirlist)
            self.settings.sync()

    def plotPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get Plots folder",
                                                   self.settings.value("plotPath", "C:/", type=str))

        if dirlist == "":
            # лишнее условие, можно упростить
            self.PlotsPath_LE.setText(self.settings.value("plotPath", "C:/", type=str))
        else:
            self.project_controller.params.nrp.plotPath = dirlist
            self.PlotsPath_LE.setText(dirlist)
            self.settings.setValue("plotPath", dirlist)
            self.settings.sync()

    ########### Callbacks properties Listeners #############
    def modelCheckpoint_TB_Click(self):
        self.model_checkpoint_window = ModelCheckpointDlg()
        self.model_checkpoint_window.signal.connect(self.get_model_checkpoint_sett)
        self.model_checkpoint_window.exec()
        pass

    def tensorBoard_TB_Click(self):
        pass

    def earlyStopping_TB_Click(self):
        self.early_stopping_window = EarlyStoppingDlg()
        self.early_stopping_window.signal.connect(self.get_early_stopping_sett)
        self.early_stopping_window.exec()
        pass

    @QtCore.pyqtSlot(object)
    def get_early_stopping_sett(self, data: dict):
        self.callbacks_handler.early_stopping = data
        print("ok")

    @QtCore.pyqtSlot(object)
    def get_model_checkpoint_sett(self, data: dict):
        self.callbacks_handler.model_checkpoint = data

    def scheduler_TB_Click(self):
        pass

    def terminateNaN_TB_Click(self):
        pass

    def reduceLR_TB_Click(self):
        pass

    def remoteMonitor_TB_Click(self):
        pass

    def lambda_TB_Click(self):
        pass

    def CSVLogger_TB_Click(self):
        pass

    def progbarLogger_TB_Click(self):
        pass

    def show_properties_Click(self):
        self.propertyWindow = PropertyWindow()
        self.propertyWindow.exec()
        pass

    ###################################################

    ######### Callbacks checked listeners #######
    def modelCheckpoint_checked(self):
        if self.modelCheckpoint_ChB.isChecked():
            self.callbacks_handler.active["model_checkpoint"] = True
        else:
            self.callbacks_handler.active["model_checkpoint"] = False
        pass

    def earlyStopping_checked(self):
        if self.earlyStopping_ChB.isChecked():
            self.callbacks_handler.active["early_stopping"] = True
        else:
            self.callbacks_handler.active["early_stopping"] = False
        pass

    def tensorboard_checked(self):
        if self.tensorBoard_ChB.isChecked():
            self.callbacks_handler.active["tensorboard"] = True
        else:
            self.callbacks_handler.active["tensorboard"] = False
        pass

    def LRScheduler_checked(self):
        if self.scheduler_ChB.isChecked():
            self.callbacks_handler.active["LRScheduler"] = True
        else:
            self.callbacks_handler.active["LRScheduler"] = False
        pass

    def terminateNaN_checked(self):
        if self.terminateNaN_ChB.isChecked():
            self.callbacks_handler.active["terminateNaN"] = True
        else:
            self.callbacks_handler.active["terminateNaN"] = False
        pass

    def reduceLR_onPlato_checked(self):
        if self.ReduceLR_ChB.isChecked():
            self.callbacks_handler.active["reduceLR_onPlato"] = True
        else:
            self.callbacks_handler.active["reduceLR_onPlato"] = False
        pass

    def remote_monitor_checked(self):
        if self.remoteMonitor_ChB.isChecked():
            self.callbacks_handler.active["remote_monitor"] = True
        else:
            self.callbacks_handler.active["remote_monitor"] = False
        pass

    def lambda_callback_checked(self):
        if self.lambda_ChB.isChecked():
            self.callbacks_handler.active["lambda_callback"] = True
        else:
            self.callbacks_handler.active["lambda_callback"] = False
        pass

    def CSVLogger_checked(self):
        if self.CSVLogger_ChB.isChecked():
            self.callbacks_handler.active["CSVLogger"] = True
        else:
            self.callbacks_handler.active["CSVLogger"] = False
        pass

    def progbar_logger_checked(self):
        if self.ProgbarLogger_ChB.isChecked():
            self.callbacks_handler.active["progbar_logger"] = True
        else:
            self.callbacks_handler.active["progbar_logger"] = False
        pass

    ################################################

    ################# Logic #############################
    def collectGUIParams(self):
        # Convolutional
        cActivations = []
        if self.cReLU_ChB.isChecked(): cActivations.append("relu")
        if self.cSoftMax_ChB.isChecked(): cActivations.append("softmax")
        if self.cLReLU_ChB.isChecked(): cActivations.append("Leaky ReLU")
        if self.cSoftSign_ChB.isChecked(): cActivations.append("softsign")
        if self.cSigmoid_ChB.isChecked(): cActivations.append("sigmoid")
        if self.cELU_ChB.isChecked(): cActivations.append("elu")
        if self.cSELU_ChB.isChecked(): cActivations.append("selu")
        if self.cSoftPlus_ChB.isChecked(): cActivations.append("softplus")
        if self.cTanh_ChB.isChecked(): cActivations.append("tang")
        if self.cPReLU_ChB.isChecked(): cActivations.append("PReLu")
        if self.cTReLU_ChB.isChecked(): cActivations.append("TReLU")

        dActivations = []
        if self.dReLU_ChB.isChecked(): dActivations.append("relu")
        if self.dSoftMax_ChB.isChecked(): dActivations.append("softmax")
        if self.dLReLU_ChB.isChecked(): dActivations.append("Leaky ReLU")
        if self.dSoftSign_ChB.isChecked(): dActivations.append("softsign")
        if self.dSigmoid_ChB.isChecked(): dActivations.append("sigmoid")
        if self.dELU_ChB.isChecked(): dActivations.append("elu")
        if self.dSELU_ChB.isChecked(): dActivations.append("selu")
        if self.dSoftPlus_ChB.isChecked(): dActivations.append("softplus")
        if self.dTanh_ChB.isChecked(): dActivations.append("tang")
        if self.dPReLU_ChB.isChecked(): dActivations.append("PReLu")
        if self.dTReLU_ChB.isChecked(): dActivations.append("TReLU")

        optimizers = []
        # if self.optAdadelta_ChB.isChecked(): optimizers.append("adadelta")
        # if self.optAdagrad_ChB.isChecked(): optimizers.append("adagrad")
        # if self.optAdam_ChB.isChecked(): optimizers.append("adam")
        # if self.optAdamax_ChB.isChecked(): optimizers.append("adamax")
        # if self.optNadam_ChB.isChecked(): optimizers.append("nadam")
        # if self.optRMSprop_ChB.isChecked(): optimizers.append("rmsprop")
        # if self.optSGD_ChB.isChecked(): optimizers.append("sgd")

        loss_func = []
        # if self.lf_BCE_ChB.isChecked(): loss_func.append("binary crossentropy")
        # if self.lf_CCE_ChB.isChecked(): loss_func.append("categorical crossentropy")
        # if self.lf_cHingle_ChB.isChecked(): loss_func.append("categorical hingle")
        # if self.lf_CosProx_ChB.isChecked(): loss_func.append("Cosine proximity")
        # if self.lf_Hingle_ChB.isChecked(): loss_func.append("hinge")
        # if self.lf_KDL_ChB.isChecked(): loss_func.append("kdl")
        # if self.lf_Logcosh.isChecked(): loss_func.append("logcosh")
        # if self.lf_MAE_ChB.isChecked(): loss_func.append("mae")
        # if self.lf_MAPE_ChB.isChecked(): loss_func.append("mape")
        # if self.lf_MSE_ChB.isChecked(): loss_func.append("mse")
        # if self.lf_MSLE_ChB.isChecked(): loss_func.append("msle")
        # if self.lf_Poisson_ChB.isChecked(): loss_func.append("poisson")
        # if self.lf_sCCE_ChB.isChecked(): loss_func.append("sparse categorical crossentropy")
        # if self.lf_sqHingle_ChB.isChecked(): loss_func.append("squared hinge")

        callbacks = []
        # if self.modelCheckpoint_ChB.isChecked(): callbacks.append(0)
        # if self.tensorBoard_ChB.isChecked(): callbacks.append(1)
        # if self.earlyStopping_ChB.isChecked(): callbacks.append(2)
        # if self.scheduler_ChB.isChecked(): callbacks.append(3)
        # if self.terminateNaN_ChB.isChecked(): callbacks.append(4)
        # if self.ReduceLR_ChB.isChecked(): callbacks.append(5)
        # if self.remoteMonitor_ChB.isChecked(): callbacks.append(6)
        # if self.lambda_ChB.isChecked(): callbacks.append(7)
        # if self.CSVLogger_ChB.isChecked(): callbacks.append(8)
        # if self.ProgbarLogger_ChB.isChecked(): callbacks.append(9)

        nrp = NetworkRandomParams(self.constLR_ChB.isChecked(),
                                  [self.minLR_dSB.value(), self.maxLR_dSB.value()],
                                  self.DatasetPath_LE.text(), self.ModelPath_LE.text(), self.Labels_LE.text(),
                                  self.PlotsPath_LE.text(), self.netName_LE.text(), optimizers, loss_func,
                                  self.networkEpoch_SB.value(), self.batchSize_SB.value(), self.callbacks_handler)
        c2d_rp = C2dRandomParams(self.maxConv_SB.value(),
                                 [self.min_filersPowIndex_SB.value(), self.max_filersPowIndex_SB.value()],
                                 len(cActivations), cActivations,
                                 [self.xKernel_SB.value(), self.yKernel_SB.value()],
                                 self.cDropout_ChB.isChecked(), self.cMaxDropout_SB.value())
        d2d_rp = D2dRandomParams(self.maxDense_SB.value(),
                                 [self.min_neuronsPowIndex_SB.value(), self.max_neuronsPowIndex_SB.value()],
                                 Support.getOutputNumb(self.DatasetPath_LE.text()), len(dActivations),
                                 dActivations, self.dDropout_ChB.isChecked(), self.dMaxDropout_SB.value())
        gp = C2D_ChromosomeParams(nrp, c2d_rp, d2d_rp, self.evolEpoch_SB.value(),
                                  [self.copy_SB.value(), self.cross_SP.value(), self.mutate_SB.value()],
                                  self.popSize_SB.value(), self.estimatingWay_CB.currentIndex(), 2,
                                  self.mutateRate_SB.value(), 1, 1)
        return gp

    ########## Forms data setters ##########
    def set_activations_state(self):
        cActivations = self.project_controller.params.c2d_rp.activations
        if "relu" in cActivations: self.cReLU_ChB.setChecked(True)
        if "softmax" in cActivations: self.cSoftMax_ChB.setChecked(True)
        if "Leaky ReLU" in cActivations: self.cLReLU_ChB.setChecked(True)
        if "softsign" in cActivations: self.cSoftSign_ChB.setChecked(True)
        if "sigmoid" in cActivations: self.cSigmoid_ChB.setChecked(True)
        if "elu" in cActivations: self.cELU_ChB.setChecked(True)
        if "selu" in cActivations: self.cSELU_ChB.setChecked(True)
        if "softplus" in cActivations: self.cSoftPlus_ChB.setChecked(True)
        if "tang" in cActivations: self.cTanh_ChB.setChecked(True)
        if "PReLu" in cActivations: self.cPReLU_ChB.setChecked(True)
        if "TReLU" in cActivations: self.cTReLU_ChB.setChecked(True)

        dActivations = self.project_controller.params.d2d_rp.activations
        if "relu" in dActivations: self.dReLU_ChB.setChecked(True)
        if "softmax" in dActivations: self.dSoftMax_ChB.setChecked(True)
        if "Leaky ReLU" in dActivations: self.dLReLU_ChB.setChecked(True)
        if "softsign" in dActivations: self.dSoftSign_ChB.setChecked(True)
        if "sigmoid" in dActivations: self.dSigmoid_ChB.setChecked(True)
        if "elu" in dActivations: self.dELU_ChB.setChecked(True)
        if "selu" in dActivations: self.dSELU_ChB.setChecked(True)
        if "softplus" in dActivations: self.dSoftPlus_ChB.setChecked(True)
        if "tang" in dActivations: self.dTanh_ChB.setChecked(True)
        if "PReLu" in dActivations: self.dPReLU_ChB.setChecked(True)
        if "TReLU" in dActivations: self.dTReLU_ChB.setChecked(True)

    def set_optimizers(self):
        optimizers = self.project_controller.params.nrp.optimizers
        if "adadelta" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "adagrad" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "adam" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "adamax" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "nadam" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "rmsprop" in optimizers: self.optAdadelta_ChB.setChecked(True)
        if "sgd" in optimizers: self.optAdadelta_ChB.setChecked(True)

    def set_loss(self):
        loss = self.project_controller.params.nrp.loss_func
        if "binary crossentropy" in loss: self.lf_BCE_ChB.setChecked(True)
        if "categorical crossentropy" in loss: self.lf_CCE_ChB.setChecked(True)
        if "categorical hingle" in loss: self.lf_cHingle_ChB.setChecked(True)
        if "Cosine proximity" in loss: self.lf_CosProx_ChB.setChecked(True)
        if "hinge" in loss: self.lf_Hingle_ChB.setChecked(True)
        if "kld" in loss: self.lf_KDL_ChB.setChecked(True)
        if "logcosh" in loss: self.lf_Logcosh.setChecked(True)
        if "mae" in loss: self.lf_MAE_ChB.setChecked(True)
        if "mape" in loss: self.lf_MAPE_ChB.setChecked(True)
        if "mse" in loss: self.lf_MSE_ChB.setChecked(True)
        if "msle" in loss: self.lf_MSLE_ChB.setChecked(True)
        if "poisson" in loss: self.lf_Poisson_ChB.setChecked(True)
        if "sparse categorical crossentropy" in loss: self.lf_sCCE_ChB.setChecked(True)
        if "squared hinge" in loss: self.lf_sqHingle_ChB.setChecked(True)

    def set_callbacks(self):
        self.callbacks_handler = self.project_controller.params.nrp.callbacks_handler
        if self.callbacks_handler.active.get("early_stopping"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("model_checkpoint"): self.modelCheckpoint_ChB.setChecked(True)
        if self.callbacks_handler.active.get("tensorboard"): self.tensorBoard_ChB.setChecked(True)
        if self.callbacks_handler.active.get("LRScheduler"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("terminateNaN"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("reduceLR_onPlato"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("remote_monitor"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("lambda_callback"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("CSVLogger"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("progbar_logger"): self.earlyStopping_ChB.setChecked(True)
    ########################################


if __name__ == '__main__':
    # Новый экземпляр QApplication
    QCoreApplication.setOrganizationName("QSoft")
    QCoreApplication.setApplicationName("NN Family Creater")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # print(QtWidgets.QStyleFactory.keys())
    # app.setStyle('Windows')
    # app.setStyle('windowsvista')
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    mainWindow = MainWindow(deque([]))
    mainWindow.show()
    # Запуск
    sys.exit(app.exec_())
