import math
import os
import json
from typing import Any

class Support:
    def getPow2(x):
        return math.ceil(math.log(x, 2))

    def getOutputNumb(path: str):
        return len(os.listdir(path))  #???

    def selection(totalCount: int, selection: list):
        totalPart = selection[0] + selection[1] + selection[2]
        copyRate = float(selection[0] / totalPart)
        crossRate = float(selection[1] / totalPart)
        mutateRate = float(selection[2] / totalPart)
        copyCount = round(float(copyRate*totalCount))
        crossCount = round(float(crossRate*totalCount))
        mutateCount = round(float(mutateRate*totalCount))

        if (copyCount + crossCount + mutateCount) < totalCount: copyCount += 1
        else:
            if copyCount > 1:
                copyCount -= 1
            else:
                if crossCount > 2:
                    crossCount -= 1
                else: mutateCount -= 1

        if crossCount % 2 > 0 and mutateCount % 2 > 0:
            crossCount -= 1
            mutateCount += 1
        elif crossCount % 2 > 0:
            crossCount -= 1
            copyCount += 1
        elif mutateCount % 2 > 0:
            mutateCount -= 1
            copyCount += 1

        return [copyCount, crossCount, mutateCount]

    def send(target: str, action: str, data: Any,  socket):
        data = {"target": target, "action": action, "data": data}
        data = json.dumps(data)
        data += "&"
        socket.send(bytes(data, encoding="utf-8"))
