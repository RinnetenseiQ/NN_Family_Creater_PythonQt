from Chromosomes.C2dChromosome import C2dChromosome
from Scripts.VGG import VGG
#import Scripts.VGG as vgg
from ChromosomeParams import ChromosomeParams
from typing import List
from threading import Thread
from Support import Support
#from project_main import MainWindow


class GeneticProgramThread(Thread):
    def __init__(self, chr_p: ChromosomeParams, mainwindow):
        self.chromosome_params = chr_p
        self.mainwindow = mainwindow
        Thread.__init__(self)

    def run(self):
        genetic_program = GeneticProgram(self.chromosome_params, self.mainwindow)
        genetic_program.startGeneticSearch()


class GeneticProgram:

    def __init__(self, chr_p: ChromosomeParams, mainwindow):

        self.tempMetrics = []
        self.chr_p = chr_p
        self.population: List[C2dChromosome] = []
        self.mainwindow = mainwindow
        #print("init...\n")

    def startGeneticSearch(self):
        self.c2dEvolve()

    def c2dEvolve(self):
        self.population.clear()

        ########## Initialise population ##########
        for i in range(self.chr_p.popSize):
            self.population.append(C2dChromosome(self.chr_p))
            self.population[i].name = str(i)
            self.tempMetrics.append(VGG(self.population[i], self.chr_p, self.mainwindow).learn())

        self.getAssessment(0, self.tempMetrics)
        # self.population = sorted(args, key=lambda x: x.address)
        self.population.sort(key=lambda x: x.assessment, reverse=True)

        ###########################################

        ########## Main cycle with genetic operators ###########
        selection = Support.selection(len(self.population), self.chr_p.selection)
        for epoch in range(self.chr_p.genEpoch):
            self.tempMetrics.clear()
            for i in range(len(self.population)):
                is_cross = False
                is_mutate = False
                # проверить условия!!
                if i < selection[0]:
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])
                elif i < selection[0] + selection[1]:
                    is_cross = self.population[i].mutate(self.chr_p.mutateRate)  # реализовать кросс
                else:
                    is_mutate = self.population[i].mutate(self.chr_p.mutateRate)
                if is_cross or is_mutate:
                    self.tempMetrics.append(VGG(self.population[i], self.chr_p, self.mainwindow).learn())
                else: self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])

            self.getAssessment(0, self.tempMetrics)


        ########################################################

    def getAssessment(self, mode, metrics):
        if mode == 0:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                self.population[i].assessment = metrics[i][1].get("accuracy") + metrics[i][1].get("accuracy") * minParam / metrics[i][0]
