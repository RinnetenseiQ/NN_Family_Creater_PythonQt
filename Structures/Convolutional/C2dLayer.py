from random import SystemRandom as sr
# from C2dRandomParams import C2dRandomParams
from Structures.Convolutional import C2dRandomParams
import random


class C2dLayer(object):

    def __init__(self, c2d_rp: C2dRandomParams.C2dRandomParams, filters):
        self.rnd = random.SystemRandom()
        self.c2d_rp = c2d_rp
        self.filters = filters

        self.dropoutRate = 0
        if c2d_rp.dropoutExist:
            if sr.randint(self.rnd, 0, 100) < 10:
                self.dropoutRate = sr.randint(self.rnd, 10, c2d_rp.dropoutRange)

        self.maxpoolExist = False
        if sr.randint(self.rnd, 0, 100) < 80: self.maxpoolExist = True
        self.actIndex = sr.randint(self.rnd, 0, c2d_rp.actIndexRange)

        self.squareKernel = False
        if sr.randint(self.rnd, 0, 100) < 20: self.squareKernel = True
        self.kernel = [0, 0]
        if self.squareKernel:
            self.kernel[0] = sr.randint(self.rnd, 2, c2d_rp.kernelSizeRange[0])
            self.kernel[1] = self.kernel[0]
        else:
            self.kernel[0] = sr.randint(self.rnd, 1, c2d_rp.kernelSizeRange[0])
            if self.kernel[0] > 1:
                self.kernel[1] = sr.randint(self.rnd, 1, c2d_rp.kernelSizeRange[1])
            else:
                self.kernel[1] = sr.randint(self.rnd, 2, c2d_rp.kernelSizeRange[1])

    def mutate(self, mutateRate):
        self.mutateKernel(mutateRate)
        self.mutateActivation(mutateRate)
        self.mutateDropout(mutateRate)

    def mutateKernel(self, mutateRate):
        # что лучше юзать sr.randint() или sr.randrange()?
        if sr.randint(self.rnd, 0, 100) < mutateRate:
            mutateWay = sr.randint(self.rnd, 0, 100)
            # 10% шанс изменения флага squareKernel и соответствующие этому мутации
            if mutateWay < 10:
                self.squareKernel = not self.squareKernel
                if self.squareKernel:
                    if self.kernel[0] > 1:
                        self.kernel[1] = self.kernel[0]
                    else:
                        self.kernel[0] = self.kernel[1]
                else:
                    randIndex = sr.randrange(self.rnd, len(self.kernel))
                    self.kernel[randIndex] = sr.randrange(self.rnd, 1, self.c2d_rp.kernelSizeRange[randIndex])
            # обычная мутация без изменения флага
            else:
                way = sr.randrange(self.rnd, 3)
                if way == 0:  # меняется только 0й элемент
                    if self.kernel[1] != 1:
                        self.kernel[0] = sr.randrange(self.rnd, 1, self.c2d_rp.kernelSizeRange[0])
                    else:
                        self.kernel[0] = sr.randrange(self.rnd, 2, self.c2d_rp.kernelSizeRange[0])
                elif way == 1:  # меняется только 1й элемент
                    if self.kernel[0] != 1:
                        self.kernel[1] = sr.randrange(self.rnd, 1, self.c2d_rp.kernelSizeRange[1])
                    else:
                        self.kernel[1] = sr.randrange(self.rnd, 2, self.c2d_rp.kernelSizeRange[1])
                else:  # меняются оба (перепроверить!)
                    if self.kernel[1] != 1:
                        self.kernel[0] = sr.randrange(self.rnd, 1, self.c2d_rp.kernelSizeRange[0])
                    else:
                        self.kernel[0] = sr.randrange(self.rnd, 2, self.c2d_rp.kernelSizeRange[0])
                    if self.kernel[0] != 1:
                        self.kernel[1] = sr.randrange(self.rnd, 1, self.c2d_rp.kernelSizeRange[1])
                    else:
                        self.kernel[1] = sr.randrange(self.rnd, 2, self.c2d_rp.kernelSizeRange[1])

            if self.kernel[0] == self.kernel[1]:
                self.squareKernel = True
            else:
                self.squareKernel = False

    def mutateActivation(self, mutateRate):
        if sr.randrange(self.rnd, 100) < mutateRate: self.actIndex = sr.randrange(self.rnd, self.c2d_rp.actIndexRange)

    def mutateDropout(self, mutateRate):
        if self.c2d_rp.dropoutExist:
            if sr.randrange(self.rnd, 100) <= mutateRate:
                way = sr.randrange(self.rnd, 100)
                if way < 30:
                    if self.dropoutRate == 0:
                        self.dropoutRate = sr.randrange(self.rnd, 1, self.c2d_rp.dropoutRange)
                    else:
                        self.dropoutRate == 0
                else:
                    self.dropoutRate = sr.randrange(self.rnd, 1, self.c2d_rp.dropoutRange)
