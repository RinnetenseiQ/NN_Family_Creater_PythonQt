from abc import ABC
from random import SystemRandom as sr
from Structures.Convolutional.C2dStructure import C2dStructure
from Structures.Dense.D2dStructure import D2dStructure
from Chromosomes.Chromosome import Chromosome
from GeneticProgram import GeneticProgram


class C2dChromosome(Chromosome, ABC):
    def __init__(self, gp: GeneticProgram):
        self.gp = gp
        self.c2d_Part = C2dStructure(self.gp.c2d_rp)
        self.d2d_Part = D2dStructure(self.gp.nrp, self.gp.d2d_rp)
        if gp.nrp.notRandomLR: self.constLR = self.gp.nrp.LR_Range[0]
        else: self.constLR = sr.uniform(gp.nrp.LR_Range[0], gp.nrp.LR_Range[1])
        self.optimizer = sr.choice(gp.nrp.optimizers)
        self.loss_func = sr.choice(gp.nrp.loss_func)



    def mutate(self, mutateRate):
        self.mutateCPart(mutateRate)
        self.mutateDPart(mutateRate)

    def mutateCPart(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return
        if sr.randrange(100) < 10: self.c2d_Part = C2dStructure(self.gp.c2d_rp)
        else:
            self.c2d_Part.mutateFilters(mutateRate)
            self.c2d_Part.mutateLayersNumb(mutateRate)
            self.c2d_Part.mutateActivations(mutateRate)
            self.c2d_Part.mutateDropouts(mutateRate)
            self.c2d_Part.mutateKernels(mutateRate)

    def mutateDPart(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return
        if sr.randrange(100) < 10: self.d2d_Part = D2dStructure(self.gp.nrp, self.gp.d2d_rp)
        else:
            self.d2d_Part.mutateDropouts(mutateRate)
            self.d2d_Part.mutateActivations(mutateRate)
            self.d2d_Part.mutateLayerNumb(mutateRate)
            self.d2d_Part.mutateNeurons(mutateRate)


