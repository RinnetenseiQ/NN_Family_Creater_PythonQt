from random import SystemRandom as sr
import random
from Structures.Convolutional.C2dLayer import C2dLayer
from Structures.Convolutional.C2dRandomParams import C2dRandomParams
import math
from Support import Support


class C2dStructure:
    def __init__(self, c2d_rp: C2dRandomParams):
        self.c2d_rp = c2d_rp
        self.rnd = random.SystemRandom()
        if sr.randrange(self.rnd, 100) < 20: self.sameKernel = True
        else: self.sameKernel = False
        if sr.randrange(self.rnd, 100) < 20: self.squaredKernels = True
        else: self.squaredKernels = False
        if sr.randrange(self.rnd, 100) < 20: self.sameActivation = True
        else: self.sameActivation = False
        if sr.randrange(self.rnd, 100) < 30: self.sameActivations = True
        else: self.sameActivations = False
        if c2d_rp.dropoutExist: self.dropoutsExist = True
        else: self.dropoutsExist = False

        self.layersNumb = sr.randrange(self.rnd, c2d_rp.layersRange)
        self.layers = []

        absorber = 0
        if self.sameActivation: absorber = sr.randrange(self.rnd, c2d_rp.actIndexRange)
        powIndex = 0
        for i in range(self.layersNumb):
            if i == 0:
                powIndex = sr.randrange(self.rnd, 1, c2d_rp.fPowRange)
            else:
                powIndex += sr.randrange(self.rnd, 2)
            filters = math.pow(2, powIndex)
            self.layers.append(C2dLayer(c2d_rp, filters))
            if self.sameActivation: self.layers[i].actIndex = absorber
            if self.squaredKernels:
                index = sr.randrange(self.rnd, 2)
                if index == 0:
                    self.layers[i].kernel[1] = self.layers[i].kernel[0]
                else:
                    self.layers[i].kernel[0] = self.layers[i].kernel[1]
                self.layers[i].squareKernel = True
        if self.sameKernel:
            print(len(self.layers))
            absorber = sr.randrange(self.rnd, len(self.layers))
            for i in len(self.layers): self.layers[i].kernel = self.layers[absorber].kernel

    def mutateFilters(self, mutateRate):
        if not sr.randrange(self.rnd, 100) < mutateRate: return
        index = sr.randrange(self.rnd, len(self.layers))
        for i in range(index, len(self.layers)):
            if i != 0:
                powIndex = Support.getPow2(self.layers[index - 1].filters)
            else:
                powIndex = sr.randrange(self.rnd, self.c2d_rp.fPowRange)
            powIndex += sr.randrange(self.rnd, 2)
            self.layers[i].filters = math.pow(2, powIndex)

    def mutateLayersNumb(self, mutateRate):
        if not sr.randrange(self.rnd, 100) < mutateRate: return
        self.layersNumb = sr.randrange(self.rnd, self.c2d_rp.layersRange)
        diff = self.layersNumb - len(self.layers)
        if diff > 0:
            powIndex = Support.getPow2(self.layers[len(self.layers)].filters)
            for i in range(diff):
                powIndex += sr.randrange(self.rnd, 2)
                filters = math.pow(2, powIndex)
                self.layers.append(C2dLayer(self.c2d_rp, filters))
                if self.sameActivation: self.layers[len(self.layers) - 1].actIndex = self.layers[0].actIndex
                if self.sameKernel: self.layers[len(self.layers) - 1].kernel = self.layers[0].kernel
                if self.squaredKernels:
                    if sr.randrange(self.rnd, 2) == 0:
                        self.layers[len(self.layers)].kernel[1] = self.layers[len(self.layers)].kernel[0]
                    else:
                        self.layers[len(self.layers)].kernel[0] = self.layers[len(self.layers)].kernel[1]
        elif diff < 0:
            # аналогично D2dStructure
            # возможно придумаю че нить поинтереснее
            diff = abs(diff)
            for i in range(diff):
                self.layers.pop(sr.randrange(len(self.layers)))

    def mutateActivations(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return  # стоит ли использовать рейт?
        way = sr.randrange(100)
        if way < 10:
            self.sameActivations = not self.sameActivations
            if self.sameActivations:
                absorber = sr.randrange(len(self.layers))
                for i in self.layers:
                    i.actIndex = self.layers[absorber].actIndex
        else:
            # pass # придумать че делать иначе
            # как вариант
            for i in self.layers:
                i.mutateActivation(mutateRate)

    def mutateDropouts(self, mutateRate):
        if not self.c2d_rp.dropoutExist: return
        if not sr.randrange(100) < mutateRate: return
        way = sr.randrange(100)
        if way < 10:
            self.dropoutsExist = not self.dropoutsExist
            if self.dropoutsExist:
                for i in self.layers:
                    i.mutateDropout(mutateRate)
            else:
                for i in self.layers:
                    i.dropoutRate = 0
        else:
            for i in self.layers:
                i.mutateDropout(mutateRate)

    def mutateKernels(self, mutateRate):
        if not sr.randrange(100) < mutateRate: return
        way = sr.randrange(100)
        if way < 10:
            self.sameKernel = not self.sameKernel
            if self.sameKernel:
                index = sr.randrange(len(self.layers))
                for i in self.layers:
                    i.kernel = self.layers[index].kernel
            else:
                for i in self.layers:
                    i.mutateKernel(mutateRate)
        elif way < 20:
            self.squaredKernels = not self.squaredKernels
            if self.squaredKernels:
                for i in self.layers:
                    if sr.randrange(2) == 0:
                        if i.kernel[0] != 1: i.kernel[1] = i.kernel[0]
                        else: i.kernel[0] = i.kernel[1]
                    else:
                        if i.kernel[1] != 1: i.kernel[0] = i.kernel[1]
                        else: i.kernel[1] = i.kernel[0]
                    i.squareKernel = True
            else:
                for i in self.layers:
                    i.mutateKernel(mutateRate)

        # elif way < 50: squred and same
        else:
            for i in self.layers:
                i.mutateKernel(mutateRate)
