from NetworkRandomParams import NetworkRandomParams
from Structures.Convolutional.C2dRandomParams import C2dRandomParams
from Structures.Dense.D2dRandomParams import D2dRandomParams
from Chromosomes import Chromosome
from Chromosomes.C2dChromosome import C2dChromosome


class GeneticProgram:
    def __init__(self, nrp: NetworkRandomParams,
                 c2d_rp: C2dRandomParams,
                 d2d_rp: D2dRandomParams,
                 genEpoch, selection, popSize,
                 assessmentWay, percent,
                 mutateRate, accPriority=1, paramPriority=1):
        self.paramPriority = paramPriority
        self.accPriority = accPriority
        self.mutateRate = mutateRate
        self.percent = percent
        self.assessmentWay = assessmentWay
        self.popSize = popSize
        self.selection = selection
        self.genEpoch = genEpoch
        self.d2d_rp = d2d_rp
        self.c2d_rp = c2d_rp
        self.nrp = nrp

    def startC2dEvolution(self):
        pass
