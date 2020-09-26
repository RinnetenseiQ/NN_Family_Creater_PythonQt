from abc import ABC, abstractmethod


class Chromosome(ABC):

    @abstractmethod
    def mutate(self, mutateRate):
        pass

    @abstractmethod
    def getNetConfig(self, mode):
        pass

    @abstractmethod
    def to_json(self):
        pass
