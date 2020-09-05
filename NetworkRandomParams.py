from Support import Support


class NetworkRandomParams:
    def __init__(self, notRandomLR, LR_Range, dataPath,
                 modelPath, labelPath, plotPath,
                 networkName, optimizers, loss_func,
                 trainEpoch, batchSize):
        self.batchSize = batchSize
        self.trainEpoch = trainEpoch
        self.loss_func = loss_func
        self.optimizers = optimizers
        self.networkName = networkName
        self.plotPath = plotPath
        self.labelPath = labelPath
        self.modelPath = modelPath
        self.dataPath = dataPath
        self.LR_Range = LR_Range
        self.notRandomLR = notRandomLR
        self.outputNumb = Support.getOutputNumb()
