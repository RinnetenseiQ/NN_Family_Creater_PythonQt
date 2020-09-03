from random import SystemRandom as sr
from C2dLayer import C2dLayer
from C2dRandomParams import C2dRandomParams
import math
from Support import Support


class C2dStructure:
    def __init__(self, c2d_rp: C2dRandomParams):
        self.c2d_rp = c2d_rp

        if sr.randrange(100) < 20: self.sameKernel = True
        else: self.sameKernel = False
        if sr.randrange(100) < 20: self.squaredKernels = True
        else: self.squaredKernels = False
        if sr.randrange(100) < 20: self.sameActivation = True
        else: self.sameActivation = False

        self.layersNumb = sr.randrange(c2d_rp.layersRange)
        self.layers = []

        absorber = 0
        if self.sameActivation: absorber = sr.randrange(c2d_rp.actIndexRange)
        powIndex = 0
        for i in range(self.layersNumb):
            if i == 0: powIndex = sr.randrange(1, c2d_rp.fPowRange)
            else: powIndex += sr.randrange(2)
            filters = math.pow(2, powIndex)
            self.layers.append(C2dLayer(c2d_rp, filters))
            if self.sameActivation: self.layers[i].actIndex = absorber
            if self.squaredKernels:
                index = sr.randrange(2)
                if index == 0: self.layers[i].kernel[1] = self.layers[i].kernel[0]
                else: self.layers[i].kernel[0] = self.layers[i].kernel[1]
                self.layers[i].squareKernel = True
        if self.sameKernel:
            absorber = sr.randrange(len(self.layers))
            for i in self.layers: self.layers[i].kernel = self.layers[absorber].kernel

    def mutateFilters(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return
        index = sr.randrange(len(self.layers))
        for i in range(index, len(self.layers)):
            if i != 0: powIndex = Support.getPow2(self.layers[index - 1].filters)
            else: powIndex = sr.randrange(self.c2d_rp.fPowRange)
            powIndex += sr.randrange(2)
            self.layers[i].filters = math.pow(2, powIndex)

    def mutateLayersNumb(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return
        self.layersNumb = sr.randrange(self.c2d_rp.layersRange)
        diff = self.layersNumb - len(self.layers)
        if diff > 0:
            powIndex = Support.getPow2(self.layers[len(self.layers)].filters)
            for i in range(diff):
                powIndex += sr.randrange(2)
                filters = math.pow(2, powIndex)
                self.layers.append(C2dLayer(self.c2d_rp, filters))
                if self.sameActivation: self.layers[len(self.layers) - 1].actIndex = self.layers[0].actIndex
                if self.sameKernel: self.layers[len(self.layers) - 1].kernel = self.layers[0].kernel
                if self.squaredKernels:
                    if sr.randrange(2) == 0: self.layers[len(self.layers)].kernel[1] = self.layers[len(self.layers)].kernel[0]
                    else: self.layers[len(self.layers)].kernel[0] = self.layers[len(self.layers)].kernel[1]
        elif diff < 0:
            # аналогично D2dStructure
            # возможно придумаю че нить поинтереснее
            diff = abs(diff)
            for i in range(diff):
                self.layers.pop(sr.randrange(len(self.layers)))