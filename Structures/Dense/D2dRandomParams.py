class D2dRandomParams:
    def __init__(self, layersNumbRange=5, firstNeuronsRange=None, outputNumb=None,
                 actIndexRange=3, activations=None, dropoutExist=False, dropoutRange=0):
        self.dropoutRange = dropoutRange
        self.dropoutExist = dropoutExist
        self.actIndexRange = actIndexRange
        self.outputNumb = outputNumb  # дописать вызов функции getOutputs
        self.firstNeuronsRange = firstNeuronsRange or [3, 5]
        self.layersNumbRange = layersNumbRange
        self.activations = activations or ["relu", "softplus", "softsign", "softmax"]
