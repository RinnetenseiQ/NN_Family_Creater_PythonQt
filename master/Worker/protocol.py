import os
import random
import sys
import time

import cv2
import numpy as np
from imutils import paths
from tensorflow.keras.losses import CategoricalCrossentropy
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.layers import (Conv2D, Dense, Flatten,
                                     MaxPool2D, Dropout, Input)
from tensorflow.keras.models import Sequential

from Constants.layers_params import (input_params, conv2d_params, dense_params,
                                     flatten_params, maxpool2d_params, dropout_params)
from Constants.opt_params import sgd_params
from Constants.callbacks_params import early_stopping_params
from Constants.losses_params import cce_params
from Constants.gen_params import IDG_params
from charm_socket import Charm_Socket


def load_data(description):
    if description["type"] == "images":
        return load_images_data(description["path"])
    # придумать что делать с разным количеством возвращаемых параметров


def load_images_data(path):
    # инициализируем данные и метки
    print("[INFO] loading images...")
    data = []
    labels = []
    # берём пути к изображениям и рандомно перемешиваем
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)

    # цикл по изображениям
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (128, 128)).flatten()
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
    trainX = trainX.reshape(trainX.shape[0], 128, 128, 3)
    testX = testX.reshape(testX.shape[0], 128, 128, 3)
    return lb, trainX, testX, trainY, testY


def build_model(network):
    model = Sequential()
    for layer in network["layers"]:
        if layer["type"] == "conv2d":
            model.add(Conv2D(**layer["params"]))
        if layer["type"] == "dense":
            model.add(Dense(**layer["params"]))
        if layer["type"] == "maxpool2d":
            model.add(MaxPool2D(**layer["params"]))
        if layer["type"] == "dropout":
            model.add(Dropout(**layer["params"]))
        if layer["type"] == "flatten":
            model.add(Flatten(**layer["params"]))
        if layer["type"] == "input":
            model.add(Input(**layer["params"]))

    model.compile(optimizer=get_opt(network["optimizer"]),
                  loss=get_loss(network["loss"]),
                  metrics=network["metrics"])
    model.summary()
    return model


def get_opt(opt: dict):
    if opt["type"] == "sgd":
        return SGD(**opt["params"])
    ...


def get_loss(loss: dict):
    if loss["type"] == "categorical_crossentropy":
        if loss["params"]:
            return CategoricalCrossentropy(loss["params"])
        else:
            return loss["type"]
    ...


def get_generator(generator: dict):
    if generator["type"] == "ImageDataGenerator":
        return ImageDataGenerator(**generator["params"])
    else:
        return None


def get_callbacks(callbacks: dict):
    temp = []
    for callback in callbacks:
        if callback["type"] == "early_stopping":
            temp.append(EarlyStopping(callback["params"]))
        if callback["type"] == "checkpoint":
            temp.append(ModelCheckpoint(callback["params"]))
    return temp


def calculate(network):
    lb, trainX, testX, trainY, testY = load_data(network["data"])
    model = build_model(network)
    gen = get_generator(network["generator"])
    callbacks = get_callbacks(network["callbacks"])

    if gen:
        model.fit(gen.flow(trainX, trainY),
                  batch_size=network["batch_size"],
                  epochs=network["epoch"],
                  validation_data=(testX, testY),
                  callbacks=callbacks)
    else:
        model.fit(trainX, trainY,
                  batch_size=network["batch_size"],
                  epochs=network["epoch"],
                  validation_data=(testX, testY),
                  callbacks=callbacks)


def handler(action, data, name):
    ...


if __name__ == "__main__":
    layers = []
    params = input_params.copy()
    params["shape"] = (128, 128, 3)
    layer = {"type": "input", "params": params}
    layers.append(layer)

    layer = {"type": "conv2d", "params": {**conv2d_params.copy(),
                                          "filters": 64,
                                          "padding": "same",
                                          "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "maxpool2d", "params": {**maxpool2d_params.copy(), "strides": (2, 2)}}
    layers.append(layer)
    layer = {"type": "conv2d", "params": {**conv2d_params.copy(), "filters": 128,
                                         "padding": "same",
                                         "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "maxpool2d", "params": {**maxpool2d_params.copy(), "strides": (2, 2)}}
    layers.append(layer)
    layer = {"type": "conv2d", "params": {**conv2d_params.copy(), "filters": 256,
                                         "padding": "same",
                                         "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "maxpool2d", "params": {**maxpool2d_params.copy(), "strides": (2, 2)}}
    layers.append(layer)
    layer = {"type": "conv2d", "params": {**conv2d_params.copy(), "filters": 512,
                                         "padding": "same",
                                         "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "maxpool2d", "params": {**maxpool2d_params.copy(), "strides": (2, 2)}}
    layers.append(layer)
    layer = {"type": "flatten", "params": flatten_params.copy()}
    layers.append(layer)
    layer = {"type": "dense", "params": {**dense_params.copy(), "units": 1024,
                                          "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "dropout", "params": {**dropout_params.copy(), "rate": 0.25}}
    layers.append(layer)
    layer = {"type": "dense", "params": {**dense_params.copy(), "units": 1024,
                                          "activation": "relu"}}
    layers.append(layer)
    layer = {"type": "dropout", "params": {**dropout_params.copy(), "rate": 0.25}}
    layers.append(layer)
    layer = {"type": "dense", "params": {**dense_params.copy(), "units": 5,
                                          "activation": "softmax"}}
    layers.append(layer)

    optimizer = {"type": "sgd", "params": sgd_params.copy()}

    loss = {"type": "categorical_crossentropy", "params": None}

    data = {"type": "images", "path": r"D:\keras\datasets\animals"}

    callback = {"type": "early_stopping", "params": early_stopping_params.copy()}

    callbacks = [callback]

    generator = {"type": "", "params": None}
    metrics = ["acc"]

    network = {"layers": layers,
               "optimizer": optimizer,
               "loss": loss,
               "epoch": 10,
               "batch_size": 16,
               "data": data,  # придется привинчивать загрузку датасета по сети
               "callbacks": callbacks,
               "generator": generator,
               "metrics": metrics,
               "project_path": "./project"}
    #calculate(network)
    print(sys.getsizeof({"action": "calculate", "data": network}))
    comm = Charm_Socket(listener=handler, args=(), address="localhost", port=9088, name="server", is_server=True, buff_size=4096)
    while True:
        time.sleep(5)
        if comm.connections:
            print("is connected")
            print(comm.connections.values())
            #print(comm.connections)
            #print(comm.connections[comm.connections.values()[0]])
            comm.send("calculate", network, list(comm.connections.values())[0])
            break

