import Support
from master.Callbacks.CallbacksHandler import CallbacksHandler

#settings = QSettings()

class NetworkRandomParams:
    def __init__(self, notRandomLR=True, LR_Range=None, dataPath="",
                 project_path="",
                 project_name="", optimizers=None, loss_func=None,
                 trainEpoch=2, batchSize=16, callbacks_handler=None):
        #self.settings = QSettings()
        self.project_path = project_path
        self.callbacks_handler = callbacks_handler or CallbacksHandler()
        self.batchSize = batchSize
        self.trainEpoch = trainEpoch
        self.loss_func = loss_func or ["CCE"]
        self.optimizers = optimizers or ["sgd", "rmsprop"]
        self.project_name = project_name
        #self.plotPath = plotPath or "../Projects/project/saved"
        #self.labelPath = labelPath or "../Projects/project/saved"
        #self.modelPath = modelPath or "../Projects/project/saved"
        self.dataPath = dataPath or "D:/keras/datasets/animals"
        self.LR_Range = LR_Range or [0.001, 0.01]
        self.notRandomLR = notRandomLR
        self.outputNumb = Support.getOutputNumb(self.dataPath)
