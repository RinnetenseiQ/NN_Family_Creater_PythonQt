import math
import os
import json
import random
from typing import Any

import cv2
import numpy as np
from imutils import paths
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer


def getPow2(x):
    # return math.ceil(math.log(x, 2))
    return round(math.log(x, 2))


def getOutputNumb(path: str):
    return len(os.listdir(path))  # ???


def selection(totalCount: int, selection: list):
    totalPart = selection[0] + selection[1] + selection[2]
    copyRate = float(selection[0] / totalPart)
    crossRate = float(selection[1] / totalPart)
    mutateRate = float(selection[2] / totalPart)
    copyCount = round(float(copyRate * totalCount))
    crossCount = round(float(crossRate * totalCount))
    mutateCount = round(float(mutateRate * totalCount))

    if (copyCount + crossCount + mutateCount) < totalCount:
        copyCount += 1
    else:
        if copyCount > 1:
            copyCount -= 1
        else:
            if crossCount > 2:
                crossCount -= 1
            else:
                mutateCount -= 1

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


def send(target: str, action: str, data: Any, socket):
    data = {"target": target, "action": action, "data": data}
    data = json.dumps(data)
    data += "&"
    socket.send(bytes(data, encoding="utf-8"))


def send_remaster(action: str, data: Any, socket):
    data = {"action": action, "data": data}
    data = json.dumps(data)
    data += "&"
    socket.send(bytes(data, encoding="utf-8"))


def load_c2d_images(path):
    size_X = 224
    size_Y = 224
    data = []
    labels = []
    # backend.set_floatx('float16')
    # берём пути к изображениям и рандомно перемешиваем
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)

    # цикл по изображениям
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (size_X, size_Y)).flatten()
        data.append(image)

        # извлекаем метку класса из пути к изображению и обновляем
        # список меток
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)
    # os.system('cls')

    # масштабируем интенсивности пикселей в диапазон [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # разбиваем данные на обучающую и тестовую выборки, используя 80%
    # данных для обучения и оставшиеся 20% для тестирования
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=42)

    # конвертируем метки из целых чисел в векторы (для 2х классов при
    # бинарной классификации вам следует использовать функцию Keras
    # “to_categorical” вместо “LabelBinarizer” из scikit-learn, которая
    # не возвращает вектор)
    lb = LabelBinarizer()
    trainY = lb.fit_transform(trainY)
    testY = lb.transform(testY)

    # reshape arrays
    trainX = trainX.reshape(trainX.shape[0], size_X, size_Y, 3)
    testX = testX.reshape(testX.shape[0], size_X, size_Y, 3)
    return lb, trainX, testX, trainY, testY

# class Support:
#     def getPow2(x):
#         # return math.ceil(math.log(x, 2))
#         return round(math.log(x, 2))
#
#     def getOutputNumb(path: str):
#         return len(os.listdir(path))  # ???
#
#     def selection(totalCount: int, selection: list):
#         totalPart = selection[0] + selection[1] + selection[2]
#         copyRate = float(selection[0] / totalPart)
#         crossRate = float(selection[1] / totalPart)
#         mutateRate = float(selection[2] / totalPart)
#         copyCount = round(float(copyRate * totalCount))
#         crossCount = round(float(crossRate * totalCount))
#         mutateCount = round(float(mutateRate * totalCount))
#
#         if (copyCount + crossCount + mutateCount) < totalCount:
#             copyCount += 1
#         else:
#             if copyCount > 1:
#                 copyCount -= 1
#             else:
#                 if crossCount > 2:
#                     crossCount -= 1
#                 else:
#                     mutateCount -= 1
#
#         if crossCount % 2 > 0 and mutateCount % 2 > 0:
#             crossCount -= 1
#             mutateCount += 1
#         elif crossCount % 2 > 0:
#             crossCount -= 1
#             copyCount += 1
#         elif mutateCount % 2 > 0:
#             mutateCount -= 1
#             copyCount += 1
#
#         return [copyCount, crossCount, mutateCount]
#
#     def send(target: str, action: str, data: Any, socket):
#         data = {"target": target, "action": action, "data": data}
#         data = json.dumps(data)
#         data += "&"
#         socket.send(bytes(data, encoding="utf-8"))
