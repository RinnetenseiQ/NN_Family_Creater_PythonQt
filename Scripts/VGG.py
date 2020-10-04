# импортируем бэкенд Agg из matplotlib для сохранения графиков на диск
import sys
from typing import Dict, Any, Union

import matplotlib
# подключаем необходимые пакеты
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
# from keras.models import Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import cv2
import os


import socket
import json

from Chromosomes.C2dChromosome import C2dChromosome
from ChromosomeParams import ChromosomeParams
from Callbacks.FitLogger import FitLogger

matplotlib.use("Agg")


class VGG:
    def __init__(self, chromosome: C2dChromosome, chr_p: ChromosomeParams, sock: socket):
        self.chr_p = chr_p
        self.chromosome = chromosome
        self.sock = sock

    def learn(self):
        # изменить название
        lb, trainX, testX, trainY, testY = self.loadData()
        model = self.createModel()
        history = self.train(model, trainX, trainY, testX, testY)
        summary = self.estimateModel(history, model, testX, testY, lb)
        if summary == [0, 0]: summary = [0, {"accuracy": 0}]
        self.saveModel(model, lb)
        return summary

    def loadData(self):
        # инициализируем данные и метки
        print("[INFO] loading images...")
        self.send("[INFO] loading images...", "chrOutput_TE")
        data = []
        labels = []
        # backend.set_floatx('float16')
        print(backend.floatx())
        # берём пути к изображениям и рандомно перемешиваем
        imagePaths = sorted(list(paths.list_images(self.chr_p.nrp.dataPath)))
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

    def createModel(self):
        modelSeq = Sequential()
        modelSeq.add(ZeroPadding2D((1, 1), input_shape=(128, 128, 3)))
        for i in range(len(self.chromosome.c2d_Part.layers)):
            filters = self.chromosome.c2d_Part.layers[i].filters
            kernel = self.chromosome.c2d_Part.layers[i].kernel
            activation = self.getActivation(0, i)
            dropoutRate = self.chromosome.c2d_Part.layers[i].dropoutRate
            maxpool = self.chromosome.c2d_Part.layers[i].maxpoolExist
            modelSeq.add(
                Conv2D(filters=int(filters), kernel_size=kernel, strides=(1, 1), padding='same', activation=activation))
            if dropoutRate != 0: modelSeq.add(Dropout(dropoutRate))
            if maxpool: modelSeq.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        modelSeq.add(Flatten())
        for i in range(len(self.chromosome.d2d_Part.layers)):
            neurons = self.chromosome.d2d_Part.layers[i].neurons
            activation = self.getActivation(1, i)
            dropoutRate = self.chromosome.d2d_Part.layers[i].dropoutRate
            modelSeq.add(Dense(units=int(neurons), activation=activation))
            if dropoutRate != 0: modelSeq.add(Dropout(dropoutRate))

        modelSeq.add(Dense(units=self.chr_p.d2d_rp.outputNumb, activation='softmax'))
        return modelSeq

    def train(self, model, trainX, trainY, testX, testY):
        print("[INFO] training network...")
        self.send("[INFO] training network...", "chrOutput_TE")
        lr = self.chromosome.constLR
        # настроить выбор оптимизатора!!
        opt = SGD(lr=lr)
        # настроить лосс!!
        loss_func = "categorical_crossentropy"
        model.compile(loss=loss_func, optimizer=opt, metrics=["acc"])

        # обучаем нейросеть
        # H = model.fit(trainX, trainY, validation_data=(testX, testY), epochs=EPOCHS, batch_size=32)

        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")

        callbacks = [FitLogger(self.sock)]
        H = model.fit_generator(aug.flow(trainX, trainY, batch_size=self.chr_p.nrp.batchSize),
                                validation_data=(testX, testY), steps_per_epoch=len(trainX) // self.chr_p.nrp.batchSize,
                                epochs=self.chr_p.nrp.trainEpoch, callbacks=callbacks)
        return H

    def estimateModel(self, H, model, testX, testY, lb):
        # оцениваем нейросеть
        print("[INFO] evaluating network...")
        predictions = model.predict(testX, batch_size=self.chr_p.nrp.batchSize)

        # реализовать в виде графиков с переключением по эпохам
        matrix = confusion_matrix(testY.argmax(axis=1), np.argmax(predictions, axis=1))
        # self.main_window.errorOutput_TE.append(np.array_str(matrix))

        report = classification_report(testY.argmax(axis=1),
                                       predictions.argmax(axis=1), target_names=lb.classes_, output_dict=True)

        # строим графики потерь и точности
        ######## Data for plotting sending ########
        plot_data: Dict[str, Union[int, Any]] = {}
        plot_data["epoch_deJure"] = self.chr_p.nrp.trainEpoch
        plot_data["epoch_deFacto"] = 0  # доделать
        plot_data["confusion_matrix"] = matrix.tolist()
        plot_data["loss"] = str(H.history["loss"])
        plot_data["val_loss"] = str(H.history["val_loss"])
        plot_data["acc"] = str(H.history["acc"])
        plot_data["val_acc"] = str(H.history["val_acc"])
        plot_data = json.dumps(plot_data)
        self.send(plot_data, "chr_plotting")
        ###########################################

        # переделать под интерфейс
        N = np.arange(0, self.chr_p.nrp.trainEpoch)
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(N, H.history["loss"], label="train_loss")
        plt.plot(N, H.history["val_loss"], label="val_loss")
        plt.plot(N, H.history["acc"], label="train_acc")
        plt.plot(N, H.history["val_acc"], label="val_acc")
        plt.title("Training Loss and Accuracy (CNN)")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend()
        plt.savefig(self.chr_p.nrp.plotPath + "\\temp_plot.png")

        # варианты вместо model.summary()
        # model.count_params()  #1

        # 2
        # import keras.backend as K
        # import numpy as np
        # trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))
        # non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))
        # return [len(model.get_weights()), report] #or
        paramsCount = model.count_params()
        return [paramsCount, report]

    def saveModel(self, model, lb):
        # сохраняем модель и бинаризатор меток на диск
        print("[INFO] serializing network and label binarizer...")
        model.save(self.chr_p.nrp.modelPath + "\\temp_model")
        f = open(self.chr_p.nrp.labelPath + "\\temp_label", "wb")
        f.write(pickle.dumps(lb))
        f.close()

    def getActivation(self, mode, i) -> int:
        # подходитЬ не для всех
        # придумат че то другое
        if mode == 0:
            return self.chr_p.c2d_rp.activations[self.chromosome.c2d_Part.layers[i].actIndex]
        else:
            return self.chr_p.d2d_rp.activations[self.chromosome.d2d_Part.layers[i].actIndex]

    def getOptimizer(self, lr):
        # доделать!!!
        optimizers = self.chr_p.nrp.optimizers
        return SGD(lr=lr)

    def send(self, data, codeword):
        data = {"codeword": codeword, "data": data}
        data = json.dumps(data)
