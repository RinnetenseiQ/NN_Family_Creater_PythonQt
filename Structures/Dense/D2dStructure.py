from Structures.Dense.D2dRandomParams import D2dRandomParams
import math
from Structures.Dense.D2dLayer import D2dLayer
from random import SystemRandom as sr
from NetworkRandomParams import NetworkRandomParams
from Support import Support
import random


class D2dStructure:
    def __init__(self, nrp: NetworkRandomParams, d2d_rp: D2dRandomParams):
        self.d2d_rp = d2d_rp
        self.nrp = nrp
        self.rnd = random.SystemRandom()

        if d2d_rp.dropoutExist:
            self.dropoutsExist = True
        else:
            self.dropoutsExist = False

        self.layersNumb = sr.randrange(self.rnd, 1, d2d_rp.layersNumbRange)
        self.layers = []

        self.sameActivations = False
        if sr.randrange(self.rnd, 100) <= 20:
            self.sameActivations = True
        else:
            self.sameActivations = False

        absorber = 0
        if self.sameActivations: absorber = sr.randrange(self.rnd, d2d_rp.actIndexRange)
        powIndex = 0
        for i in range(self.layersNumb):
            if i == 0:
                powIndex = sr.randrange(self.rnd, Support.getPow2(self.nrp.outputNumb), d2d_rp.firstNeuronsRange)
            else:
                powIndex += sr.randrange(self.rnd, 2)
            neurons = math.pow(2, powIndex)
            self.layers.insert(0, D2dLayer(self.d2d_rp, neurons))

            if self.sameActivations: self.layers[0].actIndex = absorber

    def mutate(self, mutateRate):
        self.mutateLayerNumb(mutateRate)

    def mutateLayerNumb(self, mutateRate):
        if not sr.randrange(self.rnd, 100) < mutateRate: return
        self.layersNumb = sr.randrange(self.rnd, 1, self.d2d_rp.layersNumbRange)
        diff = self.layersNumb - len(self.layers)
        if diff > 0:
            powIndex = Support.getPow2(self.layers[0].neurons)
            for i in range(diff):
                powIndex += sr.randrange(self.rnd, 2)
                neurons = math.pow(2, powIndex)
                self.layers.insert(0, D2dLayer(self.d2d_rp, neurons))
                if self.sameActivations: self.layers[0].actIndex = self.layers[1].actIndex
        elif diff < 0:
            # охота реализовать случайный адекватный ремув!
            # абсолютно случайный ремув. Возможно стоит реализовать ремув блоком
            diff = abs(diff)
            for i in range(diff):
                # не нарушится ли индексация?
                self.layers.pop(sr.randrange(self.rnd, len(self.layers)))

    def mutateActivations(self, mutateRate):
        if not sr.randrange(self.rnd, 100) < mutateRate: return  # стоит ли использовать рейт?
        way = sr.randrange(self.rnd, 100)
        if way < 10:
            self.sameActivations = not self.sameActivations
            if self.sameActivations:
                absorber = sr.randrange(self.rnd, len(self.layers))
                for i in self.layers:
                    i.actIndex = self.layers[absorber].actIndex
        else:
            # pass # придумать че делать иначе
            # как вариант
            for i in self.layers:
                i.mutateActivation(mutateRate)

    def mutateNeurons(self, mutateRate):
        if not sr.randrange(self.rnd, 100) < mutateRate: return
        index = sr.randrange(self.rnd, len(self.layers))
        while index != -1:
            if index != (len(self.layers) - 1):
                powIndex = Support.getPow2(self.layers[index + 1].neurons)
            else:
                powIndex = sr.randrange(self.d2d_rp.firstNeuronsRange)
            powIndex += sr.randrange(self.rnd, 2)
            self.layers[index].neurons = math.pow(2, powIndex)
            index -= 1

    def mutateDropouts(self, mutateRate):
        # same questions as in mutateActivations()
        if not self.d2d_rp.dropoutExist: return
        if not sr.randrange(self.rnd, 100) < mutateRate: return
        way = sr.randrange(self.rnd, 100)
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
