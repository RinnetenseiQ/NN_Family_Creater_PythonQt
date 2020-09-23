# from PySide2 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from NetworkRandomParams import NetworkRandomParams
from ChromosomeParams import ChromosomeParams
from Structures.Convolutional.C2dRandomParams import C2dRandomParams
from Structures.Dense.D2dRandomParams import D2dRandomParams
from Support import Support
from collections import deque
from threading import Thread
import time

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from Algorithms.GeneticProgram import GeneticProgramThread

# from (ui filename) import (class)
# from Forms.project_gui import Ui_MainWindow
# from PyQt5.uic.Compiler.qtproxies import QtCore

from Forms.mainWindow_gui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.queue_program_thread: QueueProgramThread = None
        self.setupUi(self)
        self.show()
        self.first_value = None
        self.second_value = None
        self.result = None
        self.example = ""
        self.equal = ""

        self.paramsQueue = deque([])

        ############## Widgets Init #################
        self.errorOutput_TE.setVisible(False)
        self.errorOutput_TE.move(self.geneticOutput_TE.mapToParent(QtCore.QPoint(0, 0)))
        self.errorOutput_TE.resize(self.geneticOutput_TE.size())
        self.chrOutput_TE.setVisible(False)
        self.chrOutput_TE.move(self.geneticOutput_TE.mapToParent(QtCore.QPoint(0, 0)))
        self.chrOutput_TE.resize(self.geneticOutput_TE.size())

        self.coutMode_CB.addItem("Current optimisation search output")
        self.coutMode_CB.addItem("Erroneous output")
        self.coutMode_CB.addItem("Current Chromosome output")
        self.plotMode_CB.addItem("Assessment - Epoch")
        self.plotMode_CB.addItem("Accuracy - Epoch")
        self.plotMode_CB.addItem("Accuracy - Params")
        self.modelMode_CB.addItem("Convolutional")
        self.modelMode_CB.addItem("LSTM")
        self.modelMode_CB.addItem("Perceptron")
        self.modelMode_CB.addItem("GAN")
        self.optimisingAlgMode_CB.addItem("Genetic")
        self.optimisingAlgMode_CB.addItem("Immune")
        self.optimisingAlgMode_CB.addItem("по Ивахненко")
        self.progressBar.setValue(0)
        ###### Experiments ######
        self.lf_CCE_ChB.setChecked(True)


        # self.errorOutput_TE.geometry().moveTo(self.geneticOutput_TE.)
        # self.errorOutput_TE.move(self.geneticOutput_TE.mapToGlobal(QtCore.QPoint(0, 0)))
        #############################################

        ############## Widgets Listeners ############
        ###### Buttons ######
        self.search_Btn.clicked.connect(self.search_Btn_Click)
        self.train_Btn.clicked.connect(self.train_Btn_Click)
        self.DatasetPath_TB.clicked.connect(self.datasetPath_TB_Click)
        self.ModelsPath_TB.clicked.connect(self.modelsPath_TB_Click)
        self.LabelPath_TB.clicked.connect(self.labelPath_TB_Click)
        self.PlotPath_TB.clicked.connect(self.plotPath_TB_Click)
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

        ####### ComboBoxes ###
        # self.coutMode_CB.currentIndexChanged.connect(self.coutMode_CB_SelectedIndexChanged)
        self.coutMode_CB.activated.connect(self.coutMode_CB_SelectedIndexChanged)
        # self.coutMode_CB.highlighted.connect(self.coutMode_CB_SelectedIndexChanged)

        # button.pressed.connect(self.process)
        # self.search_Btn.clicked.connect(lambda: self.search_Btn_Click())
        # QtCore.QObject.connect(self.search_Btn, QtCore.PYQT_SIGNAL('clicked'), self.search_Btn_Click)
        # QtCore.QObject.connectNotify(self.search_Btn, QtCore.PYQT_SIGNAL('clicked'))
        # QtCore.QObject.connect(button, QtCore.SIGNAL('clicked()'), self.onClicked)
        ############################################

    ################## Listener`s methods ###############
    ####### Buttons ########
    def search_Btn_Click(self):
        self.paramsQueue.append(self.collectGUIParams())
        if self.queue_program_thread is None or not self.queue_program_thread.is_alive():
            queue_program_thread = QueueProgramThread(self.paramsQueue, self)
            queue_program_thread.start()

    def train_Btn_Click(self):
        pass

    def datasetPath_TB_Click(self):
        pass

    def modelsPath_TB_Click(self):
        pass

    def labelPath_TB_Click(self):
        pass

    def plotPath_TB_Click(self):
        pass

    def modelCheckpoint_TB_Click(self):
        pass

    def tensorBoard_TB_Click(self):
        pass

    def earlyStopping_TB_Click(self):
        pass

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

        ###### Comboboxes #####

    def coutMode_CB_SelectedIndexChanged(self):
        if self.coutMode_CB.currentIndex() == 0:
            self.geneticOutput_TE.setVisible(True)
            self.errorOutput_TE.setVisible(False)
            self.chrOutput_TE.setVisible(False)
        elif self.coutMode_CB.currentIndex() == 1:
            self.geneticOutput_TE.setVisible(False)
            self.errorOutput_TE.setVisible(True)
            self.chrOutput_TE.setVisible(False)
        elif self.coutMode_CB.currentIndex() == 2:
            self.geneticOutput_TE.setVisible(False)
            self.errorOutput_TE.setVisible(False)
            self.chrOutput_TE.setVisible(True)

    #####################################################

    ################# Logic #############################
    def collectGUIParams(self):
        if self.modelMode_CB.currentIndex() == 0:
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
            if self.optAdadelta_ChB.isChecked(): optimizers.append("adadelta")
            if self.optAdagrad_ChB.isChecked(): optimizers.append("adagrad")
            if self.optAdam_ChB.isChecked(): optimizers.append("adam")
            if self.optAdamax_ChB.isChecked(): optimizers.append("adamax")
            if self.optNadam_ChB.isChecked(): optimizers.append("nadam")
            if self.optRMSprop_ChB.isChecked(): optimizers.append("rmsprop")
            if self.optSGD_ChB.isChecked(): optimizers.append("sgd")

            loss_func = []
            if self.lf_BCE_ChB.isChecked(): loss_func.append("binary crossentropy")
            if self.lf_CCE_ChB.isChecked(): loss_func.append("categorical crossentropy")
            if self.lf_cHingle_ChB.isChecked(): loss_func.append("categorical hingle")
            if self.lf_CosProx_ChB.isChecked(): loss_func.append("Cosine proximity")
            if self.lf_Hingle_ChB.isChecked(): loss_func.append("hinge")
            if self.lf_KDL_ChB.isChecked(): loss_func.append("kdl")
            if self.lf_Logcosh.isChecked(): loss_func.append("logcosh")
            if self.lf_MAE_ChB.isChecked(): loss_func.append("mae")
            if self.lf_MAPE_ChB.isChecked(): loss_func.append("mape")
            if self.lf_MSE_ChB.isChecked(): loss_func.append("mse")
            if self.lf_MSLE_ChB.isChecked(): loss_func.append("msle")
            if self.lf_Poisson_ChB.isChecked(): loss_func.append("poisson")
            if self.lf_sCCE_ChB.isChecked(): loss_func.append("sparse categorical crossentropy")
            if self.lf_sqHingle_ChB.isChecked(): loss_func.append("squared hinge")

            callbacks = []
            if self.modelCheckpoint_ChB.isChecked(): callbacks.append(0)
            if self.tensorBoard_ChB.isChecked(): callbacks.append(1)
            if self.earlyStopping_ChB.isChecked(): callbacks.append(2)
            if self.scheduler_ChB.isChecked(): callbacks.append(3)
            if self.terminateNaN_ChB.isChecked(): callbacks.append(4)
            if self.ReduceLR_ChB.isChecked(): callbacks.append(5)
            if self.remoteMonitor_ChB.isChecked(): callbacks.append(6)
            if self.lambda_ChB.isChecked(): callbacks.append(7)
            if self.CSVLogger_ChB.isChecked(): callbacks.append(8)
            if self.ProgbarLogger_ChB.isChecked(): callbacks.append(9)

            nrp = NetworkRandomParams(self.constLR_ChB.isChecked(),
                                      [self.minLR_dSB.value(), self.maxLR_dSB.value()],
                                      self.DatasetPath_LE.text(), self.ModelPath_LE.text(), self.Labels_LE.text(),
                                      self.PlotsPath_LE.text(), self.netName_LE.text(), optimizers, loss_func,
                                      self.networkEpoch_SB.value(), self.batchSize_SB.value())
            c2d_rp = C2dRandomParams(self.maxConv_SB.value(), self.filersPowIndex_SB.value(),
                                     len(cActivations), cActivations,
                                     [self.xKernel_SB.value(), self.yKernel_SB.value()],
                                     self.cDropout_ChB.isChecked(), self.cMaxDropout_SB.value())
            d2d_rp = D2dRandomParams(self.maxDense_SB.value(), self.neuronsPowIndex_SB.value(),
                                     Support.getOutputNumb(self.DatasetPath_LE.text()), len(dActivations),
                                     dActivations, self.dDropout_ChB.isChecked(), self.dMaxDropout_SB.value())
            gp = ChromosomeParams(nrp, c2d_rp, d2d_rp, self.evolEpoch_SB.value(),
                                  [self.copy_SB.value(), self.cross_SP.value(), self.mutate_SB.value()],
                                  self.popSize_SB.value(), self.estimatingWay_CB.currentIndex(), 2,
                                  self.mutateRate_SB.value(), 1, 1)
            return gp

    #####################################################


class QueueProgramThread(Thread):
    def __init__(self, chr_q: deque, main_window: MainWindow):
        self.chromosome_params_queue = chr_q
        self.main_window = main_window
        Thread.__init__(self)

    def run(self):
        while len(self.chromosome_params_queue) > 0:
            chromosome_params = self.chromosome_params_queue.popleft()
            genetic_program_thread = GeneticProgramThread(chromosome_params, self.main_window)
            genetic_program_thread.start()
            while genetic_program_thread.is_alive():
                time.sleep(2)


if __name__ == '__main__':
    # Новый экземпляр QApplication
    # app = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # app.setStyle('windowsvista')
    # app.setStyle('Windows')
    # print(QStyleFactory.keys())
    # Сздание инстанса класса
    # graphviz = GraphvizOutput(output_file='graph.png')
    #with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
    mainWindow = MainWindow()
    # Запуск
    sys.exit(app.exec_())
