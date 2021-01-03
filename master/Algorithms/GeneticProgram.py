import json
import time
from threading import Thread

from master.Chromosomes.C2dChromosome import C2dChromosome
from Project_controller import Project_controller
from master.Scripts.VGG import VGG
from master.Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams
from typing import List
import Support
from Support import send_remaster, selection
from multiprocessing import Process
import socket

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
from master.Structures.Network import Network


class GeneticProgramProcess:
    def __init__(self, chr_p: C2D_ChromosomeParams):
        self.chromosome_params = chr_p

    def run(self):
        # with PyCallGraph(GraphvizOutput(output_file="graph1.png")):
        # genetic_program = GeneticProgram(self.chromosome_params)
        # proc = Process(target=genetic_program.startGeneticSearch)
        # proc.start()
        # proc.join()
        pass


class Network_Listener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__()
        self.sock = sock
        self.buffer = ""

    def run(self) -> None:
        self.sock.listen()
        conn, addr = self.sock.accept()
        while True:
            # self.buffer = conn.recv(20480).decode('UTF-8')
            data = conn.recv(20480).decode('UTF-8')
            data = data.replace("&", "")
            if not (not data or data == ''):
                self.buffer += data
                conn, addr = self.sock.accept()
            # self.buffer.append(data)
            # data = json.loads(data)


class GeneticProgram(Thread):

    def __init__(self, project_controller: Project_controller, net_port, pc_port: int):

        super().__init__()
        self.net_port = net_port
        self.port = pc_port
        self.tempMetrics = []
        self.project_controller = project_controller
        self.project_params = project_controller.params
        self.population: List[C2dChromosome] = []
        self.pc_sock = socket.socket()
        self.pc_sock.connect(('localhost', pc_port))  # output from genetic search
        with open("../report.txt", "a") as f:
            f.write("GP:\n")
            f.write("pc_port = " + str(pc_port) + "\n")
            f.write("========================\n")
        self.opt_sock = socket.socket()  # output from network

    def run(self) -> None:
        self.opt_sock.bind(('localhost', 0))
        self.listener = Network_Listener(self.opt_sock)
        self.listener.start()
        # self.listener.join()
        if self.project_controller.mode == Project_controller.C2D_IMG_CLF_GEN:
            self.c2dEvolve()

    def c2dEvolve(self):
        self.population.clear()
        ########## Initialise population ##########
        send_remaster("gen_epoch", 0, self.pc_sock)
        for i in range(self.project_params.popSize):
            self.population.append(C2dChromosome(self.project_params))
            self.population[i].name = str(i + 1)
            print(self.population[-1].getNetConfig(0))
            send_remaster("chr_config", self.population[-1].getNetConfig(0), self.pc_sock)
            self.calculate_c2d(self.population[-1], self.project_params, self.net_port, self.opt_sock)
            data = json.loads(self.listener.buffer)
            self.listener.buffer = ""
            paramsCount = data.get("data")[0]
            report = data.get("data")[1]
            self.tempMetrics.append([paramsCount, report])
            self.population[i].paramsCount = paramsCount
            self.population[i].report = report
            send_remaster("interim_est", [paramsCount, report.get("accuracy")], self.pc_sock)

        self.setAssessment(1, self.tempMetrics)
        self.population.sort(key=lambda x: x.assessment, reverse=True)
        send_remaster("accuracy", self.getAccuracy(0), self.pc_sock)
        send_remaster("assesment", self.getAssessment(1, 0), self.pc_sock)
        send_remaster("params", self.getParams(0), self.pc_sock)
        send_remaster("assesment_str", self.getAssessment(0, 0), self.pc_sock)

        ###########################################

        ########## Main cycle with genetic operators ###########
        select = selection(len(self.population), self.project_params.selection)
        for epoch in range(self.project_params.genEpoch):
            send_remaster("accept", "", self.pc_sock)
            self.tempMetrics.clear()
            send_remaster("gen_epoch", epoch + 1, self.pc_sock)
            for i in range(len(self.population)):
                is_cross = False
                is_mutate = False
                # проверить условия!!
                if i < select[0]:
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])
                    continue
                elif i < select[0] + select[1]:
                    is_cross = self.population[i].mutate(self.project_params.mutateRate)  # реализовать кросс
                else:
                    is_mutate = self.population[i].mutate(self.project_params.mutateRate)
                if is_cross or is_mutate:
                    send_remaster("chr_config", self.population[i].getNetConfig(0), self.pc_sock)
                    self.calculate_c2d(self.population[i], self.project_params, self.net_port, self.opt_sock)
                    data = json.loads(self.listener.buffer)
                    self.listener.buffer = ""
                    paramsCount = data.get("data")[0]
                    report = data.get("data")[1]
                    #send_remaster("accept", "", self.pc_sock)
                    send_remaster("interim_est", [paramsCount, report.get("accuracy")], self.pc_sock)
                    self.population[i].paramsCount = paramsCount
                    self.population[i].report = report
                    self.tempMetrics.append([paramsCount, report])

                else:
                    self.tempMetrics.append([self.population[i].paramsCount, self.population[i].report])

            self.setAssessment(1, self.tempMetrics)
            self.population.sort(key=lambda x: x.assessment, reverse=True)
            send_remaster("accuracy", self.getAccuracy(epoch + 1), self.pc_sock)
            send_remaster("assesment", self.getAssessment(1, epoch + 1), self.pc_sock)
            send_remaster("params", self.getParams(epoch + 1), self.pc_sock)
            send_remaster("assesment_str", self.getAssessment(0, epoch+1), self.pc_sock)

        self.project_controller.is_run = False
        self.pc_sock.close()
        ########################################################

    def setAssessment(self, mode, metrics):
        if mode == 0:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                self.population[i].assessment = metrics[i][1].get("accuracy") + metrics[i][1].get(
                    "accuracy") * minParam / metrics[i][0]
        elif mode == 1:
            minParam = metrics[0][0]
            for i in metrics:
                if i[0] < minParam and i != 0: minParam = i[0]
            for i in range(len(metrics)):
                if metrics[i][1].get("accuracy") > 60:
                    self.population[i].assessment = metrics[i][1].get("accuracy") + metrics[i][1].get(
                        "accuracy") * minParam / metrics[i][0]
                else:
                    self.population[i].assessment = metrics[i][1].get("accuracy")

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

    def calculate_c2d(self, chromosome: C2dChromosome, chr_p: C2D_ChromosomeParams, net_port, opt_sock):
        opt_port = opt_sock.getsockname()[1]
        network = Network(chromosome, mode=Project_controller.C2D_IMG_CLF_GEN)
        vgg = VGG(network, chr_p, net_port, opt_port)
        proc = Process(target=vgg.learn)
        proc.start()
        # vgg.start()
        # vgg.join()
        proc.join()
