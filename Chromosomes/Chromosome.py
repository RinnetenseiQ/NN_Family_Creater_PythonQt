from abc import ABC, abstractmethod


class Chromosome(ABC):

    @abstractmethod
    def mutate(self, mutateRate):
        pass
