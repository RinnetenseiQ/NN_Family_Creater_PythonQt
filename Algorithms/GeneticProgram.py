from Chromosomes.C2dChromosome import C2dChromosome
from Scripts.VGG import VGG
# import Scripts.VGG as vgg
from ChromosomeParams import ChromosomeParams
from typing import List
from threading import Thread
from Support import Support
from multiprocessing import Process
import socket

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


# from project_main import MainWindow


#class GeneticProgramThread(Thread):
#    def __init__(self, chr_p: ChromosomeParams, mainwindow):
#        self.chromosome_params = chr_p
#        self.mainwindow = mainwindow
#        Thread.__init__(self)

#    def run(self):
#        # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
#        genetic_program = GeneticProgram(self.chromosome_params, self.mainwindow)
#        genetic_program.startGeneticSearch()

class GeneticProgramProcess():
    def __init__(self, chr_p: ChromosomeParams):
        self.chromosome_params = chr_p
        #Process.__init__(self)

    def run(self):
        # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
        genetic_program = GeneticProgram(self.chromosome_params)
        proc = Process(target=genetic_program.startGeneticSearch, args='')
        proc.start()
        proc.join()


class GeneticProgram:

    def __init__(self, chr_p: ChromosomeParams):

        self.tempMetrics = []
        self.chr_p = chr_p
        self.population: List[C2dChromosome] = []
        # print("init...\n")
        self.sock = socket.socket()
        self.sock.connect(('localhost', 12346))

    def startGeneticSearch(self):
        self.c2dEvolve()

    def send(self, data):
        self.sock.send(data.encode("UTF-8"))

    def c2dEvolve(self):
        self.population.clear()
        pbValue = 0
        #self.mainwindow.progressBar.setValue(pbValue)
        pbStep = 100/self.chr_p.genEpoch


        ########## Initialise population ##########
        #self.mainwindow.geneticOutput_TE.append("###################### Epoch 0 ####################\n") ##### GUI ######
        self.send("###################### Epoch 0 ####################\n")
        for i in range(self.chr_p.popSize):
            self.population.append(C2dChromosome(self.chr_p))
            self.population[i].name = str(i)

            #self.mainwindow.geneticOutput_TE.append(self.population[-1].getNetConfig(0))  ##### GUI ######
            self.send(self.population[-1].getNetConfig(0))
            print(self.population[-1].getNetConfig(0))

            current_metrics = VGG(self.population[i], self.chr_p, self.sock).learn()
            self.population[i].paramsCount = current_metrics[0]
            self.population[i].report = current_metrics[1]
            self.tempMetrics.append(current_metrics)

        self.setAssessment(0, self.tempMetrics)

        # self.population = sorted(args, key=lambda x: x.address)
        self.population.sort(key=lambda x: x.assessment, reverse=True)

        #self.mainwindow.geneticOutput_TE.append(self.getAssessment())  ##### GUI ######
        self.send(self.getAssessment())
        #self.mainwindow.geneticOutput_TE.append("###################################################\n")  ##### GUI ######
        self.send("###################################################\n")
        # pbValue = pbValue + pbStep ##### GUI ######
        # self.mainwindow.progressBar.setValue(pbValue) ##### GUI ######

        ###########################################

        ########## Main cycle with genetic operators ###########
        selection = Support.selection(len(self.population), self.chr_p.selection)
        for epoch in range(self.chr_p.genEpoch):
            #self.mainwindow.geneticOutput_TE.append("###################### Epoch " + str(epoch + 1) + "####################\n") ##### GUI ######
            self.send("###################### Epoch " + str(epoch + 1) + "####################\n")
            self.tempMetrics.clear()
            for i in range(len(self.population)):
                is_cross = False
                is_mutate = False
                # проверить условия!!
                if i < selection[0]:
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])
                    #self.mainwindow.geneticOutput_TE.append(self.population[i].getNetConfig(0))  ##### GUI ######
                    self.send(self.population[i].getNetConfig(0))


                    continue
                elif i < selection[0] + selection[1]:
                    is_cross = self.population[i].mutate(self.chr_p.mutateRate)  # реализовать кросс
                else:
                    is_mutate = self.population[i].mutate(self.chr_p.mutateRate)
                if is_cross or is_mutate:
                    #self.mainwindow.geneticOutput_TE.append(self.population[i].getNetConfig(0))  ##### GUI ######
                    self.send(self.population[i].getNetConfig(0))
                    self.tempMetrics.append(VGG(self.population[i], self.chr_p).learn())
                else:
                    #self.mainwindow.geneticOutput_TE.append(self.population[i].getNetConfig(0))  ##### GUI ######
                    self.send(self.population[i].getNetConfig(0))
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])

            self.setAssessment(0, self.tempMetrics)
            self.population.sort(key=lambda x: x.assessment, reverse=True)
            #self.mainwindow.geneticOutput_TE.append(self.getAssessment())  ##### GUI ######
            self.send(self.getAssessment())
            #self.mainwindow.geneticOutput_TE.append("###################################################\n")  ##### GUI ######
            self.send("###################################################\n")
            #pbValue = pbValue + pbStep ##### GUI ######
            #self.mainwindow.progressBar.setValue(pbValue) ##### GUI ######
        self.send("############################### ENDED!!!! ############################")

        ########################################################

    def setAssessment(self, mode, metrics):
        if mode == 0:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                self.population[i].assessment = metrics[i][1].get("accuracy") + metrics[i][1].get(
                    "accuracy") * minParam / metrics[i][0]

    def getAssessment(self):
        est_str = "#### Assessments ####\n"
        for i in self.population:
            est_str += "Chromosome(" + i.name + "): " + str(i.report.get("accuracy")) + "|" + str(
                i.paramsCount) + " => " + str(i.assessment) + "\n"
        est_str += "#####################\n"
        return est_str
