from PyQt5.QtCore import QSettings

import Support


class NetworkRandomParams:
    def __init__(self, notRandomLR=True, LR_Range=None, dataPath="",
                 modelPath="", labelPath="", plotPath="",
                 networkName="", optimizers=None, loss_func=None,
                 trainEpoch=2, batchSize=16, callbacks_handler=None):
        self.settings = QSettings()
        self.callbacks_handler = callbacks_handler
        self.batchSize = batchSize
        self.trainEpoch = trainEpoch
        self.loss_func = loss_func or ["categorical crossentropy"]
        self.optimizers = optimizers or ["sgd", "rmsprop"]
        self.networkName = networkName
        self.plotPath = plotPath or self.settings.value("plotPath", "C:/", type=str)
        self.labelPath = labelPath or self.settings.value("labelPath", "C:/", type=str)
        self.modelPath = modelPath or self.settings.value("modelsPath", "C:/", type=str)
        self.dataPath = dataPath or self.settings.value("datasetPath", "C:/", type=str)
        self.LR_Range = LR_Range or [0.001, 0.01]
        self.notRandomLR = notRandomLR
        self.outputNumb = Support.getOutputNumb(self.dataPath)
