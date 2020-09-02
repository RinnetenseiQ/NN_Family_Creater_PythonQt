class GeneticProgram:
    def __init__(self, nrp, c2d_rp, d2d_rp,
                 genEpoch, selection, popSize,
                 assessmentWay, percent,
                 mutateRate, accPriority=1, paramPriority=1):
        self.paramPriority = paramPriority
        self.accPriority = accPriority
        self.mutateRate = mutateRate
        self.percent = percent
        self.assessmentWay = assessmentWay
        self.popSize = popSize
        self.selection = selection
        self.genEpoch = genEpoch
        self.d2d_rp = d2d_rp
        self.c2d_rp = c2d_rp
        self.nrp = nrp
