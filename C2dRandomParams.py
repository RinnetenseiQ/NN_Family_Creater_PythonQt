
class C2dRandomParams:
    dropoutRange: int
    dropoutExist: bool
    kernelSizeRange: list
    activations: list
    actIndexRange: int
    fPowRange: int
    layersRange: int

    def __init__(self, layersRange: int, fPowRange,
                 actIndexRange, activations, kernelSizeRange,
                 dropoutExist, dropoutRange):
        self.dropoutRange: int = dropoutRange
        self.dropoutExist = dropoutExist
        self.kernelSizeRange = kernelSizeRange
        self.activations = activations
        self.actIndexRange = actIndexRange
        self.fPowRange = fPowRange
        self.layersRange = layersRange


