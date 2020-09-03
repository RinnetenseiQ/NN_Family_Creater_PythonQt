import math
import os


class Support:
    def getPow2(x):
        return math.ceil(math.log(x, 2))

    def getOutputNumb(path: str):
        directories = filter(os.path.isdir, os.listdir(path))
        return len(directories)
