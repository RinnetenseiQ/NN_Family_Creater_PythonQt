from master.Structures.NetworkRandomParams import NetworkRandomParams
from master.Structures.Convolutional.C2dRandomParams import C2dRandomParams
from master.Structures.Dense.D2dRandomParams import D2dRandomParams


class C2D_ChromosomeParams:
    def __init__(self, nrp: NetworkRandomParams = None,
                 c2d_rp: C2dRandomParams = C2dRandomParams(),
                 d2d_rp: D2dRandomParams = None,
                 genEpoch=20, selection=None, popSize=5,
                 assessmentWay=0, percent=70,
                 mutateRate=70, accPriority=1, paramPriority=1):
        self.paramPriority = paramPriority
        self.accPriority = accPriority
        self.mutateRate = mutateRate
        self.percent = percent
        self.assessmentWay = assessmentWay
        self.popSize = popSize
        self.selection = selection or [1, 2, 2]
        self.genEpoch = genEpoch
        self.d2d_rp = d2d_rp or D2dRandomParams()
        self.c2d_rp = c2d_rp or C2dRandomParams()
        self.nrp = nrp or NetworkRandomParams()