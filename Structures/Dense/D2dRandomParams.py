class D2dRandomParams:
    def __init__(self, layersNumbRange, firstNeuronsRange, outputNumb,
                 actIndexRange, activations, dropoutExist, dropoutRange):
        self.dropoutRange = dropoutRange
        self.dropoutExist = dropoutExist
        self.actIndexRange = actIndexRange
        self.outputNumb = outputNumb
        self.firstNeuronsRange = firstNeuronsRange
        self.layersNumbRange = layersNumbRange
        self.activations = activations
