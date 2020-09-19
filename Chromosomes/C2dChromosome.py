from abc import ABC
from random import SystemRandom
from Structures.Convolutional.C2dStructure import C2dStructure
from Structures.Dense.D2dStructure import D2dStructure
from Chromosomes.Chromosome import Chromosome
from ChromosomeParams import ChromosomeParams
import random


class C2dChromosome(Chromosome, ABC):
    def __init__(self, chr_p: ChromosomeParams):
        self.chr_p = chr_p
        self.c2d_Part = C2dStructure(self.chr_p.c2d_rp)
        self.d2d_Part = D2dStructure(self.chr_p.nrp, self.chr_p.d2d_rp)
        self.sr = random.SystemRandom()
        self.name = ''
        self.accuracy = 0
        self.paramsCount = 0
        self.assessment = 0

        if chr_p.nrp.notRandomLR:
            self.constLR = self.chr_p.nrp.LR_Range[0]
        else:
            self.constLR = self.sr.uniform(chr_p.nrp.LR_Range[0], chr_p.nrp.LR_Range[1])
        self.optimizer = self.sr.choice(chr_p.nrp.optimizers)
        self.loss_func = self.sr.choice(chr_p.nrp.loss_func)

    def mutate(self, mutateRate):
        is_mutateC2D = self.mutateCPart(mutateRate)
        is_mutateD2D = self.mutateDPart(mutateRate)
        if is_mutateC2D == 1 or is_mutateD2D == 1: return True
        else: return False

    def mutateCPart(self, mutateRate):
        if not self.sr.randrange(self.sr, 100) < mutateRate: return 0
        if self.sr.randrange(self.sr, 100) < 10:
            self.c2d_Part = C2dStructure(self.chr_p.c2d_rp)
        else:
            self.c2d_Part.mutateFilters(mutateRate)
            self.c2d_Part.mutateLayersNumb(mutateRate)
            self.c2d_Part.mutateActivations(mutateRate)
            self.c2d_Part.mutateDropouts(mutateRate)
            self.c2d_Part.mutateKernels(mutateRate)
        return 1

    def mutateDPart(self, mutateRate):
        if not self.sr.randrange(100) < mutateRate: return 0
        if self.sr.randrange(100) < 10:
            self.d2d_Part = D2dStructure(self.chr_p.nrp, self.chr_p.d2d_rp)
        else:
            self.d2d_Part.mutateDropouts(mutateRate)
            self.d2d_Part.mutateActivations(mutateRate)
            self.d2d_Part.mutateLayerNumb(mutateRate)
            self.d2d_Part.mutateNeurons(mutateRate)
        return
