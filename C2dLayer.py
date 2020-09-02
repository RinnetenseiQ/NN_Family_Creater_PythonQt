import sys
from random import SystemRandom as sr
# from C2dRandomParams import C2dRandomParams
import C2dRandomParams


class C2dLayer(object):

    def __init__(self, c2d_rp: C2dRandomParams.C2dRandomParams, filters):
        self.c2d_rp = c2d_rp
        self.filters = filters

        self.dropoutRate = 0
        if c2d_rp.dropoutExist:
            if sr.randint(0, 100) < 10:
                self.dropoutRate = sr.randint(10, c2d_rp.dropoutRange)

        self.maxpoolExist = False
        if sr.randint(0, 100) < 80: self.maxpoolExist = True
        self.actIndex = sr.randint(0, c2d_rp.actIndexRange - 1)

        self.squareKernel = False
        if sr.randint(0, 100) < 20: self.squareKernel = True
        self.kernel = [0, 0]
        if self.squareKernel:
            self.kernel[0] = sr.randint(2, c2d_rp.kernelSizeRange[0])
            self.kernel[1] = self.kernel[0]
        else:
            self.kernel[0] = sr.randint(1, c2d_rp.kernelSizeRange[0])
            if self.kernel[0] > 1:
                self.kernel[1] = sr.randint(1, c2d_rp.kernelSizeRange[1])
            else:
                self.kernel[1] = sr.randint(2, c2d_rp.kernelSizeRange[1])

    def mutate(self, mutateRate):
        pass

    def mutateKernel(self, mutateRate):
        if sr.randint(0, 100) < mutateRate:
            mutateWay = sr.randint(0, 100)
            if mutateWay < 10:
                self.squareKernel = not self.squareKernel
                if(self.squareKernel):
