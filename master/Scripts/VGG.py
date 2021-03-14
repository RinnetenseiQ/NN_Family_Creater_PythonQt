# импортируем бэкенд Agg из matplotlib для сохранения графиков на диск
import json
import os
import pickle
import random
import socket
from typing import Dict, Any, Union

import cv2
import matplotlib
import numpy as np
from imutils import paths
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
# подключаем необходимые пакеты
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras import backend
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from Support import send_remaster
from master.Callbacks.FitLogger import FitLogger
from master.Chromosomes.C2D_ChromosomeParams import C2D_ChromosomeParams
from master.Structures.Network import Network
from threading import Thread
import time

#matplotlib.use("Agg")

def func():
    while True:
        print("thread")
        time.sleep(1)

class VGG:
    def __init__(self, network: Network, chr_p: C2D_ChromosomeParams, project_controller_port: int,
                 optimising_port: int, project_path='../Projects/project'):

        self.project_path = project_path
        self.chr_p = chr_p
        self.network = network
        # port = self.sock_network.getsockname()[1]
        self.opt_send_socket = socket.socket()
        self.opt_send_socket.connect(("localhost", optimising_port))

        self.pc_send_socket = socket.socket()
        try:
            self.pc_send_socket.connect(("localhost", project_controller_port))
        except ConnectionRefusedError as e:
            print("Conn")
            print(project_controller_port)
            with open("../../report.txt", "a") as f:
                f.write("VGG:\n")
                f.write("project_controller_port = " + str(project_controller_port) + "\n")
                f.write("========================\n")
        except Exception:
            print("Ex")
            print(project_controller_port)
            pass

        super().__init__()

    def run(self) -> None:
        self.learn()

    def learn(self):
        # изменить название
        # try:
        #     lb, trainX, testX, trainY, testY = self.loadData()
        #     model = self.createModel()
        #     history = self.train(model, trainX, trainY, testX, testY)
        #     summary = self.estimateModel(history, model, testX, testY, lb)
        #     # if summary == [0, 0]: summary = [0, {"accuracy": 0}]
        #     send_remaster("summary", summary, self.opt_send_socket)
        #     send_remaster("accept", "", self.pc_send_socket)
        #     self.opt_send_socket.close()
        #     self.pc_send_socket.close()
        #     #self.saveModel(model, lb)
        #
        #     # return summary
        # except MemoryError:
        #     print("Memory Error")
        #     summary = [0, {"accuracy": 0}]
        #     send_remaster("summary", summary, self.opt_send_socket)
        #     self.opt_send_socket.close()
        #     self.pc_send_socket.close()
        #     # return summary
        # except Exception:
        #     print("Exeption")
        #     summary = [0, {"accuracy": 0}]
        #     send_remaster("summary", summary, self.opt_send_socket)
        #     self.opt_send_socket.close()
        #     self.pc_send_socket.close()


            # return summary


        ####### For testing ########

        lb, trainX, testX, trainY, testY = self.loadData()
        model = self.createModel()
        history = self.train(model, trainX, trainY, testX, testY)
        summary = self.estimateModel(history, model, testX, testY, lb)
        # if summary == [0, 0]: summary = [0, {"accuracy": 0}]
        send_remaster("summary", summary, self.opt_send_socket)
        send_remaster("accept", "", self.pc_send_socket)
        self.opt_send_socket.close()
        self.pc_send_socket.close()
        # if summary == [0, 0]: summary = [0, {"accuracy": 0}]
        #self.saveModel(model, lb)
        # return summary

    def loadData(self):
        # инициализируем данные и метки
        print("[INFO] loading images...")
        # Support.send("chrOutput_TE", "appendText", "[INFO] loading images...", self.sock)
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
        for filters, kernel, cActIndex, cDropout, maxpool in zip(self.network.filters, self.network.kernels,
                                                        self.network.cActIndexes, self.network.cDropouts, self.network.maxPools):
            activation = self.network.cActivations[cActIndex]
            modelSeq.add(
                Conv2D(filters=int(filters), kernel_size=kernel, strides=(1, 1), padding='same', activation=activation))
            if cDropout != 0: modelSeq.add(Dropout(float(cDropout) / 100))
            if maxpool: modelSeq.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        modelSeq.add(Flatten())
        for neurons, dActIndex, dDropout in zip(self.network.neurons, self.network.dActIndexes, self.network.dDropouts):
            activation = self.network.dActivations[dActIndex]
            modelSeq.add(Dense(units=int(neurons), activation=activation))
            if dDropout != 0: modelSeq.add(Dropout(float(dDropout) / 100))

        modelSeq.add(Dense(units=self.network.outputs_numb, activation='softmax'))
        return modelSeq

    def train(self, model, trainX, trainY, testX, testY):
        print("[INFO] training network...")
        # Support.send("chrOutput_TE", "appendText", "[INFO] training network...", self.sock)
        lr = self.network.LR
        # настроить выбор оптимизатора!!
        opt = SGD(lr=lr)
        # настроить лосс!!
        summary = model.summary()
        loss_func = "categorical_crossentropy"
        model.compile(loss=loss_func, optimizer=opt, metrics=["acc"])

        # обучаем нейросеть
        # H = model.fit(trainX, trainY, validation_data=(testX, testY), epochs=EPOCHS, batch_size=32)

        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
        callbacks = self.chr_p.nrp.callbacks_handler.getCallbacks()
        callbacks.append(FitLogger(self.pc_send_socket))
        # callbacks = [FitLogger(self.sock)]
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
        print(classification_report(testY.argmax(axis=1),
                                    predictions.argmax(axis=1), target_names=lb.classes_, output_dict=False))

        # строим графики потерь и точности
        ######## Data for plotting sending ########
        loss = np.array(H.history["loss"]).tolist()
        val_loss = np.array(H.history["val_loss"]).tolist()
        acc = np.array(H.history["acc"]).tolist()
        val_acc = np.array(H.history["val_acc"]).tolist()

        plot_data: Dict[str, Union[int, Any]] = {}
        plot_data["epoch_deJure"] = self.chr_p.nrp.trainEpoch
        plot_data["epoch_deFacto"] = len(loss)  # доделать
        plot_data["confusion_matrix"] = matrix.tolist()
        plot_data["loss"] = loss
        plot_data["val_loss"] = val_loss
        plot_data["acc"] = acc
        plot_data["val_acc"] = val_acc
        # plot_data["loss"] = H.history["loss"]
        # plot_data["val_loss"] = H.history["val_loss"]
        # plot_data["acc"] = H.history["acc"]
        # plot_data["val_acc"] = H.history["val_acc"]
        plot_data = json.dumps(plot_data)
        send_remaster("plot_data", plot_data, self.pc_send_socket)
        # Support.send("plot_ui", "chr_plotting", plot_data, self.sock)
        ###########################################

        # переделать под интерфейс
        # N = np.arange(0, self.chr_p.nrp.trainEpoch)
        # plt.style.use("ggplot")
        # plt.figure()
        # plt.plot(N, H.history["loss"], label="train_loss")
        # plt.plot(N, H.history["val_loss"], label="val_loss")
        # plt.plot(N, H.history["acc"], label="train_acc")
        # plt.plot(N, H.history["val_acc"], label="val_acc")
        # plt.title("Training Loss and Accuracy (CNN)")
        # plt.xlabel("Epoch #")
        # plt.ylabel("Loss/Accuracy")
        # plt.legend()
        # plt.savefig(self.chr_p.nrp.plotPath + "\\temp_plot.png")
        # plt.close('all')

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
        # model.save(self.project_path + "/saved/temp_model")
        model.save(self.project_path + "/saved/temp_model.h5")
        with open(self.project_path + "/saved/temp_label", "wb") as f:
            # f = open(self.chr_p.nrp.labelPath + "\\temp_label", "wb")
            f.write(pickle.dumps(lb))

    def getActivation(self, mode, i) -> int:
        # подходитЬ не для всех
        # придумат че то другое
        if mode == 0:
            return self.activations[self.network.c2d_Part.layers[i].actIndex]
        else:
            return self.chr_p.d2d_rp.activations[self.network.d2d_Part.layers[i].actIndex]

    def getOptimizer(self, lr):
        # доделать!!!
        optimizers = self.chr_p.nrp.optimizers
        return SGD(lr=lr)
