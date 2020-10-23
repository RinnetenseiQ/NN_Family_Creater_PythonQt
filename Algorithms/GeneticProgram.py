from Chromosomes.C2dChromosome import C2dChromosome
from Scripts.VGG import VGG
from ChromosomeParams import ChromosomeParams
from typing import List
from Support import Support
from multiprocessing import Process
import socket
import json

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


class GeneticProgramProcess:
    def __init__(self, chr_p: ChromosomeParams):
        self.chromosome_params = chr_p

    def run(self):
        # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
        genetic_program = GeneticProgram(self.chromosome_params)
        proc = Process(target=genetic_program.startGeneticSearch)
        proc.start()
        proc.join()


class GeneticProgram:

    def __init__(self, chr_p: ChromosomeParams):

        self.tempMetrics = []
        self.chr_p = chr_p
        self.population: List[C2dChromosome] = []
        self.sock = socket.socket()
        self.sock.connect(('localhost', 12246))

    def startGeneticSearch(self):
        self.c2dEvolve()

    def c2dEvolve(self):
        self.population.clear()
        Support.send("plot_ui", "clear", "data", self.sock)
        Support.send("plot_ui", "init", self.chr_p.popSize, self.sock)
        pbValue = 0
        Support.send("search_PB", "setValue", pbValue, self.sock)
        pbStep = 100 / (self.chr_p.genEpoch + 1)

        ########## Initialise population ##########
        Support.send("geneticOutput_TE", "appendText", "###################### Epoch 0 ####################\n",
                     self.sock)  ##### GUI ######
        for i in range(self.chr_p.popSize):
            self.population.append(C2dChromosome(self.chr_p))
            self.population[i].name = str(i + 1)

            Support.send("geneticOutput_TE", "appendText", self.population[-1].getNetConfig(0),
                         self.sock)  ##### GUI ######
            print(self.population[-1].getNetConfig(0))

            current_metrics = VGG(self.population[i], self.chr_p, self.sock).learn()
            self.population[i].paramsCount = current_metrics[0]
            self.population[i].report = current_metrics[1]
            self.tempMetrics.append(current_metrics)

        self.setAssessment(0, self.tempMetrics)
        # self.population = sorted(args, key=lambda x: x.address)

        self.population.sort(key=lambda x: x.assessment, reverse=True)

        Support.send("geneticOutput_TE", "appendText", self.getAssessment(0, 0), self.sock)  ##### GUI ######
        Support.send("plot_ui", "assessment", self.getAssessment(1, 0), self.sock)
        ac = self.getAccuracy(0)
        Support.send("plot_ui", "accuracy", ac, self.sock)
        Support.send("plot_ui", "params", self.getParams(0), self.sock)
        Support.send("geneticOutput_TE", "appendText", "###################################################\n",
                     self.sock)  ##### GUI ######
        pbValue = pbValue + pbStep  ##### GUI ######
        Support.send("search_PB", "setValue", pbValue, self.sock)  ##### GUI ######

        ###########################################

        ########## Main cycle with genetic operators ###########
        selection = Support.selection(len(self.population), self.chr_p.selection)
        for epoch in range(self.chr_p.genEpoch):
            Support.send("geneticOutput_TE", "appendText",
                         "###################### Epoch " + str(epoch + 1) + " ####################\n",
                         self.sock)  ##### GUI ######
            self.tempMetrics.clear()
            for i in range(len(self.population)):
                is_cross = False
                is_mutate = False
                # проверить условия!!
                if i < selection[0]:
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])
                    Support.send("geneticOutput_TE", "appendText", self.population[i].getNetConfig(0),
                                 self.sock)  ##### GUI ######
                    continue
                elif i < selection[0] + selection[1]:
                    is_cross = self.population[i].mutate(self.chr_p.mutateRate)  # реализовать кросс
                else:
                    is_mutate = self.population[i].mutate(self.chr_p.mutateRate)
                if is_cross or is_mutate:
                    Support.send("geneticOutput_TE", "appendText", self.population[i].getNetConfig(0),
                                 self.sock)  ##### GUI ######
                    self.tempMetrics.append(VGG(self.population[i], self.chr_p, self.sock).learn())
                else:
                    Support.send("geneticOutput_TE", "appendText", self.population[i].getNetConfig(0),
                                 self.sock)  ##### GUI ######
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])

            self.setAssessment(0, self.tempMetrics)
            self.population.sort(key=lambda x: x.assessment, reverse=True)
            Support.send("geneticOutput_TE", "appendText", self.getAssessment(0, epoch), self.sock)  ##### GUI ######
            Support.send("geneticOutput_TE", "appendText", "###################################################\n",
                         self.sock)  ##### GUI ######
            Support.send("plot_ui", "assessment", self.getAssessment(1, epoch + 1), self.sock)
            ac = self.getAccuracy(epoch + 1)
            Support.send("plot_ui", "accuracy", ac, self.sock)
            #Support.send("plot_ui", "accuracy", self.getAccuracy(epoch + 1), self.sock)
            Support.send("plot_ui", "params", self.getParams(epoch + 1), self.sock)
            pbValue = pbValue + pbStep  ##### GUI ######
            Support.send("search_PB", "setValue", pbValue, self.sock)  ##### GUI ######
        Support.send("geneticOutput_TE", "appendText",
                     "############################### ENDED!!!! ############################", self.sock)
        Support.send("target", "reconnect", "data", self.sock)
        ########################################################

    def setAssessment(self, mode, metrics):
        if mode == 0:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                self.population[i].assessment = metrics[i][1].get("accuracy") + metrics[i][1].get(
                    "accuracy") * minParam / metrics[i][0]

    def getAssessment(self, mode, epoch):
        if mode == 0:
            est_str = "#### Assessments ####\n"
            for i in self.population:
                est_str += "Chromosome(" + i.name + "): " + str(i.report.get("accuracy")) + "|" + str(
                    i.paramsCount) + " => " + str(i.assessment) + "\n"
            est_str += "#####################\n"
            return est_str
        if mode == 1:
            est = {}
            for i in self.population:
                chr_name = "Chromosome(" + i.name + ")"
                est[chr_name] = i.assessment

            est["epoch"] = epoch
            return est

    def getAccuracy(self, epoch):
        accuracy = {}
        for i in self.population:
            chr_name = "Chromosome(" + i.name + ")"
            accuracy[chr_name] = i.report.get("accuracy")
        accuracy["epoch"] = epoch
        return accuracy

    def getParams(self, epoch):
        params = {}
        for i in self.population:
            chr_name = "Chromosome(" + i.name + ")"
            params[chr_name] = i.paramsCount
        params["epoch"] = epoch
        return params
