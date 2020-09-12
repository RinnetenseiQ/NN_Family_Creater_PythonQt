from Chromosomes.C2dChromosome import C2dChromosome
from Scripts.VGG import VGG
from ChromosomeParams import ChromosomeParams
from typing import List
from threading import Thread


class GeneticProgramThread(Thread):
    def __init__(self, chr_p: ChromosomeParams):
        self.chromosome_params = chr_p
        Thread.__init__(self)

    def run(self):
        genetic_program = GeneticProgram(self.chromosome_params)
        genetic_program.startGeneticSearch()


class GeneticProgram:

    def __init__(self, chr_p: ChromosomeParams):

        self.tempMetrics = []
        self.chr_p = chr_p
        self.population: List[C2dChromosome] = []
        print("init...\n")

    def startGeneticSearch(self):
        self.c2dEvolve()

    def c2dEvolve(self):
        self.population.clear()
        for i in range(self.chr_p.popSize):
            self.population.append(C2dChromosome(self.chr_p))
            self.population[i].name = str(i)
            self.tempMetrics.append(VGG(self.population[i], self.chr_p).learn())

        self.getAssessment(0, self.tempMetrics)
        # self.population = sorted(args, key=lambda x: x.address)
        self.population.sort(key=lambda x: x.assesment, reverse=True)

    def getAssessment(self, mode, metrics):
        if mode == 0:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                self.population[i].assessment = metrics[i][1]["accuracy"] + metrics[i][1]["accuracy"] * minParam / \
                                                metrics[i][0]
