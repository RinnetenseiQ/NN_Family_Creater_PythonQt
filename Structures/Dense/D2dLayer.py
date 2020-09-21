from Structures.Dense.D2dRandomParams import D2dRandomParams
import random


class D2dLayer:
    def __init__(self, d2d_rp: D2dRandomParams, neurons):
        self.neurons = neurons
        self.d2d_rp = d2d_rp
        self.sr = random.SystemRandom()

        self.dropoutRate = 0
        if d2d_rp.dropoutExist:
            if self.sr.randrange(100) < 10:
                self.dropoutRate = self.sr.randint(10, d2d_rp.dropoutRange)
        self.actIndex = self.sr.randrange(d2d_rp.actIndexRange)

    def mutateActivation(self, mutateRate):
        if self.sr.randrange(100) <= mutateRate: self.actIndex = self.sr.randrange(self.d2d_rp.actIndexRange)

    def mutateDropout(self, mutateRate):
        if self.d2d_rp.dropoutExist:
            if self.sr.randrange(100) < mutateRate:
                way = self.sr.randrange(100)
                if way < 30:
                    if self.dropoutRate == 0:
                        self.dropoutRate = self.sr.randrange(1, self.d2d_rp.dropoutRange)
                    else:
                        self.dropoutRate = 0
                else:
                    self.dropoutRate = self.sr.randrange(1, self.d2d_rp.dropoutRange)

    def mutate(self, mutateRate):
        self.mutateDropout(mutateRate)
        self.mutateActivation(mutateRate)
