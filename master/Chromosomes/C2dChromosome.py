import random
from abc import ABC

from master.Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams
from master.Chromosomes.Chromosome import Chromosome
from master.Structures.Convolutional.C2dStructure import C2dStructure
from master.Structures.Dense.D2dStructure import D2dStructure


class C2dChromosome(Chromosome, ABC):
    def __init__(self, chr_p: C2D_ChromosomeParams):
        self.chr_p = chr_p
        self.c2d_Part = C2dStructure(self.chr_p.c2d_rp)
        self.d2d_Part = D2dStructure(self.chr_p.nrp, self.chr_p.d2d_rp)
        self.sr = random.SystemRandom()
        self.name = ''
        self.report = 0
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
        if is_mutateC2D == 1 or is_mutateD2D == 1:
            return True
        else:
            return False

    def mutateCPart(self, mutateRate):
        if not self.sr.randrange(100) < mutateRate: return 0
        if self.sr.randrange(100) < 10:
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
        return 1

    def getNetConfig(self, mode):
        if mode == 0:
            f_str = ""
            cAct_str = ""
            k_str = ""
            cD_str = ""
            num = 0
            num_filters = 0
            for i in self.c2d_Part.layers:
                f_str += str(i.filters) + " "
                if num > 0 and self.c2d_Part.layers[num-1].filters > i.filters:
                    #raise Exception("PZDC")
                    pass
                num += 1
                cAct_str += self.chr_p.c2d_rp.activations[i.actIndex] + " "
                k_str += str(i.kernel[0]) + "x" + str(i.kernel[1]) + " "
                cD_str += str(i.dropoutRate) + " "

            n_str = ""
            dAct_str = ""
            dD_str = ""
            for i in self.d2d_Part.layers:
                n_str += str(i.neurons) + " "
                dAct_str += self.chr_p.d2d_rp.activations[i.actIndex] + " "
                dD_str += str(i.dropoutRate) + " "

            chr_str = "====== Chromosome(" + self.name + "): ======" + \
                      "\nFilters: " + f_str + \
                      "\ncActivations: " + cAct_str + \
                      "\nKernels: " + k_str + \
                      "\ncDropouts: " + cD_str + \
                      "\nNeurons: " + n_str + \
                      "\ndActivations: " + dAct_str + \
                      "\ndDropouts: " + dD_str + \
                      "\n==================\n"
            return chr_str

    def to_json(self):
        pass
