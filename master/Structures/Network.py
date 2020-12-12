from master.Chromosomes.C2dChromosome import C2dChromosome
from Project_controller import Project_controller


class Network:
    def __init__(self, chromosome, mode):
        self.mode = mode
        if self.mode == Project_controller.C2D_IMG_CLF_GEN:
            self.from_c2d_chr(chromosome)

    def from_c2d_chr(self, chromosome: C2dChromosome):
        self.filters = []
        self.kernels = []
        self.cActivations = []
        self.cActIndexes = []
        self.cDropouts = []
        self.maxPools = []

        self.neurons = []
        self.dActivations = []
        self.dActIndexes = []
        self.dDropouts = []

        self.cActivations = chromosome.c2d_Part.c2d_rp.activations
        for item in chromosome.c2d_Part.layers:
            self.filters.append(item.filters)
            self.kernels.append(item.kernel)
            self.cActIndexes.append(item.actIndex)
            self.cDropouts.append(item.dropoutRate)
            self.maxPools.append(item.maxpoolExist)

        self.dActivations = chromosome.d2d_Part.d2d_rp.activations
        for item in chromosome.d2d_Part.layers:
            self.neurons.append(item.neurons)
            self.dActIndexes.append(item.actIndex)
            self.dDropouts.append(item.dropoutRate)

        self.epoch = chromosome.chr_p.nrp.trainEpoch
        self.BS = chromosome.chr_p.nrp.batchSize
        self.loss_func = chromosome.optimizer
        self.opt = chromosome.loss_func
        self.LR = chromosome.constLR
        self.outputs_numb = chromosome.d2d_Part.nrp.outputNumb
