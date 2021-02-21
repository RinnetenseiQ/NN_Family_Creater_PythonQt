# from PySide2 import QtWidgets
import sys
from collections import deque

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QFileDialog

from Forms.Parents.c2d_gui_parent import Ui_MainWindow
from Forms.early_stopping_dlg import EarlyStoppingDlg
from Forms.model_checkpoint_dlg import ModelCheckpointDlg
from Forms.property_dlg import PropertyWindow
from Project_controller import Project_controller
from master.Callbacks.CallbacksHandler import CallbacksHandler


# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput


# from (ui filename) import (class)
# from Forms.project_gui import Ui_MainWindow
# from PyQt5.uic.Compiler.qtproxies import QtCore


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    signal = QtCore.pyqtSignal()

    def __init__(self, project_queue: deque, project_controller: Project_controller):
        super().__init__()
        self.project_controller = project_controller
        self.project_queue = project_queue
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
        # self.DatasetPath_LE.setText(self.settings.value("datasetPath", "C:/", type=str))
        # self.ModelPath_LE.setText(self.settings.value("modelsPath", "C:/", type=str))
        # self.Labels_LE.setText(self.settings.value("labelPath", "C:/", type=str))
        # self.PlotsPath_LE.setText(self.settings.value("plotPath", "C:/", type=str))
        self.DatasetPath_LE.setText(self.project_controller.dataset_path)
        self.project_path_LE.setText(self.project_controller.project_path)
        self.project_name_LE.setText(self.project_controller.project_name)

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
        self.project_path_TB.clicked.connect(self.projectPath_TB_Click)
        # self.ModelsPath_TB.clicked.connect(self.modelsPath_TB_Click)
        # self.LabelPath_TB.clicked.connect(self.labelPath_TB_Click)
        # self.PlotPath_TB.clicked.connect(self.plotPath_TB_Click)

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

        ############ Activations ##########
        self.cReLU_ChB.stateChanged.connect(self.cRelu_checked)
        self.dReLU_ChB.stateChanged.connect(self.dRelu_checked)
        self.cSoftMax_ChB.stateChanged.connect(self.cSoftmax_checked)
        self.dSoftMax_ChB.stateChanged.connect(self.dSoftmax_checked)
        self.cLReLU_ChB.stateChanged.connect(self.cLRelu_checked)
        self.dLReLU_ChB.stateChanged.connect(self.dLRelu_checked)
        self.cSoftSign_ChB.stateChanged.connect(self.cSoftsign_checked)
        self.dSoftSign_ChB.stateChanged.connect(self.dSoftsign_checked)
        self.cSigmoid_ChB.stateChanged.connect(self.cSigmoid_checked)
        self.dSigmoid_ChB.stateChanged.connect(self.dSigmoid_checked)
        self.cELU_ChB.stateChanged.connect(self.cElu_checked)
        self.dELU_ChB.stateChanged.connect(self.dElu_checked)
        self.cSELU_ChB.stateChanged.connect(self.cSelu_checked)
        self.dSELU_ChB.stateChanged.connect(self.cSelu_checked)
        self.cSoftPlus_ChB.stateChanged.connect(self.cSoftplus_checked)
        self.dSoftPlus_ChB.stateChanged.connect(self.dSoftplus_checked)
        self.cTanh_ChB.stateChanged.connect(self.cTanh_checked)
        self.dTanh_ChB.stateChanged.connect(self.dTanh_checked)
        self.cPReLU_ChB.stateChanged.connect(self.cPRelu_checked)
        self.dPReLU_ChB.stateChanged.connect(self.dPrelu_checked)
        self.cTReLU_ChB.stateChanged.connect(self.cTRelu_checked)
        self.dTReLU_ChB.stateChanged.connect(self.dTRelu_checked)
        ##########################

        ###### Optimizers ######
        self.optAdadelta_ChB.stateChanged.connect(self.adadelta_checked)
        self.optAdagrad_ChB.stateChanged.connect(self.adagrad_checked)
        self.optAdam_ChB.stateChanged.connect(self.adam_checked)
        self.optAdamax_ChB.stateChanged.connect(self.adamax_checked)
        self.optNadam_ChB.stateChanged.connect(self.nadam_checked)
        self.optRMSprop_ChB.stateChanged.connect(self.rmsprop_checked)
        self.optSGD_ChB.stateChanged.connect(self.sgd_checked)
        #######################################

        ########### Losses ###############
        self.lf_BCE_ChB.stateChanged.connect(self.BCE_lf_checked)
        self.lf_CCE_ChB.stateChanged.connect(self.CCE_lf_checked)
        self.lf_cHingle_ChB.stateChanged.connect(self.cHinge_lf_checked)
        self.lf_CosProx_ChB.stateChanged.connect(self.cProximity_lf_checked)
        self.lf_Hingle_ChB.stateChanged.connect(self.hinge_lf_checked)
        self.lf_KDL_ChB.stateChanged.connect(self.kld_lf_checked)
        self.lf_Logcosh.stateChanged.connect(self.logcosh_lf_checked)
        self.lf_MAE_ChB.stateChanged.connect(self.mae_lf_checked)
        self.lf_MAPE_ChB.stateChanged.connect(self.mape_lf_checked)
        self.lf_MSE_ChB.stateChanged.connect(self.mse_lf_checked)
        self.lf_MSLE_ChB.stateChanged.connect(self.msle_lf_checked)
        self.lf_Poisson_ChB.stateChanged.connect(self.poisson_lf_checked)
        self.lf_sCCE_ChB.stateChanged.connect(self.SCCE_lf_checked)
        self.lf_sqHingle_ChB.stateChanged.connect(self.sqHinge_lf_checked)
        # "BCE"
        # "CCE"
        # "cHinge"
        # "cProximity"
        # "hinge"
        # "kld"
        # "logcosh"
        # "mae"
        # "mape"
        # "mse"
        # "msle"
        # "poisson"
        # "SCCE"
        # "sqHinge"
        ##################################

    ################## Listener`s methods ###############
    ####### Buttons ########
    def search_Btn_Click(self):
        # params = self.collectGUIParams()
        # self.project_controller.params = params
        self.signal.emit()
        self.project_queue.append(self.project_controller)

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

    def projectPath_TB_Click(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Get folder to save project",
                                                   self.settings.value("projectPath", "C:/", type=str))
        if dirlist == "":
            self.project_path_LE.setText(self.settings.value("projectPath", "C:/", type=str))
        else:
            self.project_controller.params.nrp.modelPath = dirlist
            self.project_path_LE.setText(dirlist)
            self.settings.setValue("projectPath", dirlist)
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

    ############ Activations Checked Listeners ############
    def cRelu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("relu")
        else:
            self.cActivations.remove("relu")

    def dRelu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("relu")
        else:
            self.dActivations.remove("relu")

    def cElu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("elu")
        else:
            self.cActivations.remove("elu")

    def dElu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("elu")
        else:
            self.dActivations.remove("elu")

    def cSelu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("selu")
        else:
            self.cActivations.remove("selu")

    def dSelu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("selu")
        else:
            self.dActivations.remove("selu")

    def cLRelu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("Leaky ReLU")
        else:
            self.cActivations.remove("Leaky ReLU")

    def dLRelu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("Leaky ReLU")
        else:
            self.dActivations.remove("Leaky ReLU")

    def cPRelu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("PReLu")
        else:
            self.cActivations.remove("PReLu")

    def dPrelu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("PReLu")
        else:
            self.dActivations.remove("PReLu")

    def cTRelu_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("TReLU")
        else:
            self.cActivations.remove("TReLU")

    def dTRelu_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("TReLU")
        else:
            self.dActivations.remove("TReLU")

    def cSoftplus_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("softplus")
        else:
            self.cActivations.remove("softplus")

    def dSoftplus_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("softplus")
        else:
            self.dActivations.remove("softplus")

    def cSoftmax_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("softmax")
        else:
            self.cActivations.remove("softmax")

    def dSoftmax_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("softmax")
        else:
            self.dActivations.remove("softmax")

    def cSoftsign_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("softsign")
        else:
            self.cActivations.remove("softsign")

    def dSoftsign_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("softsign")
        else:
            self.dActivations.remove("softsign")

    def cTanh_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("tanh")
        else:
            self.cActivations.remove("tanh")

    def dTanh_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("tanh")
        else:
            self.dActivations.remove("tanh")

    def cSigmoid_checked(self):
        if self.cReLU_ChB.isChecked():
            self.cActivations.append("sigmoid")
        else:
            self.cActivations.remove("sigmoid")

    def dSigmoid_checked(self):
        if self.dReLU_ChB.isChecked():
            self.dActivations.append("sigmoid")
        else:
            self.dActivations.remove("sigmoid")

    # "relu"
    # "softmax"
    # "Leaky ReLU"
    # "softsign"
    # "sigmoid"
    # "elu"
    # "selu"
    # "softplus"
    # "tanh"
    # "PReLu"
    # "TReLU"
    # def _checked(self):

    ######################################################

    ########### Optimizers Listeners ##########
    # "adadelta"
    # "adagrad"
    # "adam"
    # "adamax"
    # "nadam"
    # "rmsprop"
    # "sgd"
    def adadelta_checked(self):
        if self.optAdadelta_ChB.isChecked():
            self.optimizers.append("adadelta")
        else:
            self.optimizers.remove("adadelta")

    def adagrad_checked(self):
        if self.optAdagrad_ChB.isChecked():
            self.optimizers.append("adagrad")
        else:
            self.optimizers.remove("adagrad")

    def adam_checked(self):
        if self.optAdam_ChB.isChecked():
            self.optimizers.append("adam")
        else:
            self.optimizers.remove("adam")

    def adamax_checked(self):
        if self.optAdamax_ChB.isChecked():
            self.optimizers.append("adamax")
        else:
            self.optimizers.remove("adamax")

    def nadam_checked(self):
        if self.optNadam_ChB.isChecked():
            self.optimizers.append("nadam")
        else:
            self.optimizers.remove("nadam")

    def rmsprop_checked(self):
        if self.optRMSprop_ChB.isChecked():
            self.optimizers.append("rmsprop")
        else:
            self.optimizers.remove("rmsprop")

    def sgd_checked(self):
        if self.optSGD_ChB.isChecked():
            self.optimizers.append("sgd")
        else:
            self.optimizers.remove("sgd")

    ########################################

    ############### Losses Listeners ##########
    def BCE_lf_checked(self):
        if self.lf_BCE_ChB.isChecked():
            self.loss.append("BCE")
        else:
            self.loss.remove("BCE")

    def CCE_lf_checked(self):
        if self.lf_CCE_ChB.isChecked():
            self.loss.append("CCE")
        else:
            self.loss.remove("CCE")

    def cHinge_lf_checked(self):
        if self.lf_cHingle_ChB.isChecked():
            self.loss.append("cHinge")
        else:
            self.loss.remove("cHinge")

    def cProximity_lf_checked(self):
        if self.lf_CosProx_ChB.isChecked():
            self.loss.append("cProximity")
        else:
            self.loss.remove("cProximity")

    def hinge_lf_checked(self):
        if self.lf_Hingle_ChB.isChecked():
            self.loss.append("hinge")
        else:
            self.loss.remove("hinge")

    def kld_lf_checked(self):
        if self.lf_KDL_ChB.isChecked():
            self.loss.append("kld")
        else:
            self.loss.remove("kld")

    def logcosh_lf_checked(self):
        if self.lf_Logcosh.isChecked():
            self.loss.append("logcosh")
        else:
            self.loss.remove("logcosh")

    def mae_lf_checked(self):
        if self.lf_MAE_ChB.isChecked():
            self.loss.append("mae")
        else:
            self.loss.remove("mae")

    def mape_lf_checked(self):
        if self.lf_MAPE_ChB.isChecked():
            self.loss.append("mape")
        else:
            self.loss.remove("mape")

    def mse_lf_checked(self):
        if self.lf_MSE_ChB.isChecked():
            self.loss.append("mse")
        else:
            self.loss.remove("mse")

    def msle_lf_checked(self):
        if self.lf_MSLE_ChB.isChecked():
            self.loss.append("msle")
        else:
            self.loss.remove("msle")

    def poisson_lf_checked(self):
        if self.lf_Poisson_ChB.isChecked():
            self.loss.append("poisson")
        else:
            self.loss.remove("poisson")

    def SCCE_lf_checked(self):
        if self.lf_sCCE_ChB.isChecked():
            self.loss.append("SCCE")
        else:
            self.loss.remove("SCCE")

    def sqHinge_lf_checked(self):
        if self.lf_sqHingle_ChB.isChecked():
            self.loss.append("sqHinge")
        else:
            self.loss.remove("sqHinge")

    # "BCE"
    # "CCE"
    # "cHinge"
    # "cProximity"
    # "hinge"
    # "kld"
    # "logcosh"
    # "mae"
    # "mape"
    # "mse"
    # "msle"
    # "poisson"
    # "SCCE"
    # "sqHinge"
    ##############################################

    ########## Forms data setters ##########
    def set_activations_state(self):
        self.cActivations = self.project_controller.params.c2d_rp.activations
        if "relu" in self.cActivations: self.cReLU_ChB.setChecked(True)
        if "softmax" in self.cActivations: self.cSoftMax_ChB.setChecked(True)
        if "Leaky ReLU" in self.cActivations: self.cLReLU_ChB.setChecked(True)
        if "softsign" in self.cActivations: self.cSoftSign_ChB.setChecked(True)
        if "sigmoid" in self.cActivations: self.cSigmoid_ChB.setChecked(True)
        if "elu" in self.cActivations: self.cELU_ChB.setChecked(True)
        if "selu" in self.cActivations: self.cSELU_ChB.setChecked(True)
        if "softplus" in self.cActivations: self.cSoftPlus_ChB.setChecked(True)
        if "tanh" in self.cActivations: self.cTanh_ChB.setChecked(True)
        if "PReLu" in self.cActivations: self.cPReLU_ChB.setChecked(True)
        if "TReLU" in self.cActivations: self.cTReLU_ChB.setChecked(True)

        #self.cPReLU_ChB.setCheckable(False)
        self.cPReLU_ChB.setDisabled(True)
        self.cTReLU_ChB.setDisabled(True)
        self.cLReLU_ChB.setDisabled(True)

        self.dActivations = self.project_controller.params.d2d_rp.activations
        if "relu" in self.dActivations: self.dReLU_ChB.setChecked(True)
        if "softmax" in self.dActivations: self.dSoftMax_ChB.setChecked(True)
        if "Leaky ReLU" in self.dActivations: self.dLReLU_ChB.setChecked(True)
        if "softsign" in self.dActivations: self.dSoftSign_ChB.setChecked(True)
        if "sigmoid" in self.dActivations: self.dSigmoid_ChB.setChecked(True)
        if "elu" in self.dActivations: self.dELU_ChB.setChecked(True)
        if "selu" in self.dActivations: self.dSELU_ChB.setChecked(True)
        if "softplus" in self.dActivations: self.dSoftPlus_ChB.setChecked(True)
        if "tanh" in self.dActivations: self.dTanh_ChB.setChecked(True)
        if "PReLu" in self.dActivations: self.dPReLU_ChB.setChecked(True)
        if "TReLU" in self.dActivations: self.dTReLU_ChB.setChecked(True)

        self.dPReLU_ChB.setDisabled(True)
        self.dTReLU_ChB.setDisabled(True)
        self.dLReLU_ChB.setDisabled(True)

    def set_optimizers(self):
        self.optimizers = self.project_controller.params.nrp.optimizers
        if "adadelta" in self.optimizers: self.optAdadelta_ChB.setChecked(True)
        if "adagrad" in self.optimizers: self.optAdagrad_ChB.setChecked(True)
        if "adam" in self.optimizers: self.optAdam_ChB.setChecked(True)
        if "adamax" in self.optimizers: self.optAdamax_ChB.setChecked(True)
        if "nadam" in self.optimizers: self.optNadam_ChB.setChecked(True)
        if "rmsprop" in self.optimizers: self.optRMSprop_ChB.setChecked(True)
        if "sgd" in self.optimizers: self.optSGD_ChB.setChecked(True)
        # "adadelta"
        # "adagrad"
        # "adam"
        # "adamax"
        # "nadam"
        # "rmsprop"
        # "sgd"

    def set_loss(self):
        # "BCE"
        # "CCE"
        # "cHinge"
        # "cProximity"
        # "hinge"
        # "kld"
        # "logcosh"
        # "mae"
        # "mape"
        # "mse"
        # "msle"
        # "poisson"
        # "SCCE"
        # "sqHinge"
        self.loss = self.project_controller.params.nrp.loss_func
        if "BCE" in self.loss: self.lf_BCE_ChB.setChecked(True)
        if "CCE" in self.loss: self.lf_CCE_ChB.setChecked(True)
        if "cHinge" in self.loss: self.lf_cHingle_ChB.setChecked(True)
        if "cProximity" in self.loss: self.lf_CosProx_ChB.setChecked(True)
        if "hinge" in self.loss: self.lf_Hingle_ChB.setChecked(True)
        if "kld" in self.loss: self.lf_KDL_ChB.setChecked(True)
        if "logcosh" in self.loss: self.lf_Logcosh.setChecked(True)
        if "mae" in self.loss: self.lf_MAE_ChB.setChecked(True)
        if "mape" in self.loss: self.lf_MAPE_ChB.setChecked(True)
        if "mse" in self.loss: self.lf_MSE_ChB.setChecked(True)
        if "msle" in self.loss: self.lf_MSLE_ChB.setChecked(True)
        if "poisson" in self.loss: self.lf_Poisson_ChB.setChecked(True)
        if "SCCE" in self.loss: self.lf_sCCE_ChB.setChecked(True)
        if "sqHinge" in self.loss: self.lf_sqHingle_ChB.setChecked(True)

        self.lf_BCE_ChB.setDisabled(True)
        self.lf_CCE_ChB.setDisabled(False)
        self.lf_cHingle_ChB.setDisabled(True)
        self.lf_CosProx_ChB.setDisabled(True)
        self.lf_Hingle_ChB.setDisabled(True)
        self.lf_KDL_ChB.setDisabled(True)
        self.lf_Logcosh.setDisabled(True)
        self.lf_MAE_ChB.setDisabled(True)
        self.lf_MAPE_ChB.setDisabled(True)
        self.lf_MSE_ChB.setDisabled(True)
        self.lf_MSLE_ChB.setDisabled(True)
        self.lf_Poisson_ChB.setDisabled(True)
        self.lf_sCCE_ChB.setDisabled(True)
        self.lf_sqHingle_ChB.setDisabled(True)

    def set_callbacks(self):
        self.callbacks_handler = self.project_controller.params.nrp.callbacks_handler
        if self.callbacks_handler.active.get("early_stopping"): self.earlyStopping_ChB.setChecked(True)
        if self.callbacks_handler.active.get("model_checkpoint"): self.modelCheckpoint_ChB.setChecked(True)
        if self.callbacks_handler.active.get("tensorboard"): self.tensorBoard_ChB.setChecked(True)
        if self.callbacks_handler.active.get("LRScheduler"): self.scheduler_ChB.setChecked(True)
        if self.callbacks_handler.active.get("terminateNaN"): self.terminateNaN_ChB.setChecked(True)
        if self.callbacks_handler.active.get("reduceLR_onPlato"): self.ReduceLR_ChB.setChecked(True)
        if self.callbacks_handler.active.get("remote_monitor"): self.remoteMonitor_ChB.setChecked(True)
        if self.callbacks_handler.active.get("lambda_callback"): self.lambda_ChB.setChecked(True)
        if self.callbacks_handler.active.get("CSVLogger"): self.CSVLogger_ChB.setChecked(True)
        if self.callbacks_handler.active.get("progbar_logger"): self.ProgbarLogger_ChB.setChecked(True)

        #self.earlyStopping_ChB.setDisabled(True)
        #self.modelCheckpoint_ChB.setDisabled(True)
        #self.tensorBoard_ChB.setDisabled(True)
        self.scheduler_ChB.setDisabled(True)
        self.terminateNaN_ChB.setDisabled(True)
        self.ReduceLR_ChB.setDisabled(True)
        self.remoteMonitor_ChB.setDisabled(True)
        self.lambda_ChB.setDisabled(True)
        self.CSVLogger_ChB.setDisabled(True)
        self.ProgbarLogger_ChB.setDisabled(True)
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
