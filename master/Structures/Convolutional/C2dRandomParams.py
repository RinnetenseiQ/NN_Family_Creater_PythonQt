class C2dRandomParams:
    dropoutRange: int
    dropoutExist: bool
    kernelSizeRange: list
    activations: list
    actIndexRange: int
    fPowRange: int
    layersRange: int

    def __init__(self, layersRange: int = 5, fPowRange=None,
                 actIndexRange=3, activations=None, kernelSizeRange=None,
                 dropoutExist=False, dropoutRange=50):
        self.dropoutRange: int = dropoutRange
        self.dropoutExist: bool = dropoutExist
        self.kernelSizeRange: list = kernelSizeRange or [7, 7]
        self.activations: list = activations or ["relu", "selu", "elu"]
        self.actIndexRange: int = actIndexRange
        self.fPowRange: list = fPowRange or [3, 5]
        self.layersRange: int = layersRange


if __name__ == "__main__":
    v = C2dRandomParams()
    print("exp")
